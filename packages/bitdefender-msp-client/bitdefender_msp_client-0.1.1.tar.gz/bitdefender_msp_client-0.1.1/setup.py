import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bitdefender-msp-client",
    version="0.1.1",
    author="My Son",
    description="Python client for Bitdefender MSP API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sonpd2/bitdefender-msp-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
)