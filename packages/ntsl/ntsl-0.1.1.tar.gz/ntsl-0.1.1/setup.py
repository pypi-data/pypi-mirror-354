from setuptools import setup, find_packages

setup(
    name="ntsl",       # must be unique on PyPI
    version="0.1.1",                # follow semantic versioning
    author="Preston Coley",
    author_email="prestoncoley0920@proton.me",
    description="An easy to use, no-trust security layer.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)