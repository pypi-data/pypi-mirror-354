# setup.py
from setuptools import setup, find_packages
import os
import re # Import re for a more robust parsing

# Function to read the version from __init__.py
def get_version(package_name):
    version_file = os.path.join(package_name, '__init__.py')
    with open(version_file, 'r') as f:
        version_match = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Version string not found in {}.".format(version_file))

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="necta-fetcher",
    version=get_version("necta_fetcher"), # Read version from package
    author="Someless", # Replace with your name/alias
    author_email="adosomeless@gmail.com", # Replace with your email
    description="A Python client to fetch NECTA (National Examinations Council of Tanzania) results with names.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://boyoftime.github.io/necta-fetcher",  # Replace with your project's URL if you have one
    project_urls={
        "Bug Tracker": "https://boyoftime.github.io/necta-fetcher", # Replace
    },
    license="MIT", # Or another license of your choice
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*", "example_usage.py"]),
    install_requires=[
        "requests>=2.20.0",
        "beautifulsoup4>=4.9.0"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords="necta results tanzania education examination fetcher scraper api client",
)