from pathlib import Path
from setuptools import setup, find_packages

# read the README
here = Path(__file__).parent
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="private-db-llm",
    version="0.1.1",  # bump for this patch release
    author="Matin Khosravi",
    author_email="matinkhosravi97@gmail.com",
    description="Generate and execute SQL queries against MySQL/PostgreSQL using an LLM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matinkhosravi/private-db-llm",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python>=8.0.0",
        "openai>=1.0.0",
        "httpx>=0.23.0",
        "psycopg2-binary>=2.9.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
