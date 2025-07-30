from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='airflow-secret-loader',
    version='1.1.0',
    packages=find_packages(),
    install_requires=[
        "boto3",
        "azure-identity"
    ],
    description='Fetch AWS secrets as dictionary using optional Azure Identity role assumption',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='rajeshkbathula',
    author_email='rajb7723@gmail.com',
    url='https://github.com/rajeshkbathula/airflow-secret-loader',
    project_urls={
        'Source Code': 'https://github.com/rajeshkbathula/airflow-secret-loader',
        'Bug Tracker': 'https://github.com/rajeshkbathula/airflow-secret-loader/issues',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
