"""
Setup script for cursor-deeplink package.
"""

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the requirements file
try:
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
except FileNotFoundError:
    requirements = []

setup(
    name="cursor-deeplink",
    version="0.1.1",
    author="Cursor Deeplink Generator",
    author_email="",
    description="A Python package for generating Cursor deeplinks for MCP server installation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hemanth/cursor-deeplink",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.900",
        ],
    },
    entry_points={
        "console_scripts": [
            "cursor-deeplink=cursor_deeplink.cli:main",
        ],
    },
    keywords="cursor deeplink mcp server installation",
    project_urls={
        "Bug Reports": "https://github.com/hemanth/cursor-deeplink/issues",
        "Source": "https://github.com/hemanth/cursor-deeplink",
        "Documentation": "https://docs.cursor.com/deeplinks",
    },
) 