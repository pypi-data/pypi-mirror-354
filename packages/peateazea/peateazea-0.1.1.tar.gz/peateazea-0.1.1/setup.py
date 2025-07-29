from setuptools import setup, find_packages

setup(
    name="peateazea",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Ben Baptist",
    author_email="sawham6@gmail.com",
    description="A Python package for controlling PTZ cameras through various protocols",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/benbaptist/peateazea",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
