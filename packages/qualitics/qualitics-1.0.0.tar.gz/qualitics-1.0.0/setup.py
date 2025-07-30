from setuptools import setup, find_packages

setup(
    name="qualitics",
    version="1.0.0",
    description="Data Quality Tool",
    author="shubham choubey",
    author_email="choubeys331@gmail.com",
    packages=find_packages(include=["qualitics", "qualitics.*"]),
    include_package_data=True,
    install_requires=[
        "sqlalchemy",
        "boto3",
        "python-dotenv",
        "pyyaml",
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
            'dqtool = qualitics.cli.dqtoolcli:main',
        ],
    },
)
