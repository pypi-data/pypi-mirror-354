from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lax-nats-client",
    version="0.2.2",
    author="Rahul Lamba",
    author_email="rahul2lamb@gmail.com",
    description="Smart client SDK for LAX NATS JetStream broker with automatic routing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/lambdax2/lambdax-development/lax-nats-jetstream",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
    ],
    python_requires=">=3.8",
    install_requires=[
        "nats-py>=2.6.0",
        "grpcio>=1.60.0",
        "grpcio-tools>=1.60.0",
        "protobuf>=4.25.0",
        "prometheus-client>=0.19.0",
        "tenacity>=8.2.0",  # For retry logic
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "mypy>=1.7.0",
        ],
        "fastapi": [
            "fastapi>=0.104.0",
            "uvicorn>=0.24.0",
        ],
    },
)