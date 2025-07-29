from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rio_config",
    version="0.1.1",
    description="Rio Config data parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/perfecto25/rio_config",
    author="mike.reider",
    author_email="mike.reider@gmail.com",
    license="MIT",
    packages=["rio_config"],
    zip_safe=True,
)