from setuptools import setup, find_packages

setup(
    name="wxpal",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "boto3",
    ],
    entry_points={
        'console_scripts': [
            'wxpal=wxpal_cli.cli:main'
        ],
    },
)
