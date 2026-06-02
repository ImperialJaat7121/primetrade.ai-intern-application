import os
from pathlib import Path

list_of_files = [
    ".gitignore",
    "setup.py",
    "requirements.txt",
    "Dockerfile",
    "config.yaml",
    "run.py",
    "main.py",
    "data/data.csv",
    "templates/index.html",
    "notebooks/exploration.ipynb",
    "src/__init__.py",
    "src/exception/__init__.py",
    "src/exception/exception.py",
    "src/logging/__init__.py",
    "src/logging/logger.py",
    "src/constants/__init__.py",
    "src/utils/__init__.py",
    "src/utils/main_utils.py",
    "src/entity/__init__.py",
    "src/entity/config_entity.py",
    "src/config/__init__.py",
    "src/config/configuration.py",
    "src/components/__init__.py",
    "src/components/data_ingestion.py",
    "src/components/data_transformation.py",
    "src/components/model_evaluation.py",
]

for filepath in list_of_files:
    path = Path(filepath)
    file_dir, filename = os.path.split(path)
    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w") as f:
            pass
print("MLOps Project Structure successfully bootstrapped!")