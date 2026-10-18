from pathlib import Path

import typer

from .analysis import Statistics
from .errors import CLIConfigError, InvalidFormatError, StreamStatsError
from .parsers import parse_csv, parse_jsonl
from .report import build_report, save_report

app = typer.Typer()

@app.callback()
def main() -> None:
    """Создает приложения CLI"""

@app.command()
def analyze(inputs: list[str] = typer.Argument(..., help = "Путь к входным файлам"),
            format: str = typer.Option(..., help = "Формат входных файлов"),
            output: str = typer.Option(..., help = "Название файла для записи репорта"),
            skip_invalid: bool = typer.Option(False, help="Пропускать некорректные события")) -> None:
    """Анализирует входные файлы и сохраняет статистику в JSON"""
    try:
        if format not in ["csv", "jsonl"]:
            raise InvalidFormatError(f"Неподдерживаемый формат: {format}")
    except InvalidFormatError as error:
        typer.echo(f"Ошибка: {error}", err = True)
        raise typer.Exit(code=2)
    stats = Statistics()
    skipped = [0]
    try:
        for path in inputs:
            if Path(path).resolve() == Path(output).resolve():
                raise CLIConfigError("Входной и выходной файлы не должны совпадать")
        for path in inputs:
            if format == 'csv':
                parser = parse_csv(path, skipped, skip_invalid=skip_invalid)
            else:
                parser = parse_jsonl(path, skipped, skip_invalid=skip_invalid)
            for event in parser:
                stats.update(event)
        report = build_report(stats, skipped[0])
        save_report(report, output)
    except StreamStatsError as error:
        typer.echo(f"Ошибка: {error}", err = True)
        raise typer.Exit(code=2)
    except OSError as error:
        typer.echo(f"Ошибка работы с файлом: {error}", err=True)
        raise typer.Exit(code=2)

if __name__ == '__main__':
    app()