from setuptools import setup, find_packages

setup(
    name="private_db_llm",
    version="0.1.0",
    description="Generate and execute SQL queries against MySQL using an LLM. Get prompt and MySQL connection, give the response with no data leakage!",
    author="Matin Khosravi",
    author_email="matinkhosravi97@gmail.com",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python>=8.0.0",
        "psycopg2-binary>=2.9.0",
        "openai>=0.27.0",
        "httpx>=0.23.0",
    ],
    python_requires=">=3.12",
)
