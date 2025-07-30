#!/usr/bin/env python3
"""
PyDefender Setup
================

Установочный файл для публикации в PyPI
"""

from setuptools import setup, find_packages
from pathlib import Path

# Читаем README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8') if (this_directory / "README.md").exists() else """
# 🛡️ Beautiful Validator - Beautiful Smart Input Validation

**The most beautiful and intelligent input validation library for Python** 🌟

## ✨ Quick Start

```python
import beautiful_validator as pv

@pv.number(min_value=0, max_value=100)
def set_score(score):
    return f"Score: {score}"

@pv.name()
def set_name(name):
    return f"Hello, {name}!"

# Try it!
print(set_score("85"))      # ✅ Score: 85
print(set_name("  john  ")) # ✅ Hello, John!
```
"""

setup(
    name="beautiful-validator",  # ИЗМЕНЕНО: новое уникальное имя
    version="0.0.1",
    author="PyDefender Team",
    author_email="team@pydefender.dev",
    description="🛡️ Beautiful Smart Input Validation for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pydefender/pydefender",
    project_urls={
        "Homepage": "https://github.com/pydefender/pydefender",
        "Bug Reports": "https://github.com/pydefender/pydefender/issues",
        "Source": "https://github.com/pydefender/pydefender",
        "Documentation": "https://pydefender.dev/docs",
        "Changelog": "https://github.com/pydefender/pydefender/blob/main/CHANGELOG.md",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    install_requires=[
        "colorama>=0.4.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
            "pre-commit>=3.0.0",
        ],
        "test": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "coverage>=7.0.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.0.0",
            "mkdocstrings>=0.22.0",
        ]
    },
    keywords=[
        "validation", "input", "data", "forms", "decorators",
        "beautiful", "smart", "defensive", "programming", "python",
        "validators", "validation-library", "input-validation",
        "data-validation", "form-validation", "type-checking"
    ],
    include_package_data=True,
    zip_safe=False,
    license="MIT",
    platforms=["any"],
    package_data={
        "pydefender": [
            "py.typed",
        ],
    },
)