# tests/test_quality_checker.py
import pytest
import pandas as pd
from qa_filter.data_handler import DataHandler
from qa_filter.quality_checker import QualityChecker

# 테스트용 기본 설정
BASE_CONFIG = {
    "output_dir": "test_output/quality_checker_results",
    "q_col": "text", # 간단한 테스트를 위해 단일 컬럼 사용
    "quality_filters": {
        "length": {
            "enable": True,
            "min": 5,
            "max": 20
        },
        "language": {
            "enable": True,
            "target": "ko",
            "confidence_threshold": 0.7
        }
    }
}

# 테스트 데이터
TEST_DATA = pd.DataFrame({
    "id": ["id1", "id2", "id3", "id4", "id5", "id6", "id7", "id8"],
    "text": [
        "짧음",                            # 길이 미달 (min:5)
        "적당한 길이의 한국어 문장입니다.",     # 통과
        "This is an English sentence.",    # 언어 불일치 (target:ko)
        "매우 긴 한국어 문장입니다. 이 문장은 최대 길이를 초과합니다.", # 길이 초과 (max:20)
        "これも日本語の文章です。",          # 언어 불일치
        "   앞뒤 공백 많은 한국어   ",     # 공백 제거 후 길이/언어 통과
        "123",                             # 짧고, 언어 감지 어려움
        ""                                 # 빈 문자열
    ],
    "status": "selected", # 초기 상태
    "rejection_reason": ""
})
# DataHandler의 _preprocess_text를 모방하거나, 실제 DataHandler를 통해 processed_text_minimal 생성
TEST_DATA['processed_text_minimal'] = TEST_DATA['text'].astype(str).apply(lambda x: " ".join(x.strip().split()))


@pytest.fixture
def setup_qc(request): # request를 사용하여 파라미터를 받을 수 있음
    config_override = getattr(request, "param", {}) # parametrize로부터 받은 값
    current_config = BASE_CONFIG.copy()
    # 기본 설정에 override 적용 (깊은 복사 필요 시 주의)
    if "quality_filters" in config_override:
        current_config["quality_filters"] = {**current_config["quality_filters"], **config_override["quality_filters"]}
    else:
        current_config = {**current_config, **config_override}


    data_handler = DataHandler(current_config)
    # DataHandler의 DataFrame을 테스트 데이터로 설정
    data_handler.df = TEST_DATA.copy() # 원본 TEST_DATA 변경 방지
    
    quality_checker = QualityChecker(current_config, data_handler)
    return quality_checker, data_handler


def test_length_filter_enabled(setup_qc):
    quality_checker, data_handler = setup_qc
    quality_checker._filter_by_length() # 직접 호출하여 테스트
    
    df = data_handler.get_dataframe()
    assert df.loc[df['id'] == 'id1', 'status'].iloc[0] == 'rejected_length'
    assert df.loc[df['id'] == 'id1', 'rejection_reason'].iloc[0] == 'Too short (min: 5 chars)'
    assert df.loc[df['id'] == 'id4', 'status'].iloc[0] == 'rejected_length'
    assert df.loc[df['id'] == 'id4', 'rejection_reason'].iloc[0] == 'Too long (max: 20 chars)'
    assert df.loc[df['id'] == 'id7', 'status'].iloc[0] == 'rejected_length' # "123"
    assert df.loc[df['id'] == 'id8', 'status'].iloc[0] == 'rejected_length' # ""
    assert df.loc[df['id'] == 'id2', 'status'].iloc[0] == 'selected'
    assert df.loc[df['id'] == 'id6', 'status'].iloc[0] == 'selected' # "앞뒤 공백 많은 한국어" -> 길이 9로 통과

@pytest.mark.parametrize("setup_qc", [{"quality_filters": {"length": {"enable": False}}}], indirect=True)
def test_length_filter_disabled(setup_qc):
    quality_checker, data_handler = setup_qc
    quality_checker._filter_by_length()
    
    df = data_handler.get_dataframe()
    # 필터 비활성화 시 모든 상태가 'selected'로 유지되어야 함 (길이 필터에 한해서)
    assert all(df['status'] == 'selected')

def test_language_filter_enabled(setup_qc):
    quality_checker, data_handler = setup_qc
    
    # 이 테스트는 setup_qc fixture가 기본 BASE_CONFIG (language.enable: True)를 사용합니다.
    # setup_qc fixture의 로직:
    # config_override = getattr(request, "param", {})
    # request.param이 없으면 config_override는 {}가 되고, BASE_CONFIG가 그대로 사용됩니다.

    # 언어 필터 전, 길이 필터로 짧은 것들 먼저 제외 (실제 흐름 모방)
    quality_checker._filter_by_length()
    quality_checker._filter_by_language() # 여기서는 언어 필터가 활성화되어야 함

    df = data_handler.get_dataframe()
    # id3는 길이(max:20)에 먼저 걸림: "This is an English sentence." (길이 28)
    assert df.loc[df['id'] == 'id3', 'status'].iloc[0] == 'rejected_length'
    # "これも日本語の文章です。" (길이 13, 길이 통과, 언어 불일치) -> language.enable: True이므로 reject 되어야 함
    assert df.loc[df['id'] == 'id5', 'status'].iloc[0] == 'rejected_language' # 이 부분이 이전 실패 지점
    assert df.loc[df['id'] == 'id2', 'status'].iloc[0] == 'selected'
    assert df.loc[df['id'] == 'id6', 'status'].iloc[0] == 'selected'

@pytest.mark.parametrize("setup_qc", [{"quality_filters": {"language": {"enable": False}}}], indirect=True)
def test_language_filter_disabled(setup_qc): # 이 함수는 언어 필터 비활성화 케이스 담당
    quality_checker, data_handler = setup_qc
    quality_checker._filter_by_language()

    df = data_handler.get_dataframe()
    # 필터 비활성화 시 모든 상태가 'selected'로 유지되어야 함 (언어 필터에 한해서)
    assert all(df.loc[~df['id'].isin(['id1', 'id4', 'id7', 'id8']), 'status'] == 'selected') # 길이 필터에 걸린 건 제외

def test_apply_filters_all_enabled(setup_qc):
    quality_checker, data_handler = setup_qc
    quality_checker.apply_filters() # 전체 필터 적용

    df = data_handler.get_dataframe()
    # 예상 결과 종합
    assert df.loc[df['id'] == 'id1', 'status'].iloc[0] == 'rejected_length'
    assert df.loc[df['id'] == 'id2', 'status'].iloc[0] == 'selected'
    # id3는 길이(max:20)에 먼저 걸림: "This is an English sentence." (길이 28)
    assert df.loc[df['id'] == 'id3', 'status'].iloc[0] == 'rejected_length'
    assert df.loc[df['id'] == 'id4', 'status'].iloc[0] == 'rejected_length'
    # id5는 길이 통과("これも日本語の文章です。", 길이 13), 언어에서 걸림
    assert df.loc[df['id'] == 'id5', 'status'].iloc[0] == 'rejected_language'
    assert df.loc[df['id'] == 'id6', 'status'].iloc[0] == 'selected'
    assert df.loc[df['id'] == 'id7', 'status'].iloc[0] == 'rejected_length' # 길이 먼저
    assert df.loc[df['id'] == 'id8', 'status'].iloc[0] == 'rejected_length'
