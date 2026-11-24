from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List

@dataclass
class EmailMessage:
    message_id: str
    recipient: str
    subject: str
    body_text: str
    sent_at: datetime
    is_success: bool = True
    error_message: str = ""

class IEmailService(ABC):
    @abstractmethod
    def send_email(self, recipient: str, subject: str, body_text: str) -> bool:
        pass

    @abstractmethod
    def get_sent_messages(self) -> List[EmailMessage]:
        pass

class MockEmailService(IEmailService):
    def __init__(self):
        self._sent_messages: List[EmailMessage] = []
        self._simulate_failure: bool = False

    def set_failure_simulation(self, should_fail: bool) -> None:
        self._simulate_failure = should_fail

    def send_email(self, recipient: str, subject: str, body_text: str) -> bool:
        now_dt = datetime.now(timezone.utc)
        if self._simulate_failure:
            msg = EmailMessage(
                message_id=f"MSG_{len(self._sent_messages)+1:04d}",
                recipient=recipient,
                subject=subject,
                body_text=body_text,
                sent_at=now_dt,
                is_success=False,
                error_message="SMTP connection timed out"
            )
            self._sent_messages.append(msg)
            return False

        msg = EmailMessage(
            message_id=f"MSG_{len(self._sent_messages)+1:04d}",
            recipient=recipient,
            subject=subject,
            body_text=body_text,
            sent_at=now_dt,
            is_success=True
        )
        self._sent_messages.append(msg)
        return True

    def get_sent_messages(self) -> List[EmailMessage]:
        return list(self._sent_messages)

    def clear(self) -> None:
        self._sent_messages.clear()
