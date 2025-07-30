# setup.py

from setuptools import setup, find_packages

setup(
    name="errorex",
    version="0.1.0",
    author="Minal Bansal",
    description="A Python library for explaining and debugging errors in ML/data pipelines with variable snapshots and LLM-ready prompts.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/minalbansal14/errorex",  # update with actual repo URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "rich",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # You can choose another license
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
    ],
    python_requires=">=3.7",
)
