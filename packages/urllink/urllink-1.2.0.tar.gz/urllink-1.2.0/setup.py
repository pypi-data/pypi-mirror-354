from setuptools import setup, find_packages

# Read the content of README.md to use as the long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="urllink",
    version="1.2.0",
    author="Muhammad Hamza Shahzad",
    author_email="myhamza.204@gmail.com",
    description="A Python library for URL shortening and QR code generation.",
    long_description=long_description,  # Now correctly included
    long_description_content_type="text/markdown",
    url="https://urllink.site",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
)
