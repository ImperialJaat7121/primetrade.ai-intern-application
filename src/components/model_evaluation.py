import pandas as pd

from src.utils.main_utils import compute_signals


def evaluate_signal_rate(dataframe: pd.DataFrame, window: int) -> float:
	_, signal_rate = compute_signals(dataframe, window)
	return signal_rate
