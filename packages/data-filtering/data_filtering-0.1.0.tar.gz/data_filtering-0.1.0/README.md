# QA 데이터 필터링 및 중복 제거 라이브러리 (data_filtering)

이 라이브러리는 질문(Q)과 답변(A) 쌍으로 구성된 텍스트 데이터셋(CSV 파일)에서 중복을 확인하고, 품질 기준에 따라 데이터를 선별하는 기능을 제공합니다.

## 주요 기능

- **다양한 CSV 입력 형식 지원**:
  - 질문 컬럼과 답변 컬럼이 분리된 경우
  - 질문과 답변이 합쳐진 단일 컬럼인 경우
- **품질 필터링**:
  - 텍스트 길이 (최소/최대 길이 지정 가능, 활성화/비활성화 가능)
  - 언어 감지 (특정 언어 및 신뢰도 임계값 설정 가능, 활성화/비활성화 가능)
- **중복 제거**:
  - **정확한 중복**: 완전히 동일한 텍스트 제거
  - **의미론적 중복**: Transformer 모델을 사용하여 의미적으로 유사한 텍스트 제거 (유사도 임계값 및 모델 지정 가능)
  - 중복 발생 시 남길 기준 선택 가능 ('first': 먼저 나온 데이터, 'longest': 가장 긴 데이터)
- **결과 출력**:
  - 선별된 데이터를 새로운 CSV 파일로 저장
  - 처리 과정 및 통계를 담은 리포트 생성 (HTML 또는 TXT 형식)
- **설정**: `config/default_settings.yaml` 파일을 통해 대부분의 동작을 상세하게 설정 가능하며, CLI 인자 또는 함수 호출 시 오버라이드 가능.

## 설치 및 환경 설정

### 1. 환경 준비 (Conda 권장)

새로운 가상 환경을 생성하는 것을 권장합니다. Conda를 사용하는 경우:

```bash
conda create --name data-filtering-env python=3.11 # 예시 환경 이름 및 Python 버전
conda activate data-filtering-env
```

Python 3.11 이상을 권장합니다.

### 2. 라이브러리 설치

**방법 A: PyPI에서 설치 (배포된 경우)**

```bash
pip install data-filtering
```

(이 명령어는 라이브러리가 PyPI에 정식 배포된 후에 사용 가능합니다.)

**방법 B: 소스에서 직접 빌드 및 설치 (현재 개발/테스트 단계)**

1.  **소스 코드 다운로드 또는 클론:**

    ```bash
    git clone https://github.com/yourusername/data-filtering.git # 실제 저장소 URL로 변경
    cd data-filtering
    ```

2.  **필수 빌드 도구 설치:**

    ```bash
    pip install build
    ```

3.  **패키지 빌드:**
    프로젝트 루트 디렉토리에서 다음 명령을 실행합니다.

    ```bash
    python -m build
    ```

    이 명령은 `dist` 디렉토리에 `.whl` 파일과 `.tar.gz` 파일을 생성합니다.

4.  **빌드된 패키지 설치:**
    생성된 `.whl` 파일을 사용하여 설치합니다.
    ```bash
    pip install dist/data_filtering-0.1.0-py3-none-any.whl # 실제 생성된 파일명으로 변경
    ```
    또는, 개발 중에는 editable 모드로 설치할 수 있습니다:
    ```bash
    pip install -e .
    ```

### 3. 의존성 패키지 확인 및 설치

`data-filtering` 패키지는 필요한 의존성을 자동으로 함께 설치하려고 시도합니다. 주요 의존성은 `pyproject.toml` 파일의 `dependencies` 섹션에 명시되어 있습니다.

