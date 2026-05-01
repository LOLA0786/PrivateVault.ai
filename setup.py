from setuptools import setup, find_packages

setup(
    name="privatevault-sdk",
    version="1.0.0",
    packages=find_packages(where="sdk"),
    package_dir={"": "sdk"},
    entry_points={
        "console_scripts": [
            "pv-cli=privatevault.cli:main",
        ],
    },
)
