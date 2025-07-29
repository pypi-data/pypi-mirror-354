from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="random-delay",
    version="1.0.0",
    author="Abderrahim GHAZALI",
    author_email="ghazali.abderrahim1@gmail.com",
    description="Create random delays for rate limiting, jitter, or testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abderrahimghazali/random-delay",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "typing-extensions>=3.7.4; python_version<'3.8'",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
            "mypy>=0.910",
        ],
        "cli": [
            "click>=8.0.0",
            "rich>=12.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "random-delay=random_delay.cli:main",
        ],
    },
    keywords=["delay", "rate-limiting", "jitter", "testing", "async", "random"],
)
