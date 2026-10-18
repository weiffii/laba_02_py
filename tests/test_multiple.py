from streamstats.analysis import Statistics
from streamstats.parsers import parse_csv


def test_multiple_files(tmp_path):
    """Проверяет объединение статистики из несокльких файлов"""
    file1 = tmp_path / "first.csv"
    file2 = tmp_path / "second.csv"
    file1.write_text(
        "timestamp,level,source,message\n"
        "2026-10-17T10:00:00,INFO,auth,Login\n",
        encoding="utf-8"
    )
    file2.write_text(
        "timestamp,level,source,message\n"
        "2026-10-17T11:00:00,ERROR,server,Failure\n",
        encoding="utf-8"
    )
    stats = Statistics()
    skipped = [0]
    for path in [file1, file2]:
        for event in parse_csv(str(path), skipped):
            stats.update(event)

    assert stats.total_events == 2
    assert stats.by_level == {"INFO": 1, "ERROR": 1}
    assert stats.by_source == {"auth": 1, "server": 1}
    assert skipped[0] == 0