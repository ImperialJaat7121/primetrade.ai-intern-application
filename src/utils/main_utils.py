from pathlib import Path
from typing import Any, Dict, Tuple
import csv

import json
import logging

import numpy as np
import pandas as pd

from src.constants import DEFAULT_METRIC_NAME, REQUIRED_DATA_COLUMN


def load_dataset(input_path: str | Path) -> pd.DataFrame:
	input_file = Path(input_path)
	if not input_file.exists():
		raise FileNotFoundError(f"Input file not found: {input_file}")
	if input_file.is_dir():
		raise IsADirectoryError(f"Input path is a directory, not a file: {input_file}")
	if input_file.stat().st_size == 0:
		raise ValueError(f"Input file is empty: {input_file}")

	try:
		dataframe = pd.read_csv(input_file)
	except (pd.errors.ParserError, UnicodeDecodeError, pd.errors.EmptyDataError) as error:
		raise ValueError(f"Invalid CSV format: {error}") from error

	if dataframe.shape[1] == 1 and REQUIRED_DATA_COLUMN not in dataframe.columns:
		raw_column = dataframe.columns[0]
		cleaned_rows = [str(value).strip().strip('"') for value in dataframe[raw_column].tolist() if str(value).strip()]
		if not cleaned_rows:
			raise ValueError(f"Input file is empty: {input_file}")

		parsed_header = next(csv.reader([raw_column]))
		parsed_rows = list(csv.reader(cleaned_rows))
		if not parsed_rows:
			raise ValueError(f"Invalid CSV format: {input_file}")

		header = [column.strip() for column in parsed_header]
		rows = [[cell.strip() for cell in row] for row in parsed_rows]
		dataframe = pd.DataFrame(rows, columns=header)

	if dataframe.empty:
		raise ValueError(f"Input file is empty: {input_file}")
	if REQUIRED_DATA_COLUMN not in dataframe.columns:
		raise ValueError(f"Missing required column: {REQUIRED_DATA_COLUMN}")

	try:
		dataframe[REQUIRED_DATA_COLUMN] = pd.to_numeric(dataframe[REQUIRED_DATA_COLUMN], errors="raise")
	except (TypeError, ValueError) as error:
		raise ValueError(f"Invalid values in required column '{REQUIRED_DATA_COLUMN}': {error}") from error

	return dataframe


def compute_signals(dataframe: pd.DataFrame, window: int) -> Tuple[pd.DataFrame, float]:
	processed = dataframe.copy()
	processed["rolling_mean"] = processed[REQUIRED_DATA_COLUMN].rolling(window=window, min_periods=window).mean()

	valid_rows = processed["rolling_mean"].notna()
	processed["signal"] = np.where(
		valid_rows,
		(processed[REQUIRED_DATA_COLUMN] > processed["rolling_mean"]).astype(int),
		np.nan,
	)

	valid_signals = processed.loc[valid_rows, "signal"]
	signal_rate = float(valid_signals.mean()) if not valid_signals.empty else 0.0
	return processed, signal_rate


def build_metrics(
	*,
	version: str,
	rows_processed: int,
	signal_rate: float,
	latency_ms: int,
	seed: int,
	status: str,
	error_message: str | None = None,
) -> Dict[str, Any]:
	if status == "error":
		return {"version": version, "status": status, "error_message": error_message or "Unknown error"}

	return {
		"version": version,
		"rows_processed": int(rows_processed),
		"metric": DEFAULT_METRIC_NAME,
		"value": round(float(signal_rate), 4),
		"latency_ms": int(latency_ms),
		"seed": int(seed),
		"status": status,
	}


def write_metrics(metrics_path: str | Path, metrics: Dict[str, Any]) -> None:
	metrics_file = Path(metrics_path)
	metrics_file.parent.mkdir(parents=True, exist_ok=True)
	with metrics_file.open("w", encoding="utf-8") as file_obj:
		json.dump(metrics, file_obj, indent=2)
		file_obj.write("\n")


def get_logger(name: str = "mlops_batch_job") -> logging.Logger:
	return logging.getLogger(name)
