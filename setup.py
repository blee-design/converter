# File: setup.py
from setuptools import setup, find_packages

setup(
    name="question-converter",
    version="2.0",
    author="Udaya Raj Joshi",
    email="udayarajjoshi@aol.com",
    description="Multi-format question converter for academic use",
    long_description=open("README.md", "r", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    py_modules=["converter"],  # Root converter module
    entry_points={
        "console_scripts": [
            "qconvert=converter:main",  # Creates 'qconvert' command
        ],
    },
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
