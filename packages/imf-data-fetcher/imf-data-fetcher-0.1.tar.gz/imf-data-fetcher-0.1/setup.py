from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="imf-data-fetcher",
    version="0.1",
    packages=find_packages(),
    description="Interacts with the International Monetary Fund API (SDMX 3.0) to retrieve macroeconomic data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="nndjoli",
    url="https://github.com/nndjoli/imf-data-fetcher",
    install_requires=["pandas", "httpx", "nest_asyncio"],
)
