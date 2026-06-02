from pathlib import Path
from typing import List

from setuptools import find_packages, setup


def get_requirements(file_path: str) -> List[str]:
    requirements: List[str] = []
    requirements_path = Path(__file__).resolve().parent / file_path
    try:
        with requirements_path.open("r", encoding="utf-8") as file:
            for line in file:
                requirement = line.strip()
                if requirement and requirement != "-e .":
                    requirements.append(requirement)
    except FileNotFoundError:
        print(f"Error: {requirements_path} not found.")
    return requirements


setup(
    name="mlops_project",
    version="0.0.1",
    author="Imperialjaat7121",
    author_email="chaudharykartik7121@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)