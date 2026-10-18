import json

from .analysis import Statistics


def build_report(stats: Statistics, skipped: int = 0) -> dict:
    """Формирует словарь с итоговой статистикой событий"""
    report = {"total_events": stats.total_events,
              "by_level": stats.by_level,
              "by_source": stats.by_source,
              "top_error_sources": dict(sorted(stats.error_sources.items(), key = lambda item: item[1], reverse = True)[:5]),
              "earliest_timestamp": stats.earliest.isoformat() if stats.earliest is not None else None,
              "latest_timestamp": stats.latest.isoformat() if stats.latest is not None else None,
              "skipped_events": skipped}
    return report

def save_report(report: dict, path:str) -> None:
    """Сохраняет отчет в файл JSON"""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=4)
    