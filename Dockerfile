FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	INPUT_PATH=data/raw/data.csv \
	CONFIG_PATH=config.yaml \
	OUTPUT_PATH=metrics.json \
	LOG_FILE=run.log \
	VERSION=v1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

CMD ["python", "run.py", "--input", "data/raw/data.csv", "--config", "config.yaml", "--output", "metrics.json", "--log-file", "run.log"]
