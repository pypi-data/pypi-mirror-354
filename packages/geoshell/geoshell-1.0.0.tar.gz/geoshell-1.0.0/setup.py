from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="geoshell",
    version="1.0.0",
    author="kelv",
    author_email="your.email@example.com",
    description="A CLI & Python library to fetch real-time geo-data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kelv-inn/geoshell",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "geoshell=geoshell.cli:main",
        ],
    },
)