# KPII

한국어 개인정보 탐지 패키지입니다.

## 주요 기능

- 주민등록번호 탐지
- 전화번호 탐지
- 이메일 주소 탐지
- 신용카드 번호 탐지

## 빠른 시작

```python
from kpii import KoreanPIIDetector

# 탐지기 초기화
detector = KoreanPIIDetector()

# 텍스트에서 개인정보 탐지
text = "내 주민번호는 123456-1234567이고, 전화번호는 010-1234-5678입니다."
results = detector.detect(text)
print(results)

# 개인정보 마스킹
masked_text = detector.mask_text(text)
print(masked_text)
```

## 설치

```bash
pip install kpii
```

## 라이선스

MIT License 