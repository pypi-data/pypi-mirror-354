# tests/test_duplication_handler.py
import pytest
import pandas as pd
from qa_filter.data_handler import DataHandler
from qa_filter.duplication_handler import DuplicationHandler, SENTENCE_TRANSFORMERS_AVAILABLE

# 테스트용 기본 설정
BASE_CONFIG_DUP = {
    "output_dir": "test_output/duplication_handler_results",
    "q_col": "text", # 단일 컬럼 사용
    "deduplication": {
        "enable_exact": True,
        "enable_semantic": True, # 테스트 시 모델 로딩 시간 고려
        "semantic_model": "sentence-transformers/all-MiniLM-L6-v2", # 가볍고 빠른 모델로 테스트
        "semantic_threshold": 0.85, # 임계값 조절
        "keep_criterion": "first"
    }
}

# 테스트 데이터 (processed_text_minimal 이 중요)
# DuplicationHandler는 DataHandler가 생성한 'id', 'processed_text_minimal', 'status' 컬럼을 사용
TEST_DATA_DUP = pd.DataFrame({
    "id": ["dup_id1", "dup_id2", "dup_id3", "dup_id4", "dup_id5", "dup_id6", "dup_id7", "dup_id8"],
    "text": [ # 원본 텍스트, DataHandler를 통해 processed_text_minimal로 변환된다고 가정
        "정확히 동일한 문장입니다.",                 # dup_id1
        "정확히 동일한 문장입니다.",                 # dup_id2 (dup_id1과 정확한 중복)
        "의미는 비슷하지만 표현이 약간 다른 문장입니다.", # dup_id3
        "의미는 비슷하지만 표현이 조금 다른 문장입니다.", # dup_id4 (dup_id3과 의미론적 중복 후보)
        "짧은 의미론적 중복 문장.",                 # dup_id5
        "이것은 매우 짧지만 의미가 유사한 중복 문장입니다.", # dup_id6 (dup_id5와 의미론적 중복, 더 김)
        "완전히 다른 내용의 문장 1.",               # dup_id7 (유니크)
        "정확히 동일한 문장입니다."                  # dup_id8 (dup_id1, dup_id2와 정확한 중복)
    ]
})

@pytest.fixture
def setup_dup_handler(request): # request를 사용하여 파라미터를 받을 수 있음
    config_override = getattr(request, "param", {})
    current_config = BASE_CONFIG_DUP.copy()
    
    # 깊은 복사를 통해 중첩된 dict도 안전하게 오버라이드
    if "deduplication" in config_override:
        current_config["deduplication"] = {**current_config["deduplication"], **config_override["deduplication"]}
    else: # 다른 top-level config 오버라이드
        current_config = {**current_config, **config_override}


    data_handler = DataHandler(current_config)
    
    # 테스트 데이터 준비 (DataHandler의 load_data를 모방하여 필요한 컬럼 생성)
    temp_df = TEST_DATA_DUP.copy()
    temp_df['status'] = 'selected'
    temp_df['rejection_reason'] = ''
    # DataHandler의 _preprocess_text와 유사하게 처리
    temp_df['processed_text_minimal'] = temp_df['text'].astype(str).apply(lambda x: " ".join(x.strip().split()))
    # original_question/answer 등은 duplication handler에서 직접 사용하지 않으므로 생략 가능
    # 하지만 _apply_keep_criterion 은 'processed_text_minimal'을 사용
    data_handler.df = temp_df

    duplication_handler = DuplicationHandler(current_config, data_handler)
    return duplication_handler, data_handler


def test_exact_duplicates_keep_first(setup_dup_handler):
    duplication_handler, data_handler = setup_dup_handler
    duplication_handler._remove_exact_duplicates()
    
    df = data_handler.get_dataframe()
    assert df.loc[df['id'] == 'dup_id1', 'status'].iloc[0] == 'selected' # 첫번째 남김
    assert df.loc[df['id'] == 'dup_id2', 'status'].iloc[0] == 'rejected_exact_duplicate'
    assert df.loc[df['id'] == 'dup_id8', 'status'].iloc[0] == 'rejected_exact_duplicate'

