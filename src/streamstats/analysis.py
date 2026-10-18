from datetime import datetime

from .models import Event


class Statistics:
    """Хранит и обновляет статистику обработанных событий"""
    def __init__(self) -> None:
        """Создает пустую статистику перед анализом файлов"""
        self.total_events: int = 0
        self.by_level: dict[str,int] = {}
        self.by_source: dict[str, int] = {}
        self.error_sources: dict[str,int] = {}
        self.earliest: datetime | None = None
        self.latest: datetime | None = None
    def update(self, event: Event) -> None:
        """Обновляет статистику на основе одного события"""
        self.total_events += 1
        self.by_level[event.level] = self.by_level.get(event.level, 0) + 1
        self.by_source[event.source] = self.by_source.get(event.source, 0) + 1
        if event.level in ["CRITICAL", "ERROR"]:
            self.error_sources[event.source] = self.error_sources.get(event.source, 0) + 1
        date = datetime.fromisoformat(event.timestamp)
        if self.earliest is None or self.earliest > date:
            self.earliest = date
        if self.latest is None or self.latest < date:
            self.latest = date