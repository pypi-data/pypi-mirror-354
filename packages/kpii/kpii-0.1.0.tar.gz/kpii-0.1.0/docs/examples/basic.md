# 기본 사용법 예제

## 텍스트에서 개인정보 탐지

```python
from kpii import KoreanPIIDetector

# 탐지기 초기화
detector = KoreanPIIDetector()

# 예제 텍스트
text = """
이름: 홍길동
주민번호: 901231-2123456
전화번호: 010-1234-5678
이메일: hong@example.com
신용카드: 9430-8212-3456-2393
"""

# 개인정보 탐지
results = detector.detect(text)

# 결과 출력
for pii_type, matches in results.items():
    print(f"{pii_type}:")
    for match in matches:
        print(f"  - {match['value']} -> {match['masked_value']}")

# 개인정보 마스킹
masked_text = detector.mask_text(text)
print("\n마스킹된 텍스트:")
print(masked_text)
```

## 특정 유형의 개인정보만 처리

```python
from kpii import KoreanPIIDetector

detector = KoreanPIIDetector()
text = "내 주민번호는 901231-2123456이고, 전화번호는 010-1234-5678입니다."

# 주민등록번호만 처리
results = detector.detect(text)
rrn_results = results['rrn']
print("주민등록번호:", [match['value'] for match in rrn_results])

# 전화번호만 처리
phone_results = results['phone']
print("전화번호:", [match['value'] for match in phone_results])
``` 