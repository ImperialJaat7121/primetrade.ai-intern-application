from pathlib import Path
from typing import Any, Dict

import yaml

from src.constants import REQUIRED_CONFIG_KEYS
from src.entity.config_entity import JobConfig


def load_yaml_config(config_path: str | Path) -> Dict[str, Any]:
	config_file = Path(config_path)
	if not config_file.exists():
		raise FileNotFoundError(f"Config file not found: {config_file}")

	try:
		with config_file.open("r", encoding="utf-8") as file_obj:
			config_data = yaml.safe_load(file_obj)
	except yaml.YAMLError as error:
		raise ValueError(f"Invalid YAML config: {error}") from error

	if not isinstance(config_data, dict):
		raise ValueError("Invalid config structure: expected a YAML mapping")

	return config_data


def validate_config(config_data: Dict[str, Any]) -> JobConfig:
	missing_keys = [key for key in REQUIRED_CONFIG_KEYS if key not in config_data]
	if missing_keys:
		raise ValueError(f"Invalid config structure: missing keys {', '.join(missing_keys)}")

	try:
		seed = int(config_data["seed"])
		window = int(config_data["window"])
		version = str(config_data["version"]).strip()
	except (TypeError, ValueError, KeyError) as error:
		raise ValueError(f"Invalid config structure: {error}") from error

	if window <= 0:
		raise ValueError("Invalid config structure: window must be a positive integer")
	if not version:
		raise ValueError("Invalid config structure: version cannot be empty")

	return JobConfig(seed=seed, window=window, version=version)
