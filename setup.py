from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="numsys-math",
    version="1.0.0",
    author="Kosta Novosel",
    author_email="novoselkosta@gmail.com",
    description="Convert between number systems and perform arithmetic.",
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