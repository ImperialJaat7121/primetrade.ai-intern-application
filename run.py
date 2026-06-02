from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from src.config.configuration import load_yaml_config, validate_config
from src.constants import DEFAULT_ERROR_STATUS, DEFAULT_SUCCESS_STATUS
from src.logging.logger import configure_logger
from src.utils.main_utils import build_metrics, compute_signals, load_dataset, write_metrics


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Minimal deterministic MLOps batch job")
	parser.add_argument("--input", default=os.getenv("INPUT_PATH", os.getenv("MLOPS_INPUT_PATH", "data/raw/data.csv")), help="Path to the input CSV file")
	parser.add_argument("--config", default=os.getenv("CONFIG_PATH", os.getenv("MLOPS_CONFIG_PATH", "config.yaml")), help="Path to the YAML config file")
	parser.add_argument("--output", default=os.getenv("OUTPUT_PATH", os.getenv("MLOPS_OUTPUT_PATH", "metrics.json")), help="Path to the output metrics JSON file")
	parser.add_argument("--log-file", default=os.getenv("LOG_FILE", os.getenv("MLOPS_LOG_FILE", "run.log")), help="Path to the log file")
	return parser.parse_args()


def main() -> int:
	load_dotenv()
	args = parse_args()
	logger = configure_logger(args.log_file)

	job_start = time.perf_counter()
	logger.info("Job start timestamp: %s", time.strftime("%Y-%m-%dT%H:%M:%S"))

	config_data = None
	try:
		config_data = load_yaml_config(args.config)
		job_config = validate_config(config_data)
		logger.info("Config loaded and validated: seed=%s window=%s version=%s", job_config.seed, job_config.window, job_config.version)

		import numpy as np

		np.random.seed(job_config.seed)
		logger.info("Seed set to %s", job_config.seed)

		dataframe = load_dataset(args.input)
		logger.info("Rows loaded: %s", len(dataframe))
		logger.info("Processing step: rolling mean computation")
		processed_data, signal_rate = compute_signals(dataframe, job_config.window)
		logger.info("Processing step: signal generation")

		latency_ms = int((time.perf_counter() - job_start) * 1000)
		metrics = build_metrics(
			version=job_config.version,
			rows_processed=len(processed_data),
			signal_rate=signal_rate,
			latency_ms=latency_ms,
			seed=job_config.seed,
			status=DEFAULT_SUCCESS_STATUS,
		)
		write_metrics(args.output, metrics)
		logger.info("Metrics summary: %s", metrics)
		logger.info("Job end status: success")
		print(json.dumps(metrics, indent=2))
		return 0
	except Exception as error:
		latency_ms = int((time.perf_counter() - job_start) * 1000)
		logger.exception("Job failed")
		fallback_version = os.getenv("VERSION", "v1")
		fallback_seed = 42
		if isinstance(config_data, dict):
			fallback_version = str(config_data.get("version", fallback_version))
			try:
				fallback_seed = int(config_data.get("seed", fallback_seed))
			except (TypeError, ValueError):
				fallback_seed = 42

		metrics = build_metrics(
			version=fallback_version,
			rows_processed=0,
			signal_rate=0.0,
			latency_ms=latency_ms,
			seed=fallback_seed,
			status=DEFAULT_ERROR_STATUS,
			error_message=str(error),
		)
		write_metrics(args.output, metrics)
		logger.info("Job end status: error")
		print(json.dumps(metrics, indent=2))
		return 1


if __name__ == "__main__":
	raise SystemExit(main())
