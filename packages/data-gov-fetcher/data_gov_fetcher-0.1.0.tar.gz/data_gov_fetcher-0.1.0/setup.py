from setuptools import setup, find_packages

setup(
    name="data-gov-fetcher",
    version="0.1.0",
    description="A CLI tool to fetch datasets from Data.gov CKAN API",
    author="brainiacpol",
    author_email="work4product@gmail.com",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "datafetch=data_gov_fetcher.cli:run",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
