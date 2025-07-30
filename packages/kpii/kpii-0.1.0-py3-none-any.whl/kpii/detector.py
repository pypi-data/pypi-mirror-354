import re
from typing import List, Dict, Any


class KoreanPIIDetectorError(Exception):
    """KPII 감지기 관련 기본 예외 클래스"""


class InvalidInputError(KoreanPIIDetectorError):
    """잘못된 입력값에 대한 예외"""


class MaskingError(KoreanPIIDetectorError):
    """마스킹 처리 중 발생하는 예외"""


class KoreanPIIDetector:
    def __init__(self):
        # 주민등록번호 패턴 (하이픈 포함/미포함)
        self.rrn_pattern = re.compile(r"\d{6}[-\s]?\d{7}")

        # 전화번호 패턴 (지역번호, 휴대폰)
        self.phone_pattern = re.compile(
            r"(?:0[2-9]{1,2}|01[0-9])[-\s]?\d{3,4}[-\s]?\d{4}"  # 지역번호나 휴대폰 번호로 시작하는 경우만
        )

        # 이메일 패턴
        self.email_pattern = re.compile(
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        )

        # 신용카드 번호 패턴 (하이픈 포함/미포함)
        self.credit_card_pattern = re.compile(r"\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}")

    def detect(
        self, text: str, mask_types: List[str] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        주어진 텍스트에서 개인정보를 탐지합니다.

        Args:
            text (str): 검사할 텍스트
            mask_types (List[str], optional): 마스킹할 항목 목록.
                가능한 값: ["rrn", "phone", "email", "credit_card"]
                기본값은 None으로, 모든 항목을 마스킹합니다.

        Returns:
            Dict[str, List[Dict[str, Any]]]: 탐지된 개인정보 목록

        Raises:
            InvalidInputError: 입력 텍스트가 유효하지 않은 경우
        """
        if not isinstance(text, str):
            raise InvalidInputError("입력값은 문자열이어야 합니다.")

        if not text.strip():
            raise InvalidInputError("입력 텍스트가 비어있습니다.")

        if mask_types is not None:
            valid_types = ["rrn", "phone", "email", "credit_card"]
            if not all(t in valid_types for t in mask_types):
                raise InvalidInputError(
                    f"유효하지 않은 마스킹 타입입니다. 가능한 값: {valid_types}"
                )

        try:
            results = {}
            if mask_types is None or "rrn" in mask_types:
                results["rrn"] = self._detect_rrn(text)
            if mask_types is None or "phone" in mask_types:
                results["phone"] = self._detect_phone(text)
            if mask_types is None or "email" in mask_types:
                results["email"] = self._detect_email(text)
            if mask_types is None or "credit_card" in mask_types:
                results["credit_card"] = self._detect_credit_card(text)
            return results
        except Exception as e:
            raise KoreanPIIDetectorError(f"개인정보 탐지 중 오류 발생: {str(e)}") from e

    def _detect_rrn(self, text: str) -> List[Dict[str, Any]]:
        matches = []
        for match in self.rrn_pattern.finditer(text):
            rrn = match.group()
            # 하이픈 추가
            masked_rrn = rrn[:8] + "*" * 6
            matches.append(
                {
                    "type": "주민등록번호",
                    "value": rrn,
                    "masked_value": masked_rrn,
                    "start": match.start(),
                    "end": match.end(),
                }
            )
        return matches

    def _detect_phone(self, text: str) -> List[Dict[str, Any]]:
        matches = []
        for match in self.phone_pattern.finditer(text):
            phone = match.group()
            # 마스킹 처리된 결과 (뒤 4자리)
            masked_phone = phone[: len(phone) - 4] + "*" * 4
            matches.append(
                {
                    "type": "전화번호",
                    "value": phone,
                    "masked_value": masked_phone,
                    "start": match.start(),
                    "end": match.end(),
                }
            )
        return matches

    def _detect_email(self, text: str) -> List[Dict[str, Any]]:
        matches = []
        for match in self.email_pattern.finditer(text):
            email = match.group()
            # 마스킹 처리된 결과 (이름의 첫 번째 글자만 표시)
            username, domain = email.split("@")
            masked_email = username[0] + "*" * (len(username) - 1) + "@" + domain
            matches.append(
                {
                    "type": "이메일",
                    "value": email,
                    "masked_value": masked_email,
                    "start": match.start(),
                    "end": match.end(),
                }
            )
        return matches

    def _detect_credit_card(self, text: str) -> List[Dict[str, Any]]:
        matches = []
        for match in self.credit_card_pattern.finditer(text):
            card = match.group()
            # 하이픈 제거 후 마스킹
            card_clean = card.replace("-", "").replace(" ", "")
            masked_card = f"{card_clean[:6]}{'*' * 6}{card_clean[12:]}"
            # 하이픈 추가 (4자리씩)
            masked_card = "-".join(masked_card[i : i + 4] for i in range(0, 16, 4))
            matches.append(
                {
                    "type": "신용카드",
                    "value": card,
                    "masked_value": masked_card,
                    "start": match.start(),
                    "end": match.end(),
                }
            )
        return matches

    def mask_text(self, text: str, mask_types: List[str] = None) -> str:
        """
        주어진 텍스트에서 개인정보를 마스킹 처리합니다.

        Args:
            text (str): 마스킹 처리할 텍스트
            mask_types (List[str], optional): 마스킹할 항목 목록.
                가능한 값: ["rrn", "phone", "email", "credit_card"]
                기본값은 None으로, 모든 항목을 마스킹합니다.

        Returns:
            str: 마스킹 처리된 텍스트

        Raises:
            InvalidInputError: 입력 텍스트가 유효하지 않은 경우
            MaskingError: 마스킹 처리 중 오류가 발생한 경우
        """
        if not isinstance(text, str):
            raise InvalidInputError("입력값은 문자열이어야 합니다.")

        if not text.strip():
            raise InvalidInputError("입력 텍스트가 비어있습니다.")

        try:
            results = self.detect(text, mask_types)
            masked_text = text

            # 마스킹 처리를 위해 end 위치부터 처리
            for pii_type in results.values():
                for pii in sorted(pii_type, key=lambda x: x["end"], reverse=True):
                    try:
                        masked_text = (
                            masked_text[: pii["start"]]
                            + pii["masked_value"]
                            + masked_text[pii["end"] :]
                        )
                    except Exception as e:
                        raise MaskingError(f"마스킹 처리 중 오류 발생: {str(e)}") from e

            return masked_text
        except Exception as e:
            raise MaskingError(f"마스킹 처리 중 오류 발생: {str(e)}") from e
