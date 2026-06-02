from setuptools import setup, find_packages
from typing import List
import os

def get_requirements(file_path: str) -> List[str]:
    requirement_lst:List[str] = []
    try:
        with open("requirements.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                #ignore empty lines and -e.
                if requirement and requirement != "-e .":
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    return requirement_lst

setup(
    name = "mlops_project",
    version = "0.0.1",
    author = "Imperialjaat7121",
    author_email = "chaudharykartik7121@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements("requirements.txt")
)