
from setuptools import setup, find_packages

setup(
    name='airflow-secret-loader',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "boto3"
    ],
    description='Auto-load AWS Secrets into Airflow Variables via env',
    author='Your Name',
    author_email='your@email.com',
)
