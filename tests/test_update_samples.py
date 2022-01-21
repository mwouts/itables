from pathlib import Path

import pytest
import world_bank_data as wb

sample_dir = Path(__file__).parent / ".." / "itables" / "samples"


def test_update_countries():
    df = wb.get_countries()
    with open(sample_dir / "countries.csv", "w") as fp:
        fp.write(df.to_csv())


def test_update_population():
    x = wb.get_series("SP.POP.TOTL", mrv=1, simplify_index=True)
    with open(sample_dir / "population.csv", "w") as fp:
        fp.write(x.to_csv())


@pytest.mark.skip("The indicators appear to change often")
def test_update_indicators():
    df = wb.get_indicators().sort_index().head(500)
    with open(sample_dir / "indicators.csv", "w") as fp:
        fp.write(df.to_csv())
