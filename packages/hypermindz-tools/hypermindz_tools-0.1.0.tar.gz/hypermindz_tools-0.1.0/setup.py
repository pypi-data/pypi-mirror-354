from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hypermindz-tools",
    version="0.1.0",
    author="Hypermindz Team",
    description="A collection of tools for AI workflows by Hypermindz.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hypermindz-tools",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "crewai>=0.76.2",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
    },
)
