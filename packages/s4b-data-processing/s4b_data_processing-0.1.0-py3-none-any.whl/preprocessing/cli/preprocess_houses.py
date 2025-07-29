
+41
-0

import argparse
from pathlib import Path
import pandas as pd

from preprocessing.core.houses import preprocess_houses


def load_dataframe(path: Path) -> pd.DataFrame:
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    elif path.suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")


def save_dataframe(df: pd.DataFrame, path: Path) -> None:
    if path.suffix == ".parquet":
        df.to_parquet(path, index=False)
    elif path.suffix in {".xlsx", ".xls"}:
        df.to_excel(path, index=False)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")


def main(args=None) -> None:
    parser = argparse.ArgumentParser(description="Compute house-level statistics")
    parser.add_argument("deals", type=Path, help="Path to deals file")
    parser.add_argument("pd", type=Path, help="Path to project declarations file")
    parser.add_argument("output", type=Path, help="Path to save result")

    parsed = parser.parse_args(args)

    df_deals = load_dataframe(parsed.deals)
    df_pd = load_dataframe(parsed.pd)
    result = preprocess_houses(df_deals, df_pd)
    save_dataframe(result, parsed.output)


if __name__ == "__main__":
    main()