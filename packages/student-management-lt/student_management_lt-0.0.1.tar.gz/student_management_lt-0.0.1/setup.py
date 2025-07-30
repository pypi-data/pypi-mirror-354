from setuptools import setup, find_packages

setup(
    name="student-management-lt",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "PyQt6",
        "python-dotenv"
    ]
)