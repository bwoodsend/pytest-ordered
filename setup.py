from setuptools import setup, find_packages
from pathlib import Path

HERE = Path(__file__).resolve().parent

readme = (HERE / "README.rst").read_text("utf-8")

setup(
    author="Brénainn Woodsend",
    author_email="bwoodsend@gmail.com",
    python_requires=">=3.6",
    description="A pytest plugin to control the order in which tests are run in.",
    extras_require={
        "test": ["pytest>=3", "pytest-order", "coverage", "pytest-cov"]
    },
    license="MIT",
    long_description=readme,
    name="pytest_ordered",
    packages=find_packages(include=["pytest_ordered", "pytest_ordered.*"]),
    url="https://github.com/bwoodsend/pytest_ordered",
    version="0.1.0",
)
