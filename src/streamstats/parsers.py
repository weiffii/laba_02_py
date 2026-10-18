import csv
import json
import warnings
from collections.abc import Iterator

from .errors import InvalidEventError, InvalidTimestampError
from .models import Event


def parse_csv(path: str, skipped: list[int], skip_invalid:bool = False) -> Iterator[Event]:
    """Читает CSV-файл и по одному возвращает корректные события"""
    with open(path, "r", encoding="utf-8", newline ="") as file:
        reader = csv.DictReader(file)
        for number, row in enumerate(reader, start=2):
            try:
                event = Event(
                    row["timestamp"],
                    row["level"],
                    row["source"],
                    row["message"]
                )
            except KeyError as error:
                if skip_invalid:
                    skipped[0]+=1
                    warnings.warn(f"Файл {path}, строка {number}: {error}")
                    continue
                else:
                    raise InvalidEventError(f"Ошибка в файле {path}, строка {number} отсутствует поле {error}")
            try:
                event.validate()
            except InvalidTimestampError as error:
                if skip_invalid:
                    skipped[0]+=1
                    warnings.warn(f"Файл {path}, строка {number}: {error}")
                    continue
                else:
                    raise InvalidTimestampError(f"Ошибка в файле {path}, строка {number}: {error}")
            except InvalidEventError as error:
                if skip_invalid:
                    skipped[0]+=1
                    warnings.warn(f"Файл {path}, строка {number}: {error}")
                    continue
                else:
                    raise InvalidEventError(f"Ошибка в файле {path}, строка {number}: {error}")
            yield event

def parse_jsonl(path: str, skipped: list[int], skip_invalid:bool = False) -> Iterator[Event]:
    """Читает JSONL-файл и по одному возвращает корректные события"""
    with open(path, "r", encoding="utf-8") as file:
        for number,line in enumerate(file, start =1):
            if not line.strip():
                if skip_invalid:
                    skipped[0]+=1
                    warnings.warn(f"Файл {path}, строка {number}: пустая строка")
                    continue
                else:
                    raise InvalidEventError(f"Ошибка в файле {path}, строка {number} пустая строка")
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                if skip_invalid:
                    skipped[0]+=1
                    warnings.warn(f"Файл {path}, строка {number}: некорректный JSON")
                    continue
                else:
                    raise InvalidEventError(f"Ошибка в файле {path}, строка {number} некорректный JSON")
            try:
                event = Event(
                    row["timestamp"],
                    row["level"],
                    row["source"],
                    row["message"]
                )
            except KeyError as error:
                if skip_invalid:
                    skipped[0]+=1
                    warnings.warn(f"Файл {path}, строка {number}: {error}")
                    continue
                else:
                    raise InvalidEventError(f"Ошибка в файле {path}, строка {number} отсутствует поле {error}")
            except TypeError as error:
                if skip_invalid:
                    skipped[0]+=1
                    warnings.warn(f"Файл {path}, строка {number}: {error}")
                    continue
                else:
                    raise InvalidEventError(f"Ошибка в файле {path}, строка {number}: {error}")
            try:
                event.validate()
            except InvalidTimestampError as error:
                if skip_invalid:
                    skipped[0]+=1
                    warnings.warn(f"Файл {path}, строка {number}: {error}")
                    continue
                else:
                    raise InvalidTimestampError(f"Ошибка в файле {path}, строка {number}: {error}")
            except InvalidEventError as error:
                if skip_invalid:
                    skipped[0]+=1
                    warnings.warn(f"Файл {path}, строка {number}: {error}")
                    continue
                else:
                    raise InvalidEventError(f"Ошибка в файле {path}, строка {number}: {error}")
            yield event

