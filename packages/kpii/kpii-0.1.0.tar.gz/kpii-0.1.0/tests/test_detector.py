import pytest
from kpii import KoreanPIIDetector


@pytest.fixture
def detector():
    return KoreanPIIDetector()


def test_detect_rrn(detector):
    text = "주민등록번호: 901231-2123456"
    results = detector.detect(text, mask_types=["rrn"])
    assert "rrn" in results
    assert len(results["rrn"]) == 1
    assert results["rrn"][0]["value"] == "901231-2123456"
    assert results["rrn"][0]["masked_value"] == "901231-2******"
    assert results["rrn"][0]["type"] == "주민등록번호"
    assert "start" in results["rrn"][0]
    assert "end" in results["rrn"][0]
    assert "phone" not in results
    assert "email" not in results
    assert "credit_card" not in results


def test_detect_phone(detector):
    text = "전화번호: 010-1234-5678"
    results = detector.detect(text, mask_types=["phone"])
    assert "phone" in results
    assert len(results["phone"]) == 1
    assert results["phone"][0]["value"] == "010-1234-5678"
    assert results["phone"][0]["masked_value"] == "010-1234-****"
    assert results["phone"][0]["type"] == "전화번호"
    assert "start" in results["phone"][0]
    assert "end" in results["phone"][0]
    assert "rrn" not in results
    assert "email" not in results
    assert "credit_card" not in results


def test_detect_email(detector):
    text = "이메일: hong@example.com"
    results = detector.detect(text, mask_types=["email"])
    assert "email" in results
    assert len(results["email"]) == 1
    assert results["email"][0]["value"] == "hong@example.com"
    assert results["email"][0]["masked_value"] == "h***@example.com"
    assert results["email"][0]["type"] == "이메일"
    assert "start" in results["email"][0]
    assert "end" in results["email"][0]
    assert "rrn" not in results
    assert "phone" not in results
    assert "credit_card" not in results


def test_detect_credit_card(detector):
    text = "신용카드: 9430-8212-3456-2393"
    results = detector.detect(text, mask_types=["credit_card"])
    assert "credit_card" in results
    assert len(results["credit_card"]) == 1
    assert results["credit_card"][0]["value"] == "9430-8212-3456-2393"
    assert results["credit_card"][0]["masked_value"] == "9430-82**-****-2393"
    assert results["credit_card"][0]["type"] == "신용카드"
    assert "start" in results["credit_card"][0]
    assert "end" in results["credit_card"][0]
    assert "rrn" not in results
    assert "phone" not in results
    assert "email" not in results


def test_mask_text(detector):
    text = """
    주민번호: 901231-2123456
    전화번호: 010-1234-5678
    이메일: hong@example.com
    신용카드: 9430-8212-3456-2393
    """
    masked_text = detector.mask_text(text)
    assert "901231-2******" in masked_text
    assert "010-1234-****" in masked_text
    assert "h***@example.com" in masked_text
    assert "9430-82**-****-2393" in masked_text


def test_mask_text_with_types(detector):
    text = """
    주민번호: 901231-2123456
    전화번호: 010-1234-5678
    이메일: hong@example.com
    신용카드: 9430-8212-3456-2393
    """
    masked_text = detector.mask_text(text, mask_types=["rrn", "phone"])
    assert "901231-2******" in masked_text
    assert "010-1234-****" in masked_text
    assert "hong@example.com" in masked_text  # 마스킹되지 않음
    assert "9430-8212-3456-2393" in masked_text  # 마스킹되지 않음


def test_multiple_detections(detector):
    text = "주민등록번호: 901231-2123456, 전화번호: 010-1234-5678"
    results = detector.detect(text, mask_types=["rrn", "phone"])
    assert len(results["rrn"]) == 1
    assert len(results["phone"]) == 1
    assert "email" not in results
    assert "credit_card" not in results


def test_invalid_mask_type(detector):
    text = "주민등록번호: 901231-2123456"
    with pytest.raises(Exception) as exc_info:
        detector.detect(text, mask_types=["invalid_type"])
    assert "유효하지 않은 마스킹 타입입니다" in str(exc_info.value)
