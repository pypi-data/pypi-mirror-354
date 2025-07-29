from setuptools import setup, find_packages

setup(
    name="evolvishub_sqlite_adapter",
    version="0.1.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "aiosqlite>=0.19.0",
        "pandas>=2.0.0",
        "sqlalchemy>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.1.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "ruff>=0.1.0",
            "build>=1.0.0",
            "wheel>=0.42.0"
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
            "sphinx-autodoc-typehints>=1.24.0"
        ]
    },
    author="Alban Maxhuni, PhD",
    author_email="a.maxhuni@evolvis.ai",
    description="A robust SQLite adapter with both synchronous and asynchronous interfaces",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/evolvis/evolvishub-sqlite-adapter",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",
)

if __name__ == "__main__":
    setup() 