# MLOps Batch Job

This repository contains a minimal deterministic batch job that:

- loads configuration from `config.yaml`
- reads OHLCV data from `data/raw/data.csv`
- computes a rolling mean on the `close` column
- generates a binary signal from `close` vs rolling mean
- writes machine-readable metrics to `metrics.json`
- writes structured logs to `run.log`

## Local Run

Install the dependencies first:

```bash
pip install -r requirements.txt
```

Run the job with explicit paths:

```bash
python run.py --input data/raw/data.csv --config config.yaml --output metrics.json --log-file run.log
```

You can also use the optional `.env` file for path overrides. No credentials are required for this assessment.

## Docker Run

Build the container:

```bash
docker build -t mlops-task .
```

Run the container:

```bash
docker run --rm mlops-task
```

The container includes `data/raw/data.csv` and `config.yaml`, writes `metrics.json` and `run.log`, prints the final metrics JSON to stdout, and exits with code `0` on success.

## Config

`config.yaml` must contain:

```yaml
seed: 42
window: 5
version: "v1"
```

## Data Schema

The dataset schema is documented in `data/schema/schema.yaml`.

## Example Metrics Output

```json
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4991,
  "latency_ms": 56,
  "seed": 42,
  "status": "success"
}
```
