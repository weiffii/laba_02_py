from datetime import datetime

from .errors import InvalidEventError, InvalidTimestampError


class Event:
    """Представляет событие из CSV/JSONL файла"""
    def __init__(self, timestamp: str, level: str, source: str, message: str) -> None:
        """Создает событие с заданными полями"""
        self.timestamp = timestamp
        self.level = level
        self.source = source
        self.message = message
    def validate(self) -> None:
        """Проверяет корректность полей события"""
        if self.level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise InvalidEventError("Неправильное значение в level")
        if  not isinstance(self.source, str) or not self.source.strip():
            raise InvalidEventError("Неправильное значение в source")
        if not isinstance(self.message, str):
            raise InvalidEventError("Неправильное значение в message")
        if not isinstance(self.timestamp, str):
            raise InvalidTimestampError("Неправильное значение в timestamp")
        try:
            datetime.fromisoformat(self.timestamp)
        except ValueError:
            raise InvalidTimestampError("Неправильное значение в timestamp")

