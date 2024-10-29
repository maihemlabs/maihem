from setuptools import setup, find_packages

setup(
    name="maihem",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "maihem=maihem.cli:cli",
        ],
    },
)
