"""
Setup configuration for Rapid framework
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rapid-api",
    version="0.1.0",
    author="Wesley Ellis",
    author_email="your.email@example.com",
    description="The fastest Python web framework for building APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wesellis/rapid",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "uvloop>=0.17.0; sys_platform != 'win32'",  # High-performance event loop
        "typing-extensions>=4.0.0",  # Type hints support
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "coverage>=6.0.0",
            "httpx>=0.23.0",  # For testing HTTP requests
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.20.0",
            "httpx>=0.23.0",
            "coverage>=6.0.0",
        ],
        "docs": [
            "mkdocs>=1.4.0",
            "mkdocs-material>=8.0.0",
            "mkdocstrings[python]>=0.19.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "rapid=rapid.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/wesellis/rapid/issues",
        "Source": "https://github.com/wesellis/rapid",
        "Documentation": "https://rapid-api.readthedocs.io/",
    },
    keywords="web framework api fast performance async",
    zip_safe=False,
)
