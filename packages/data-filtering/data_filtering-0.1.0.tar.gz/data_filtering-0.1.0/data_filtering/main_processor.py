# qa_filter/main_processor.py

import argparse
import pkg_resources # 또는 from importlib import resources
import os
import yaml
from typing import Dict, Optional, Any, Tuple
import pandas as pd

from .data_handler import DataHandler
from .quality_checker import QualityChecker
from .duplication_handler import DuplicationHandler
from .report_generator import ReportGenerator

# 프로젝트 루트 경로 설정 (main_processor.py가 qa_filter 내부에 있으므로)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DEFAULT_CONFIG_PATH = pkg_resources.resource_filename('data_filtering', 'config/default_settings.yaml')

class MainProcessor:
    def __init__(self, config_path: Optional[str] = None, **cli_kwargs):
        self.config = self._load_and_merge_configs(config_path, **cli_kwargs)
        self.data_handler = DataHandler(self.config)

    def _deep_update(self, base_dict: Dict, update_dict: Dict) -> Dict:
        """Helper function to deeply update a dictionary."""
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
                base_dict[key] = self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
        return base_dict

    def _load_and_merge_configs(self, user_config_path: Optional[str] = None, **cli_kwargs) -> Dict:
        """Loads configurations in order: default, user_file, cli_kwargs."""
        # 1. Load default settings
        if not os.path.exists(DEFAULT_CONFIG_PATH): # pkg_resources.resource_filename이 실제 파일 시스템 경로를 반환하므로 os.path.exists로 확인 가능
            raise FileNotFoundError(f"Default configuration file not found at expected package path: {DEFAULT_CONFIG_PATH}")
        with open(DEFAULT_CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # 2. Load user-provided config file (if any) and merge
        if user_config_path:
            user_config_path_abs = os.path.join(PROJECT_ROOT, user_config_path) \
                if not os.path.isabs(user_config_path) else user_config_path
            if os.path.exists(user_config_path_abs):
                with open(user_config_path_abs, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                config = self._deep_update(config, user_config) # Deep update
            else:
                print(f"Warning: User-specified config file not found at {user_config_path_abs}. Using defaults.")

        # 3. Override with CLI arguments (kwargs)
        # CLI kwargs might be flat, need to map them to nested config structure if necessary
        # For simplicity, assume cli_kwargs match top-level keys or specific nested keys handled in process()
        # More robust CLI parsing would map args like --dedup-threshold to config['deduplication']['semantic_threshold']
        
        # Simple override for top-level keys passed via cli_kwargs
        # For nested keys, they need to be handled where they are used or parsed more carefully
        config = self._deep_update(config, {k: v for k, v in cli_kwargs.items() if v is not None})
        
        return config
    
    def _get_effective_input_params(self, 
                                    input_csv_path: str,
                                    cli_q_col: Optional[str], cli_a_col: Optional[str], 
                                    cli_qa_col: Optional[str], cli_encoding: Optional[str]
                                   ) -> Tuple[str, Optional[str], Optional[str], Optional[str], str]:
        """Determines effective input parameters based on CLI args and config."""
        # Config values are fallbacks if CLI args are not provided
        q_col = cli_q_col if cli_q_col is not None else self.config.get('q_col')
        a_col = cli_a_col if cli_a_col is not None else self.config.get('a_col')
        qa_col = cli_qa_col if cli_qa_col is not None else self.config.get('qa_col')
        encoding = cli_encoding if cli_encoding is not None else self.config.get('encoding', 'utf-8')
        
        # Validate that at least q_col (with or without a_col) or qa_col is specified
        if not qa_col and not q_col:
             raise ValueError("Either 'qa_col' or 'q_col' (question column) must be specified "
                              "either via CLI or in the configuration file.")
        
        # If qa_col is specified, it usually takes precedence (DataHandler logic)
        # If q_col is specified but not a_col, DataHandler will handle it (warn and proceed with Q only)
        
        # Convert to string if they are None but should be actual None for DataHandler
        # This logic is a bit tricky, DataHandler already handles None well.
        # The main point is to ensure that if a user provides a CLI arg, it's used.
        # If not, the config value is used. If config also doesn't have it, DataHandler might error or use default.

        return str(input_csv_path), q_col, a_col, qa_col, encoding


    def process(self, input_csv_path: str, 
                q_col: Optional[str] = None, 
                a_col: Optional[str] = None, 
                qa_col: Optional[str] = None, 
                encoding: Optional[str] = None) -> None:
        """
        Main processing pipeline.
        CLI args for q_col, a_col, qa_col, encoding will override config file settings.
        """
        print(f"Starting processing for: {input_csv_path}")
        
        # Resolve effective input parameters
        effective_q_col = q_col if q_col is not None else self.config.get('q_col')
        effective_a_col = a_col if a_col is not None else self.config.get('a_col')
        effective_qa_col = qa_col if qa_col is not None else self.config.get('qa_col')
        effective_encoding = encoding if encoding is not None else self.config.get('encoding', 'utf-8')

        if not os.path.isabs(input_csv_path):
            input_csv_path = os.path.join(PROJECT_ROOT, input_csv_path)

        if not os.path.exists(input_csv_path):
            print(f"Error: Input CSV file not found at {input_csv_path}")
            return

        input_filename_for_report = os.path.basename(input_csv_path)
        initial_df_info = {"total_loaded": 0, "path": input_csv_path}

        try:
            # 1. Load Data
            print("Step 1: Loading data...")
            df = self.data_handler.load_data(
                input_csv_path, 
                q_col=effective_q_col, 
                a_col=effective_a_col, 
                qa_col=effective_qa_col, 
                encoding=effective_encoding
            )
            initial_df_info["total_loaded"] = len(df)
            print(f"Successfully loaded {len(df)} rows.")
        except Exception as e:
            print(f"Error during data loading: {e}")
            report_generator = ReportGenerator(self.config, self.data_handler, input_filename_for_report)
            report_generator.generate_report(initial_df_info)
            return

        # 2. Quality Checking
        print("\nStep 2: Applying quality filters...")
        quality_checker = QualityChecker(self.config, self.data_handler)
        quality_checker.apply_filters()

        # 3. Duplication Handling
        print("\nStep 3: Processing duplicates...")
        duplication_handler = DuplicationHandler(self.config, self.data_handler)
        duplication_handler.process_duplicates()

        # 4. Save selected data
        print("\nStep 4: Saving selected data...")
        selected_df = self.data_handler.get_selected_data()
        output_csv_config = self.config.get('output_csv', {})
        output_filename = output_csv_config.get('filename', 'selected_qna_data.csv')
        
        if not selected_df.empty:
            saved_path = self.data_handler.save_data(selected_df, output_filename)
            # print(f"Selected data saved to: {saved_path}") # save_data_already_prints
        else:
            print("No data selected after filtering. Output CSV will be empty or not created.")
            # Optionally, save an empty file or skip saving
            # To ensure output_dir is created for the report even if no selected data:
            os.makedirs(os.path.join(PROJECT_ROOT, self.config.get('output_dir', 'filtered_results')), exist_ok=True)


        # 5. Generate Report
        print("\nStep 5: Generating report...")
        report_generator = ReportGenerator(self.config, self.data_handler, input_filename_for_report)
        report_generator.generate_report(initial_df_info)

        print("\nProcessing finished.")


def main_cli():
    parser = argparse.ArgumentParser(description="Filter and deduplicate Q&A text datasets from a CSV file.")
    parser.add_argument("input_csv_path", type=str, help="Path to the input CSV file.")
    parser.add_argument("--config", type=str, help="Path to a custom YAML configuration file.")
    
    # Input column arguments (override config)
    parser.add_argument("--q_col", type=str, help="Name of the question column in the CSV.")
    parser.add_argument("--a_col", type=str, help="Name of the answer column in the CSV.")
    parser.add_argument("--qa_col", type=str, help="Name of the combined question+answer column (alternative to q_col and a_col).")
    parser.add_argument("--encoding", type=str, help="Encoding of the input CSV file (e.g., 'utf-8', 'cp949').")

    # Output directory (override config)
    parser.add_argument("--output_dir", type=str, help="Directory to save filtered results and reports.")
    
    # Example of overriding a nested config (more complex to generalize fully)
    # For simplicity, we'll let MainProcessor's config loading handle CLI args as top-level overrides
    # or handle specific ones like output_dir here.
    # parser.add_argument("--semantic_threshold", type=float, help="Semantic similarity threshold for deduplication.")

    args = parser.parse_args()

    cli_provided_configs = {}
    if args.output_dir:
        cli_provided_configs['output_dir'] = args.output_dir
    # if args.semantic_threshold: # Example for nested
    #    if 'deduplication' not in cli_provided_configs: cli_provided_configs['deduplication'] = {}
    #    cli_provided_configs['deduplication']['semantic_threshold'] = args.semantic_threshold

    try:
        processor = MainProcessor(config_path=args.config, **cli_provided_configs)
        processor.process(
            input_csv_path=args.input_csv_path,
            q_col=args.q_col,
            a_col=args.a_col,
            qa_col=args.qa_col,
            encoding=args.encoding
        )
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Configuration or Input Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # For debugging, you might want to re-raise or print traceback
        # import traceback
        # traceback.print_exc()

if __name__ == "__main__":
    main_cli()