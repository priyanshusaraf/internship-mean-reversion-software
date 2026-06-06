import csv
import pytest


@pytest.fixture
def sample_csv(tmp_path) -> str:
    path = tmp_path / "nifty.csv"
    rows = [
        ["date", "open", "high", "low", "close", "volume"],
        ["2024-01-01", "21000.0", "21200.0", "20900.0", "21100.0", "1000000"],
        ["2024-01-02", "21100.0", "21300.0", "21000.0", "21250.0", "1100000"],
        ["2024-01-03", "21250.0", "21400.0", "21100.0", "21150.0", "900000"],
    ]
    with open(path, "w", newline="") as f:
        csv.writer(f).writerows(rows)
    return str(path)
