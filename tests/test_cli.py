import json

from typer.testing import CliRunner

from streamstats.__main__ import app

runner = CliRunner()

def test_cli(tmp_path):
    """Првоеряет запуск CLI и создание отчета в файле JSON"""
    file = tmp_path / "events.csv"
    output = tmp_path / "report.json"
    file.write_text(
        "timestamp,level,source,message\n"
        "2026-10-17T10:00:00,INFO,auth,Login\n",
        encoding="utf-8"
    )
    result = runner.invoke(app, [
        "analyze",
        str(file),
        "--format", "csv",
        "--output", str(output)
    ])
    assert result.exit_code == 0
    assert output.exists()
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["total_events"] == 1
    assert report["by_level"] == {"INFO": 1}