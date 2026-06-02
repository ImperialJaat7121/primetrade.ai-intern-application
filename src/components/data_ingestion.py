from pathlib import Path

import pandas as pd

from src.utils.main_utils import load_dataset


def ingest_data(input_path: str | Path) -> pd.DataFrame:
	return load_dataset(input_path)
