from setuptools import setup, find_packages

setup(
    name="CRC_API",                                # This is the PyPI name
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Python wrapper for the CRC 1625 MatInf VRO API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.ruhr-uni-bochum.de/icams-mids/crc1625rdmswrapper/-/tree/Doaa?ref_type=heads",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
