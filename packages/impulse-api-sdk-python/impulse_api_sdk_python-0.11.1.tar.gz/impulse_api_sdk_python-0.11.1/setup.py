from setuptools import setup, find_packages

# Read README.md file for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from VERSION file
with open("VERSION", "r", encoding="utf-8") as fh:
    version = fh.read()

# Read requirements from requirements.txt file
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

# Setup configuration
setup(
    name="impulse-api-sdk-python",
    version=version,
    author="Impulse Labs AI",
    author_email="engg@impulselabs.ai",
    license="MIT",
    description="A Python SDK for interacting with the Impulse Labs API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/impulselabs/api-sdk-python",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=requirements,
)