# setup.py
"""
Setup file untuk NutriCheck.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nutrichecker",
    version="0.1.0",
    author="Eden Simamora",
    author_email="aeden6877@gmail.com",
    description="Library advanced nutrition analysis dan rekomendasi makanan sehat",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/nutricheck",
    packages=find_packages(),
    license="MIT",
    install_requires=[
        "requests",
        "pandas",
        "numpy",
        "scikit-learn",
        "matplotlib",
        "tqdm",
        "tinydb",
        "python-decouple",
        "loguru"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires='>=3.6',
)
