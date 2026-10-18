import json

import pytest

from streamstats.errors import InvalidEventError
from streamstats.parsers import parse_csv, parse_jsonl


def test_parse_csv(tmp_path):
    """Проверяет корректность ччтения CSV-файла"""
    file = tmp_path / "events.csv"
    file.write_text(
        "timestamp,level,source,message\n"
        "2026-10-17T10:00:00,INFO,auth,User logged in\n",
        encoding="utf-8"
    )
    skipped = [0]
    events = list(parse_csv(str(file), skipped))
    assert len(events) == 1
    assert events[0].level == "INFO"
    assert events[0].source == "auth"
    assert skipped[0] == 0

def test_parse_jsonl(tmp_path):
    """Проверяет корректность чтения JSONL-файла"""
    file = tmp_path / "events.jsonl"
    event = {
        "timestamp": "2026-10-17T10:00:00",
        "level": "ERROR",
        "source": "server",
        "message": "Connection failed"
    }
    file.write_text(
        json.dumps(event) + "\n",
        encoding="utf-8"
    )
    skipped = [0]
    events = list(parse_jsonl(str(file), skipped))
    assert len(events) == 1
    assert events[0].level == "ERROR"
    assert skipped[0] == 0

@pytest.mark.parametrize("format", ["csv", "jsonl"])
def test_empty_file(tmp_path, format):
    """Проверяет обработку пустого файла"""
    file = tmp_path / f"empty.{format}"
    file.write_text("", encoding="utf-8")
    skipped = [0]
    if format == "csv":
        events = list(parse_csv(str(file), skipped))
    else:
        events = list(parse_jsonl(str(file), skipped))
    assert events == []
    assert skipped[0] == 0

@pytest.mark.parametrize("format", ["csv", "jsonl"])
def test_invalid_without_skip(tmp_path, format):
    """Проверяет ошибку при некорректной строке"""
    file = tmp_path / f"invalid.{format}"
    if format == "csv":
        file.write_text(
            "timestamp,level,source,message\n"
            "2026-10-17T10:00:00,BANANA,auth,Wrong level\n",
            encoding="utf-8"
        )
        parser = parse_csv
    else:
        file.write_text(
            '{"timestamp":"2026-10-17T10:00:00",'
            '"level":"BANANA","source":"auth",'
            '"message":"Wrong level"}\n',
            encoding="utf-8"
        )
        parser = parse_jsonl
    skipped = [0]
    with pytest.raises(InvalidEventError):
        list(parser(str(file),skipped))
    assert skipped[0] == 0

@pytest.mark.parametrize("format", ["csv", "jsonl"])
def test_invalid_with_skip(tmp_path, format):
    """Проверяет пропуск некорректной строки"""
    file = tmp_path / f"invalid.{format}"
    if format == "csv":
        file.write_text(
            "timestamp,level,source,message\n"
            "2026-10-17T10:00:00,BANANA,auth,Wrong level\n"
            "2026-10-17T10:05:00,INFO,auth,Valid event\n",
            encoding="utf-8"
        )
        parser = parse_csv
    else:
        file.write_text(
            '{"timestamp":"2026-10-17T10:00:00",'
            '"level":"BANANA","source":"auth",'
            '"message":"Wrong level"}\n'
            '{"timestamp":"2026-10-17T10:05:00",'
            '"level":"INFO","source":"auth",'
            '"message":"Valid event"}\n',
            encoding="utf-8"
        )
        parser = parse_jsonl
    skipped = [0]
    with pytest.warns(UserWarning):
        events = list(
            parser(str(file), skipped, skip_invalid=True)
        )
    assert len(events) == 1
    assert events[0].level == "INFO"
    assert skipped[0] == 1

@pytest.mark.parametrize("format", ["csv", "jsonl"])
def test_unicode(tmp_path, format):
    """Проверяет обработку Unicode"""
    file = tmp_path / f"unicode.{format}"
    message = "Привет, 世界!"
    if format == "csv":
        file.write_text(
            "timestamp,level,source,message\n"
            f"2026-10-17T10:00:00,INFO,auth,\"{message}\"\n",
            encoding="utf-8"
        )
        parser = parse_csv
    else:
        event = {
            "timestamp": "2026-10-17T10:00:00",
            "level": "INFO",
            "source": "auth",
            "message": message
        }
        file.write_text(
            json.dumps(event, ensure_ascii=False) + "\n",
            encoding="utf-8"
        )
        parser = parse_jsonl
    events = list(parser(str(file), [0]))
    assert events[0].message == message
