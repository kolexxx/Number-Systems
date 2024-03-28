from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="number-systems",
    version="1.0.0",
    author="Kosta Novosel",
    author_email="novoselkosta@gmail.com",
    description="A short description of your package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kolexxx/Number-Systems",
    packages=['numsys'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)