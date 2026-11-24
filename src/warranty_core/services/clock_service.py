from abc import ABC, abstractmethod
from datetime import datetime, date, timezone

class IClockService(ABC):
    @abstractmethod
    def now(self) -> datetime:
        pass

    @abstractmethod
    def today(self) -> date:
        pass

class SystemClockService(IClockService):
    def now(self) -> datetime:
        return datetime.now(timezone.utc)

    def today(self) -> date:
        return datetime.now(timezone.utc).date()

class SimulatedClockService(IClockService):
    def __init__(self, current_time: datetime):
        self._current_time = current_time

    def set_time(self, new_time: datetime) -> None:
        self._current_time = new_time

    def set_date(self, new_date: date) -> None:
        self._current_time = datetime.combine(
            new_date,
            self._current_time.time(),
            tzinfo=self._current_time.tzinfo
        )

    def now(self) -> datetime:
        return self._current_time

    def today(self) -> date:
        return self._current_time.date()
