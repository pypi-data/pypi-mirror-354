from setuptools import setup, find_packages

setup(
    name="polymerization_planner",
    version="0.1.0",
    description="A tool to generate reaction recipes from user-defined molar ratios and stock concentrations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Cesar Ramirez",
    packages=find_packages(),
    install_requires=["pandas", "openpyxl","numpy"],
    entry_points={
        "console_scripts": [
            "atrp-calc=atrp_calculator.main:cli",  # Make sure your main.py has a function named `cli()`
        ],
    },
    python_requires=">=3.7",
)
