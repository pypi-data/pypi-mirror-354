from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zionai_utils",  
    version="1.1.0",
    author="Harshith Gundela",
    author_email="harshith.gundela@zionclouds.com",
    description="A simple utility library for Google Cloud Storage operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZionClouds/ZionAI-utils.git",  
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    license="MIT",
    python_requires=">=3.7",
    install_requires=[
        "google-cloud-storage>=2.0.0",
    ],
    keywords="google-cloud-storage gcs upload utility",
)