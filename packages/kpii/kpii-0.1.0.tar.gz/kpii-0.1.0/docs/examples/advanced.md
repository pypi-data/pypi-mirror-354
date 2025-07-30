# 고급 사용법 예제

## 여러 텍스트 처리

```python
from kpii import KoreanPIIDetector

detector = KoreanPIIDetector()

# 여러 텍스트 처리
texts = [
    "주민번호: 901231-2123456",
    "전화번호: 010-1234-5678",
    "이메일: hong@example.com"
]

# 각 텍스트에서 개인정보 탐지
for text in texts:
    results = detector.detect(text)
    print(f"\n텍스트: {text}")
    for pii_type, matches in results.items():
        if matches:
            print(f"{pii_type}: {[match['value'] for match in matches]}")

# 여러 텍스트 마스킹
masked_texts = [detector.mask_text(text) for text in texts]
for original, masked in zip(texts, masked_texts):
    print(f"\n원본: {original}")
    print(f"마스킹: {masked}")
```

## 결과 필터링

```python
from kpii import KoreanPIIDetector

detector = KoreanPIIDetector()
text = "주민번호: 901231-2123456, 전화번호: 010-1234-5678"

# 개인정보 탐지
results = detector.detect(text)

# 특정 유형의 개인정보만 필터링
phone_numbers = results['phone']
print("전화번호:", [match['value'] for match in phone_numbers])

# 특정 패턴과 일치하는 결과만 필터링
rrn_matches = results['rrn']
print("주민등록번호:", [match['value'] for match in rrn_matches])
```

## 개인정보 마스킹

```python
from kpii import KoreanPIIDetector

detector = KoreanPIIDetector()

# 개인정보가 포함된 텍스트
text = """
이름: 홍길동
주민번호: 901231-2123456
전화번호: 010-1234-5678
이메일: hong@example.com
신용카드: 9430-8212-3456-2393
"""

# 전체 텍스트 마스킹
masked_text = detector.mask_text(text)
print("마스킹된 텍스트:")
print(masked_text)

# 개인정보 탐지 후 선택적 마스킹
results = detector.detect(text)
for pii_type, matches in results.items():
    print(f"\n{pii_type}:")
    for match in matches:
        print(f"  원본: {match['value']}")
        print(f"  마스킹: {match['masked_value']}")
``` 