from setuptools import setup, find_packages

setup(
    name="dataqualitys",
    version="1.9.7",
    description="Data Quality tool",
    author="shubham choubey",
    author_email="choubeys331@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    package_data={'dataqualitys': ['templates/**/*.j2', 'templates/**/*.jinja']},
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
    entry_points={
        'console_scripts': [
            'dqtool = cli.dqtoolcli:main',
        ],
    },
)