**참고 (PyTorch):**
의미론적 중복 제거 기능은 `sentence-transformers` 라이브러리를 사용하며, 이는 PyTorch에 의존합니다. 대부분의 경우 CPU 버전의 PyTorch가 함께 설치됩니다. GPU 환경이나 특정 버전의 PyTorch가 필요하다면, `data-filtering` 설치 전에 [PyTorch 공식 웹사이트](https://pytorch.org/get-started/locally/)를 참고하여 해당 환경에 맞는 PyTorch를 먼저 설치하는 것이 좋습니다.

## 사용 방법

라이브러리는 두 가지 주요 방식으로 사용할 수 있습니다: 명령줄 인터페이스(CLI) 또는 Python 코드 내에서 직접 호출.

### 1. 명령줄 인터페이스 (CLI) 사용

패키지가 올바르게 설치되었다면, 터미널에서 `data-filtering-cli` 명령어를 사용할 수 있습니다.

**기본 사용법:**

```bash
data-filtering-cli <입력_CSV_파일_경로>
```

예시:

```bash
data-filtering-cli examples/sample_data.csv
```

**주요 옵션:**

- `--config <설정_파일_경로>`: 사용자 정의 YAML 설정 파일을 지정합니다. (기본값: `config/default_settings.yaml`)
- `--q_col <컬럼명>`: CSV 파일 내 질문 컬럼명을 지정합니다. (설정 파일 값 오버라이드)
- `--a_col <컬럼명>`: CSV 파일 내 답변 컬럼명을 지정합니다. (설정 파일 값 오버라이드)
- `--qa_col <컬럼명>`: CSV 파일 내 질문+답변 통합 컬럼명을 지정합니다. (`q_col`, `a_col` 대신 사용)
- `--encoding <인코딩>`: 입력 CSV 파일의 인코딩을 지정합니다. (예: `utf-8`, `cp949`)
- `--output_dir <경로>`: 결과 파일(선별된 CSV, 리포트)이 저장될 디렉토리를 지정합니다.

**CLI 예시:**

```bash
# 사용자 설정 파일과 함께 실행
data-filtering-cli data/my_qna_data.csv --config config/my_custom_settings.yaml

# 질문/답변 컬럼명 직접 지정 및 출력 디렉토리 변경
data-filtering-cli data/another_data.csv --q_col "Question" --a_col "Answer" --output_dir processed_results
```

(만약 `data-filtering-cli` 명령어가 인식되지 않는다면, Python 환경의 `bin` 또는 `Scripts` 디렉토리가 시스템 PATH에 올바르게 추가되었는지, 또는 `python -m data_filtering.main_processor <입력_CSV_파일_경로>` 형태로 직접 모듈을 실행해야 할 수 있습니다.)

### 2. Python 코드에서 라이브러리로 사용

`data_filtering` 모듈의 `run` 함수를 사용하여 Python 스크립트 내에서 필터링 프로세스를 실행할 수 있습니다.

```python
from data_filtering import run

# 기본 설정 사용 (패키지 내부의 default_settings.yaml 사용)
run(input_csv_path="examples/sample_data.csv")

# 사용자 정의 설정 파일 및 일부 옵션 kwargs로 오버라이드
run(
    input_csv_path="data/my_qna_data.csv",
    config_path="path/to/my_custom_settings.yaml", # 사용자 YAML 파일 경로
    output_dir="custom_output", # kwargs로 최상위 설정 오버라이드
    deduplication={"semantic_threshold": 0.88} # kwargs로 중첩된 설정 오버라이드
)

# 컬럼명 직접 지정 (config 파일 설정보다 우선)
run(
    input_csv_path="data/other_format.csv",
    q_col="Inquiry",
    a_col="Response"
)
```

## 설정 (`config/default_settings.yaml`)

라이브러리의 세부 동작은 `config/default_settings.yaml` 파일을 통해 제어됩니다. 주요 설정 항목은 다음과 같습니다:

- **입력 컬럼명 및 인코딩**: `q_col`, `a_col`, `qa_col`, `encoding`
- **출력 디렉토리**: `output_dir`
- **중복 제거 설정 (`deduplication`)**:
  - 정확/의미론적 중복 제거 활성화 여부 (`enable_exact`, `enable_semantic`)
  - Sentence Transformer 모델명 또는 로컬 경로 (`semantic_model`)
  - 의미론적 유사도 임계값 (`semantic_threshold`)
  - 중복 시 남길 기준 (`keep_criterion`)
- **품질 필터 설정 (`quality_filters`)**:
  - 길이 필터 (`length`): 활성화 여부 (`enable`), 최소/최대 길이 (`min`, `max`)
  - 언어 필터 (`language`): 활성화 여부 (`enable`), 목표 언어 (`target`), 신뢰도 임계값 (`confidence_threshold`)
- **리포트 설정 (`report`)**:
  - 리포트 형식 (`format`: `html` 또는 `txt`)
  - 리포트 파일명 (`filename`)
  - 리포트에 포함할 거부된 샘플 수 (`include_rejected_samples`)
- **출력 CSV 설정 (`output_csv`)**:
  - 선별된 데이터 CSV 파일명 (`filename`)
  - 최종 CSV에 포함될 컬럼 목록 (`columns`)

사용자 정의 설정을 원할 경우, `default_settings.yaml` 파일을 복사하여 수정 후 `--config` 옵션이나 `run` 함수의 `config_path` 인자로 지정하여 사용하십시오.

## 디렉토리 구조

```
.
├── data_filtering/          # 라이브러리 소스 코드 패키지
│   ├── config/              # 기본 설정 파일 디렉토리
│   │   └── default_settings.yaml
│   ├── templates/           # HTML 리포트 템플릿
│   │   └── report_template.html
│   ├── __init__.py
│   ├── data_handler.py
│   ├── duplication_handler.py
│   ├── main_processor.py    # CLI 진입점 및 핵심 로직
│   ├── quality_checker.py
│   └── report_generator.py
├── examples/                # 예제 스크립트 및 데이터
│   ├── run_example.py       # 라이브러리 사용 예시 Python 스크립트
│   └── sample_data.csv
├── tests/                   # 테스트 코드
│   ├── pytest.ini           # Pytest 설정 (PYTHONPATH 등)
│   └── ... (각 모듈별 테스트 파일) ...
├── MANIFEST.in              # 패키지에 포함할 비-Python 파일 목록
├── pyproject.toml           # 빌드 시스템, 프로젝트 메타데이터, 의존성 명시
├── README.md                # 현재 파일
├── requirements.txt         # 개발 환경용 의존성 목록 (선택적)
└── setup.py                 # Setuptools 설정 파일
```

## 테스트 실행

프로젝트의 기능을 검증하기 위해 `pytest`를 사용합니다.

1.  Conda 환경(`data_filtering-env`)을 활성화합니다.
2.  프로젝트 루트 디렉토리에서 다음 명령을 실행합니다:

    ```bash
    pytest
    ```

**주요 업데이트 사항:**

- 라이브러리 이름을 `qa-filter`에서 `data-filtering`으로 일괄 변경했습니다.
- 설치 방법을 PyPI에서 설치하는 방법(배포 후)과 소스에서 직접 빌드 및 설치하는 방법으로 나누어 설명했습니다.
- `requirements.txt`의 역할을 개발 환경용으로 명확히 하고, 패키지 의존성은 `pyproject.toml`에서 관리됨을 암시했습니다.
- CLI 명령어 이름을 `data-filtering-cli`로 변경했습니다.
- 설정 파일(`default_settings.yaml`)이 패키지 내부(`data_filtering/config/`)에 포함됨을 명시하고, 사용자가 설정을 변경하는 방법을 더 자세히 설명했습니다.
- 디렉토리 구조에서 `config` 폴더의 위치를 `data_filtering` 패키지 내부로 수정했습니다.
