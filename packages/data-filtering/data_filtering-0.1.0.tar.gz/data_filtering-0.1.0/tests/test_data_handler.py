# tests/test_data_handler.py
import pytest
import pandas as pd
import os
import shutil # for cleaning up test outputs
from typing import List, Dict, Optional, Union

from qa_filter.data_handler import DataHandler

# 테스트용 기본 설정 (필요한 부분만)
SAMPLE_CONFIG = {
    "output_dir": "test_output/data_handler_results",
    "output_csv": {
        "filename": "test_saved_data.csv",
        "columns": ["id", "original_question", "original_answer", "processed_text_minimal"]
    },
    "q_col": "질문",
    "a_col": "답변",
    "qa_col": "QA통합"
}

# 테스트용 CSV 데이터 생성 함수
@pytest.fixture(scope="module") # 모듈 스코프로 fixture 사용
def create_test_csv_files(tmp_path_factory):
    data_dir = tmp_path_factory.mktemp("data")
    
    # 시나리오 1: q_col, a_col 사용
    csv_q_a_content = """질문,답변
"  안녕하세요?  ","  반갑습니다.  "
"질문만 있습니다.",
"""
    file_q_a = data_dir / "test_q_a.csv"
    with open(file_q_a, "w", encoding="utf-8") as f:
        f.write(csv_q_a_content)

    # 시나리오 2: qa_col 사용
    csv_qa_content = """QA통합
"  하나의 컬럼입니다.  "
"두번째 QA 통합 내용"
"""
    file_qa = data_dir / "test_qa.csv"
    with open(file_qa, "w", encoding="utf-8") as f:
        f.write(csv_qa_content)

    # 시나리오 3: q_col만 사용
    csv_q_only_content = """질문
"  질문 컬럼만 존재합니다.  "
"이것도 질문임"
"""
    file_q_only = data_dir / "test_q_only.csv"
    with open(file_q_only, "w", encoding="utf-8") as f:
        f.write(csv_q_only_content)
        
    # 시나리오 4: 잘못된 컬럼명
    csv_wrong_col_content = """잘못된질문,잘못된답변
"내용1","내용2"
"""
    file_wrong_col = data_dir / "test_wrong_col.csv"
    with open(file_wrong_col, "w", encoding="utf-8") as f:
        f.write(csv_wrong_col_content)

    return {"q_a": str(file_q_a), "qa": str(file_qa), "q_only": str(file_q_only), "wrong_col": str(file_wrong_col)}


@pytest.fixture
def data_handler():
    # 각 테스트 후 출력 디렉토리 정리
    output_dir = os.path.join(os.path.dirname(__file__), SAMPLE_CONFIG["output_dir"]) # 상대 경로로
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    return DataHandler(SAMPLE_CONFIG)

def test_load_data_q_a_cols(data_handler, create_test_csv_files):
    df = data_handler.load_data(create_test_csv_files["q_a"], q_col="질문", a_col="답변")
    assert not df.empty
    assert len(df) == 2
    assert "id" in df.columns
    assert "status" in df.columns
    assert "processed_text_minimal" in df.columns
    assert df.iloc[0]["original_question"] == "  안녕하세요?  "
    assert df.iloc[0]["processed_text_minimal"] == "안녕하세요? 반갑습니다." # 공백 제거 및 결합 확인
    assert df.iloc[1]["original_question"] == "질문만 있습니다."
    assert df.iloc[1]["original_answer"] == "" # NaN이 아닌 빈 문자열로 채워지는지 확인
    assert df.iloc[1]["processed_text_minimal"] == "질문만 있습니다."


def test_load_data_qa_col(data_handler, create_test_csv_files):
    df = data_handler.load_data(create_test_csv_files["qa"], qa_col="QA통합")
    assert not df.empty
    assert len(df) == 2
    assert df.iloc[0]["original_text_combined"] == "  하나의 컬럼입니다.  "
    assert df.iloc[0]["processed_text_minimal"] == "하나의 컬럼입니다."
    # qa_col 사용 시 original_question은 qa_col 내용, original_answer는 '' (DataHandler 로직에 따름)
    assert df.iloc[0]["original_question"] == "  하나의 컬럼입니다.  "
    assert df.iloc[0]["original_answer"] == ""

def test_load_data_q_only_col(data_handler, create_test_csv_files):
    # DataHandler는 q_col만 있는 경우를 처리 (경고 출력)
    df = data_handler.load_data(create_test_csv_files["q_only"], q_col="질문")
    assert not df.empty
    assert len(df) == 2
    assert df.iloc[0]["original_question"] == "  질문 컬럼만 존재합니다.  "
    assert df.iloc[0]["original_answer"] == ""
    assert df.iloc[0]["processed_text_minimal"] == "질문 컬럼만 존재합니다."

def test_load_data_file_not_found(data_handler):
    with pytest.raises(FileNotFoundError):
        data_handler.load_data("non_existent_file.csv", q_col="Q", a_col="A")

def test_load_data_wrong_cols(data_handler, create_test_csv_files):
    with pytest.raises(ValueError, match="Insufficient column specification"): # 에러 메시지 일부 매칭
        data_handler.load_data(create_test_csv_files["wrong_col"], q_col="질문", a_col="답변") # 없는 컬럼명

def test_preprocess_text(data_handler):
    assert data_handler._preprocess_text("  hello   world  ") == "hello world"
    assert data_handler._preprocess_text("\tmultiple  spaces\nand newlines  ") == "multiple spaces and newlines"
    assert data_handler._preprocess_text(123) == "123" # 숫자도 문자열로 변환 후 처리

def test_save_data(data_handler, create_test_csv_files):
    df_loaded = data_handler.load_data(create_test_csv_files["q_a"], q_col="질문", a_col="답변")
    
    # 임시 출력 디렉토리 생성 (DataHandler가 생성하지만, 명시적으로)
    # output_dir_path = os.path.join(os.path.dirname(__file__), SAMPLE_CONFIG["output_dir"])
    # os.makedirs(output_dir_path, exist_ok=True) # DataHandler가 처리
    
    output_filename = SAMPLE_CONFIG["output_csv"]["filename"]
    saved_path = data_handler.save_data(df_loaded, output_filename)
    
    assert os.path.exists(saved_path)
    df_saved = pd.read_csv(saved_path)
    
    # 저장된 컬럼 확인
    expected_cols = SAMPLE_CONFIG["output_csv"]["columns"]
    assert all(col in df_saved.columns for col in expected_cols)
    assert len(df_saved.columns) == len(expected_cols)
    assert len(df_saved) == len(df_loaded)

    # 테스트 후 생성된 파일/디렉토리 정리 (fixture에서 처리)

def test_update_status_and_get_data(data_handler, create_test_csv_files):
    df = data_handler.load_data(create_test_csv_files["q_a"], q_col="질문", a_col="답변")
    initial_selected_count = len(data_handler.get_selected_data())
    assert initial_selected_count == 2 # 처음엔 모두 selected

    ids_to_reject = [df.iloc[0]["id"]]
    data_handler.update_status(ids_to_reject, "rejected_test", "Test rejection")

    assert len(data_handler.get_selected_data()) == initial_selected_count - 1
    assert len(data_handler.get_rejected_data()) == 1
    rejected_item = data_handler.get_rejected_data().iloc[0]
    assert rejected_item["id"] == ids_to_reject[0]
    assert rejected_item["status"] == "rejected_test"
    assert rejected_item["rejection_reason"] == "Test rejection"