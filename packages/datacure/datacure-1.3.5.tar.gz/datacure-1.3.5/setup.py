from setuptools import setup, find_packages

setup(
    name="datacure",
    version="1.3.5",
    description="Data Quality tool",
    author="shubham choubey",
    author_email="choubeys331@gmail.com",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy",
        "boto3",
        "python-dotenv",  # 'dotenv' should be 'python-dotenv' on PyPI
        "pyyaml",  # 'yaml' should be 'pyyaml' on PyPI
        "psycopg2",
        "redshift-connector",
        "sqlalchemy-redshift",
        "apscheduler",
        "croniter",
        "jinja2",
        "tabulate",
        "simpleeval",
        "spacy"
    ],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'dqtool = cli.dqtoolcli:main',
        ],
    },
)
