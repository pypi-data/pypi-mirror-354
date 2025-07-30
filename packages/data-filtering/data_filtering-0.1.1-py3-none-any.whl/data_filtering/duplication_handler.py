# qa_filter/duplication_handler.py

import pandas as pd
from typing import Dict, List, Set
from .data_handler import DataHandler

# Semantic Duplication Handling (optional imports)
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTINEL = object() # Placeholder for SentenceTransformer type hint if not available
    SentenceTransformer = SENTINEL # type: ignore
    cosine_similarity = SENTINEL # type: ignore
    np = SENTINEL # type: ignore
    SENTENCE_TRANSFORMERS_AVAILABLE = False


class DuplicationHandler:
    def __init__(self, config: Dict, data_handler: DataHandler):
        self.config = config
        self.data_handler = data_handler
        self.dedup_config = self.config.get('deduplication', {})
        self.model: SentenceTransformer = None # type: ignore

        if self.dedup_config.get('enable_semantic', False) and SENTENCE_TRANSFORMERS_AVAILABLE:
            model_name_or_path = self.dedup_config.get('semantic_model')
            if model_name_or_path:
                try:
                    # model_name_or_path가 로컬 경로인지 Hugging Face 모델명인지 라이브러리가 자동으로 판단합니다.
                    # 로컬 경로인 경우 해당 경로에 모델 파일들이 존재해야 합니다.
                    # (예: pytorch_model.bin, config.json, tokenizer_config.json 등)
                    print(f"Loading sentence transformer model from: {model_name_or_path}...")
                    # 선택적: 로컬 경로일 경우 존재 여부 확인 (필수는 아님, SentenceTransformer가 내부적으로 처리)
                    # if os.path.isdir(model_name_or_path):
                    #     print(f"Attempting to load from local path: {model_name_or_path}")
                    # else:
                    #     print(f"Attempting to load from Hugging Face Hub or cache: {model_name_or_path}")
                    
                    self.model = SentenceTransformer(model_name_or_path)
                    print("Model loaded successfully.")
                except Exception as e:
                    print(f"Warning: Could not load sentence transformer model '{model_name_or_path}'. "
                          f"Ensure it's a valid Hugging Face model name or a path to a downloaded model directory. "
                          f"Semantic deduplication might not work. Error: {e}")
                    self.model = None
            else:
                print("Warning: Semantic deduplication enabled but no model specified in config.")
        elif self.dedup_config.get('enable_semantic', False) and not SENTENCE_TRANSFORMERS_AVAILABLE:
            print("Warning: Semantic deduplication enabled, but 'sentence-transformers' or 'scikit-learn' not installed. "
                  "Skipping semantic deduplication.")


    def process_duplicates(self) -> None:
        """Processes duplicates based on configuration."""
        df = self.data_handler.get_dataframe()
        if df is None or df.empty:
            print("DataFrame not loaded or empty. Skipping duplication processing.")
            return

        print("Processing duplicates...")
        if self.dedup_config.get('enable_exact', False):
            self._remove_exact_duplicates()

        if self.dedup_config.get('enable_semantic', False) and self.model and SENTENCE_TRANSFORMERS_AVAILABLE:
            self._remove_semantic_duplicates()
        elif self.dedup_config.get('enable_semantic', False):
            print("Semantic deduplication was enabled but could not proceed (model not loaded or libraries missing).")
        
        print("Duplication processing complete.")

    def _apply_keep_criterion(self, duplicate_group_df: pd.DataFrame, criterion: str) -> str:
        """
        Applies the keep criterion to a group of duplicates and returns the ID of the item to keep.
        Assumes duplicate_group_df contains 'id' and 'processed_text_minimal' columns.
        The DataFrame should be sorted by original order if 'first' is relevant.
        """
        if duplicate_group_df.empty:
            raise ValueError("Duplicate group DataFrame cannot be empty.")

        if criterion == 'longest':
            # Add length, then sort by length (desc) and then by original index (asc) to break ties
            # Original index is implicit in a pre-sorted DataFrame passed to this function.
            # Here, we assume the df is passed with original order preserved when 'first' is a tie-breaker.
            # For simplicity, if lengths are equal, the one appearing first in the group_df is chosen.
            # A more robust 'first' tie-breaker would need original index tracking.
            # However, pandas groupby preserves order of appearance within groups by default.
            duplicate_group_df = duplicate_group_df.copy() # Avoid SettingWithCopyWarning
            duplicate_group_df['text_length'] = duplicate_group_df['processed_text_minimal'].astype(str).str.len()
            item_to_keep_id = duplicate_group_df.loc[duplicate_group_df['text_length'].idxmax()]['id']
        elif criterion == 'first':
            item_to_keep_id = duplicate_group_df.iloc[0]['id'] # Keep the first item in the group
        else: # Default to 'first' if criterion is unknown
            print(f"Warning: Unknown keep_criterion '{criterion}'. Defaulting to 'first'.")
            item_to_keep_id = duplicate_group_df.iloc[0]['id']
        
        return str(item_to_keep_id)


    def _remove_exact_duplicates(self) -> None:
        print("Removing exact duplicates...")
        df = self.data_handler.get_dataframe()
        if df is None: return

        # Process only 'selected' items
        # Create a copy to avoid issues with chained indexing if df is a slice
        selected_df = df[df['status'] == 'selected'].copy() 
        
        if selected_df.empty:
            print("No items in 'selected' status to check for exact duplicates.")
            return

        # 'processed_text_minimal' is the target for deduplication
        # Pandas duplicated() keeps 'first' by default. We need to implement 'longest' or other criteria.
        
        duplicated_ids_to_reject = []
        criterion = self.dedup_config.get('keep_criterion', 'first')

        # Group by the text to find duplicates
        # Important: groupby preserves the order of rows within each group as they appeared in the original DataFrame.
        for _, group in selected_df.groupby('processed_text_minimal', sort=False):
            if len(group) > 1: # If there's more than one item in the group, it's a duplicate set
                item_to_keep_id = self._apply_keep_criterion(group, criterion)
                
                # IDs to reject are all IDs in the group except the one to keep
                for id_val in group['id']:
                    if str(id_val) != item_to_keep_id:
                        duplicated_ids_to_reject.append(str(id_val))
        
        if duplicated_ids_to_reject:
            reason = f"Exact duplicate (kept item by criterion: {criterion})"
            self.data_handler.update_status(duplicated_ids_to_reject, 'rejected_exact_duplicate', reason)
            print(f"Marked {len(duplicated_ids_to_reject)} items as exact duplicates.")
        else:
            print("No exact duplicates found among selected items.")


    def _remove_semantic_duplicates(self) -> None:
        if not self.model or not SENTENCE_TRANSFORMERS_AVAILABLE:
            print("Semantic model not available or 'sentence-transformers'/'scikit-learn' not installed. Skipping semantic deduplication.")
            return

        print("Removing semantic duplicates...")
        df = self.data_handler.get_dataframe()
        if df is None: return

        # Process only 'selected' items.
        # Make a copy to ensure we are working with up-to-date data and avoid SettingWithCopyWarning
        selected_df = df[df['status'] == 'selected'].copy()

        if selected_df.empty or len(selected_df) < 2:
            print("Not enough 'selected' items to check for semantic duplicates.")
            return

        texts = selected_df['processed_text_minimal'].tolist()
        
        # Handle potential empty strings if not filtered out by length filter.
        # SBERT models might error on empty strings.
        valid_texts_indices = [i for i, t in enumerate(texts) if isinstance(t, str) and len(t.strip()) > 0]
        if not valid_texts_indices:
            print("No valid texts found for semantic encoding among selected items.")
            return
        
        valid_texts = [texts[i] for i in valid_texts_indices]
        original_ids_for_valid_texts = selected_df.iloc[valid_texts_indices]['id'].tolist()

        print(f"Encoding {len(valid_texts)} texts for semantic comparison...")
        try:
            embeddings = self.model.encode(valid_texts, show_progress_bar=False, convert_to_tensor=False)
        except Exception as e:
            print(f"Error during sentence embedding: {e}. Skipping semantic deduplication.")
            return
            
        if not isinstance(embeddings, np.ndarray) or embeddings.ndim != 2:
            print(f"Error: Embeddings are not in the expected format (numpy ndarray, 2D). Got type: {type(embeddings)}. Skipping.")
            return


        print("Calculating similarity matrix...")
        # Calculate cosine similarity. Ensure embeddings are normalized for dot product to be cosine sim,
        # or use sklearn.metrics.pairwise.cosine_similarity
        # SentenceTransformer models usually output normalized embeddings, but cosine_similarity is safer.
        similarity_matrix = cosine_similarity(embeddings)

        threshold = self.dedup_config.get('semantic_threshold', 0.9)
        criterion = self.dedup_config.get('keep_criterion', 'first')
        
        # Find duplicate pairs/groups
        # This is a common approach: iterate through the upper triangle of the similarity matrix
        # Keep track of items already processed or marked for keeping/rejection to avoid redundant checks
        
        # Store ids that are part of any duplicate cluster
        # key: id of item to keep, value: set of ids to reject for this cluster
        duplicate_clusters: Dict[str, Set[str]] = {}
        # Set of all ids that have been decided (either to keep or reject)
        processed_ids: Set[str] = set() 
        ids_to_reject_overall: Set[str] = set()

        num_valid_texts = len(valid_texts)
        for i in range(num_valid_texts):
            if original_ids_for_valid_texts[i] in processed_ids:
                continue

            current_item_id = original_ids_for_valid_texts[i]
            current_item_text = valid_texts[i]
            
            # Collect all items semantically similar to current_item_id
            # The group includes the current item itself initially
            similar_items_indices = [i] 
            for j in range(i + 1, num_valid_texts):
                if original_ids_for_valid_texts[j] in processed_ids: # Already part of another cluster and decided
                    continue
                if similarity_matrix[i, j] >= threshold:
                    similar_items_indices.append(j)
            
            if len(similar_items_indices) > 1: # Found a semantic cluster
                # Create a temporary DataFrame for this cluster to apply keep_criterion
                cluster_data = []
                for idx in similar_items_indices:
                    cluster_data.append({
                        'id': original_ids_for_valid_texts[idx],
                        'processed_text_minimal': valid_texts[idx]
                        # Add original index if needed for 'first' criterion robustly,
                        # but selected_df.iloc[valid_texts_indices] might already be in order.
                    })
                
                cluster_df = pd.DataFrame(cluster_data)
                
                # Ensure the order for 'first' criterion is based on original_ids_for_valid_texts order
                # which comes from selected_df.iloc[valid_texts_indices]
                # This requires careful handling if cluster_df is reordered.
                # For simplicity, assume cluster_df created from similar_items_indices (which are sorted)
                # maintains the 'first' notion relative to this group.
                
                item_to_keep_in_cluster_id = self._apply_keep_criterion(cluster_df, criterion)
                
                for item_id_in_cluster in cluster_df['id']:
                    processed_ids.add(item_id_in_cluster) # Mark all items in this cluster as processed
                    if item_id_in_cluster != item_to_keep_in_cluster_id:
                        ids_to_reject_overall.add(item_id_in_cluster)
            else:
                # Item i is not similar to any subsequent items (above threshold)
                # And it hasn't been clustered with a previous item. So it's unique in this context.
                processed_ids.add(current_item_id)


        if ids_to_reject_overall:
            reason = f"Semantic duplicate (threshold: {threshold}, kept by: {criterion})"
            # Convert set to list for DataHandler
            self.data_handler.update_status(list(ids_to_reject_overall), 'rejected_semantic_duplicate', reason)
            print(f"Marked {len(ids_to_reject_overall)} items as semantic duplicates.")
        else:
            print("No semantic duplicates found among selected items meeting the threshold.")