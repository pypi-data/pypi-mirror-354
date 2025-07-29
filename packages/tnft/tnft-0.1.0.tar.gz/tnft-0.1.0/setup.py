from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tnft",
    version="0.1.0",
    author="Furry",
    author_email="your.email@example.com",
    description="Python client for NFT API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tnft",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)