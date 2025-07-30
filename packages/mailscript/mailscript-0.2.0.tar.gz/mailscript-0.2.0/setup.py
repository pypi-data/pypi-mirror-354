"""
Setup script for mailscript package.
"""

from setuptools import setup, find_packages
import os

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from version.txt using absolute path
try:
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "version.txt"), "r", encoding="utf-8") as f:
        version = f.read().strip()
except FileNotFoundError:
    print("Warning: version.txt not found. Using default version 0.1.0")
    version = "0.1.0"


setup(
    name="mailscript",
    version=version,
    author="Rakshith Kalmadi",
    author_email="rakshithkalmadi@gmail.com",
    description="A Python library for simplified email sending and receiving with secure credentials management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rakshithkalmadi/mailscript",
    packages=find_packages(exclude=["*.secret", "*.secret.*", "secret.*", "secret", "config", "tests"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Email",
    ],
    python_requires=">=3.7",
    install_requires=[
        "jinja2>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=21.5b2",
            "flake8>=3.9.0",
        ],
    },
    keywords="email, smtp, mail, template, html-email",
)
