# 사용법

## 기본 사용법

```python
from kpii import KoreanPIIDetector

# 탐지기 초기화
detector = KoreanPIIDetector()

# 텍스트에서 개인정보 탐지
text = "내 주민번호는 901231-2123456이고, 전화번호는 010-1234-5678입니다."
results = detector.detect(text)

# 결과 출력
for pii_type, matches in results.items():
    print(f"{pii_type}: {matches}")

# 개인정보 마스킹
masked_text = detector.mask_text(text)
print(masked_text)
```

## 탐지 가능한 개인정보 유형

- `rrn`: 주민등록번호
- `phone`: 전화번호
- `email`: 이메일 주소
- `credit_card`: 신용카드 번호

## detect() 결과 형식

```python
{
    'rrn': [{
        'type': '주민등록번호',
        'value': '901231-2123456',
        'masked_value': '901231-2******',
        'start': 10,
        'end': 24
    }],
    'phone': [{
        'type': '전화번호',
        'value': '010-1234-5678',
        'masked_value': '010-1234-****',
        'start': 30,
        'end': 43
    }],
    'email': [],
    'credit_card': []
}
```

## mask_text() 결과 형식

```python
# 입력 텍스트
"내 주민번호는 901231-2123456이고, 전화번호는 010-1234-5678입니다."

# 출력 텍스트
"내 주민번호는 901231-2******이고, 전화번호는 010-1234-****입니다."
```

## 마스킹 규칙

```
- 주민등록번호: 뒤에서부터 6자리 마스킹 (예: 901231-2******)
- 전화번호: 뒤 4자리 마스킹 (예: 010-1234-****)
- 이메일: 이름의 첫 번째 글자만 표시 (예: h***@example.com)
- 신용카드: 7번째부터 12번째 자리 마스킹 (예: 9430-82**-****-2393)
```

## 고급 사용법

특정 유형의 개인정보만 처리하려면:

```python
from kpii import KoreanPIIDetector

detector = KoreanPIIDetector()
text = "내 주민번호는 901231-2123456이고, 전화번호는 010-1234-5678입니다."

# 주민번호만 탐지
results = detector.detect(text, mask_types=["rrn"])
print(results)  # {'rrn': [...], 'phone': [], 'email': [], 'credit_card': []}

# 주민번호만 마스킹
masked_text = detector.mask_text(text, mask_types=["rrn"])
print(masked_text)  # "내 주민번호는 901231-2******이고, 전화번호는 010-1234-5678입니다."
``` 