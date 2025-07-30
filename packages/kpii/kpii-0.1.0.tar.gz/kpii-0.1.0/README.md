# KPII (Korean Personal Information Identifier)

한국어 텍스트에서 개인정보를 탐지하고 마스킹 처리하는 Python 라이브러리입니다.

## 설치

```bash
pip install kpii
```

## 사용 예시

```python
from kpii import KoreanPIIDetector

# 감지기 초기화
detector = KoreanPIIDetector()

# 텍스트에서 개인정보 탐지
text = """
주민번호: 901231-2123456
전화번호: 010-1234-5678
이메일: hong@example.com
신용카드: 9430-8212-3456-2393
"""

# 모든 개인정보 마스킹
masked_text = detector.mask_text(text)

# 특정 유형만 마스킹
masked_text = detector.mask_text(text, mask_types=["rrn", "phone"])
```

## 지원하는 개인정보 유형

- 주민등록번호
- 전화번호
- 이메일
- 신용카드 번호

## 개발 환경 설정

1. 저장소 클론
```bash
git clone https://github.com/sotthang/kpii.git
cd kpii
```

2. Poetry를 사용한 의존성 설치
```bash
poetry install
```

3. 개발 의존성 설치 (테스트 도구 포함)
```bash
poetry install --with dev
```

## 테스트

### 테스트 실행

```bash
# 모든 테스트 실행
poetry run pytest

# 커버리지 리포트와 함께 테스트 실행
poetry run pytest --cov=kpii

# 특정 테스트 파일만 실행
poetry run pytest tests/test_detector.py

# 특정 테스트 함수만 실행
poetry run pytest tests/test_detector.py::test_detect_rrn
```

### 테스트 커버리지 확인

```bash
# HTML 형식의 커버리지 리포트 생성
poetry run pytest --cov=kpii --cov-report=html

# 터미널에서 커버리지 리포트 확인
poetry run pytest --cov=kpii --cov-report=term-missing
```

## 라이선스

MIT License
