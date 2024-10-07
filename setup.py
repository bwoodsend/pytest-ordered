from setuptools import setup, find_packages
from pathlib import Path

HERE = Path(__file__).resolve().parent

readme = (HERE / "README.rst").read_text("utf-8")

setup(
    author="Brénainn Woodsend",
    author_email="bwoodsend@gmail.com",
    classifiers=[
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
    ],
    description="A pytest plugin to control the order in which tests are run in.",
    entry_points={
        "pytest11": ["ordered = pytest_ordered",],
    },
    install_requires=["pytest>=6.2.0"],
    license="MIT",
    long_description=readme,
    name="pytest-ordered",
    py_modules=["pytest_ordered"],
    python_requires=">=3.6",
    version="0.1.0",
    url="https://github.com/bwoodsend/pytest-ordered",
)
