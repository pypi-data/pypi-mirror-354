from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PyConnectTelnet",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="hxk",
    description="Connect command channels by entering commands to query log data。",
    long_description_content_type="text/markdown",
    long_description=long_description,
)
