from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hashkit",
    version="1.0.0",
    author="AbderrahimGHAZALI",
    author_email="ghazali.abderrahim1@gmail.com",
    description="Professional hash identification and cracking tool for security professionals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abderrahimghazali/hashkit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "colorama>=0.4.6",
        "passlib>=1.7.4",
        "bcrypt>=4.0.0",
        "pycryptodome>=3.15.0",
        "tabulate>=0.9.0",
        "tqdm>=4.64.0",
        "pyyaml>=6.0",
        "requests>=2.28.0",
    ],
    extras_require={
        "gpu": [
            "pyopencl>=2022.2",  # For GPU acceleration
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "hashkit=hashkit.cli:main",
        ],
    },
    keywords=["security", "hashing", "password-cracking", "cryptography", "forensics"],
)