from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="paylix-python-sdk",
    version="1.0.9.1",
    packages=find_packages(),
    url='https://github.com/Paylix/python-sdk',
    install_requires=[
        'requests',
    ],
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown'
)
