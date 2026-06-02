from dataclasses import dataclass


@dataclass(frozen=True)
class JobConfig:
	seed: int
	window: int
	version: str