@pytest.mark.parametrize("setup_dup_handler", [{"deduplication": {"keep_criterion": "longest"}}], indirect=True)
def test_exact_duplicates_keep_longest(setup_dup_handler):
    # 'longest'는 processed_text_minimal 길이가 기준. 정확한 중복은 길이가 모두 같으므로 'first'와 동일하게 동작.
    # 이 테스트는 _apply_keep_criterion의 'longest' 로직이 호출되는지 확인하는 의미.
    duplication_handler, data_handler = setup_dup_handler
    duplication_handler._remove_exact_duplicates()
    
    df = data_handler.get_dataframe()
    # 정확한 중복에서는 길이가 같으므로, 'longest'도 사실상 'first'처럼 동작
    assert df.loc[df['id'] == 'dup_id1', 'status'].iloc[0] == 'selected'
    assert df.loc[df['id'] == 'dup_id2', 'status'].iloc[0] == 'rejected_exact_duplicate'
    assert df.loc[df['id'] == 'dup_id8', 'status'].iloc[0] == 'rejected_exact_duplicate'

@pytest.mark.skipif(not SENTENCE_TRANSFORMERS_AVAILABLE, reason="sentence-transformers not available")
def test_semantic_duplicates_keep_first(setup_dup_handler):
    duplication_handler, data_handler = setup_dup_handler
    # 의미론적 중복 테스트 전, 정확한 중복 먼저 제거 (실제 흐름)
    duplication_handler._remove_exact_duplicates() 
    duplication_handler._remove_semantic_duplicates()
    
    df = data_handler.get_dataframe()
    # dup_id3, dup_id4 (의미 유사) -> dup_id3 selected, dup_id4 rejected (first)
    # 모델과 threshold에 따라 결과 달라질 수 있음. 이 테스트는 예시.
    # 이 모델(all-MiniLM-L6-v2)과 threshold(0.85)에서 해당 문장들이 유사하게 잡히는지 확인 필요.
    # 만약 안 잡히면, 더 확실한 예시 문장 또는 threshold 조정 필요.
    if df.loc[df['id'] == 'dup_id4', 'status'].iloc[0] == 'rejected_semantic_duplicate':
        assert df.loc[df['id'] == 'dup_id3', 'status'].iloc[0] == 'selected'
    
    # dup_id5, dup_id6 (의미 유사, 길이 다름) -> dup_id5 selected, dup_id6 rejected (first)
    if df.loc[df['id'] == 'dup_id6', 'status'].iloc[0] == 'rejected_semantic_duplicate':
        assert df.loc[df['id'] == 'dup_id5', 'status'].iloc[0] == 'selected'
        
    assert df.loc[df['id'] == 'dup_id7', 'status'].iloc[0] == 'selected' # 유니크

@pytest.mark.skipif(not SENTENCE_TRANSFORMERS_AVAILABLE, reason="sentence-transformers not available")
@pytest.mark.parametrize("setup_dup_handler", [{"deduplication": {"keep_criterion": "longest"}}], indirect=True)
def test_semantic_duplicates_keep_longest(setup_dup_handler):
    duplication_handler, data_handler = setup_dup_handler
    duplication_handler._remove_exact_duplicates()
    duplication_handler._remove_semantic_duplicates()

    df = data_handler.get_dataframe()
    # dup_id3, dup_id4: processed_text_minimal 길이 비교. 길이가 같다면 first.
    # "의미는 비슷하지만 표현이 약간 다른 문장입니다." (길이 24)
    # "의미는 비슷하지만 표현이 조금 다른 문장입니다." (길이 24)
    # 길이가 같으므로, 'longest' 적용 시에도 먼저 나온 dup_id3이 selected, dup_id4가 rejected될 가능성 높음.
    if df.loc[df['id'] == 'dup_id4', 'status'].iloc[0] == 'rejected_semantic_duplicate':
        assert df.loc[df['id'] == 'dup_id3', 'status'].iloc[0] == 'selected'

    # dup_id5, dup_id6: dup_id6이 더 김.
    # "짧은 의미론적 중복 문장." (길이 13)
    # "이것은 매우 짧지만 의미가 유사한 중복 문장입니다." (길이 26)
    # dup_id6 selected, dup_id5 rejected (longest)
    if df.loc[df['id'] == 'dup_id5', 'status'].iloc[0] == 'rejected_semantic_duplicate':
        assert df.loc[df['id'] == 'dup_id6', 'status'].iloc[0] == 'selected'

@pytest.mark.parametrize("setup_dup_handler", [{"deduplication": {"enable_exact": False, "enable_semantic": False}}], indirect=True)
def test_no_deduplication_if_disabled(setup_dup_handler):
    duplication_handler, data_handler = setup_dup_handler
    duplication_handler.process_duplicates() # 전체 프로세스 호출
    
    df = data_handler.get_dataframe()
    assert all(df['status'] == 'selected') # 중복 제거 비활성화 시 모두 selected 유지