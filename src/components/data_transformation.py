import pandas as pd

from src.utils.main_utils import compute_signals


def transform_data(dataframe: pd.DataFrame, window: int) -> pd.DataFrame:
	processed, _ = compute_signals(dataframe, window)
	return processed
