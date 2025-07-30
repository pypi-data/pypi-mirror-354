from setuptools import setup, find_packages

setup(
    name="csb_validator",
    version="0.1.0",
    description="Validate CSB (Crowdsourced Bathymetry) GeoJSON and other formats",
    author="Your Name",
    author_email="you@example.com",
    url="https://github.com/yourusername/csb_validator",
    packages=find_packages(),
    install_requires=[
        "json",
        "asyncio",
        "os",
        "sys",
        "datetime",
        "typing",
        "aiofiles",
        "setuptools"
    ],
    entry_points={
        "console_scripts": [
            "csb-validator=csb_validator.validator:main", 
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)