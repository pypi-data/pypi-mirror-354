from setuptools import setup, find_packages

setup(
    name="alumath_group20",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Christian, Carine, Eva, Thierry",
    author_email="ishimwechris765@gmail.com",
    description="A library for matrix operations by Group 20",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/alumath_group20",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
