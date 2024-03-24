from pathlib import Path

import world_bank_data as wb

SAMPLE_DIR = Path(__file__).parent / ".." / "src" / "itables" / "samples"


def create_csv_file_if_missing(df, csv_file):
    if not csv_file.exists():
        with open(str(csv_file), "w") as fp:  # pragma: no cover
            fp.write(df.to_csv())


def test_update_countries(csv_file=SAMPLE_DIR / "countries.csv"):
    df = wb.get_countries()
    create_csv_file_if_missing(df, csv_file)


def test_update_population(csv_file=SAMPLE_DIR / "population.csv"):
    x = wb.get_series("SP.POP.TOTL", mrv=1, simplify_index=True)
    create_csv_file_if_missing(x, csv_file)


def test_update_indicators(csv_file=SAMPLE_DIR / "indicators.csv"):
    df = wb.get_indicators().sort_index().head(500)
    create_csv_file_if_missing(df, csv_file)
