from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="zionai_utils",  
    version="1.2.0",
    author="Harshith Gundela",
    author_email="harshith.gundela@zionclouds.com",
    description="Enterprise AI utilities for Google Cloud Storage and Secrets Manager operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZionClouds/zionai-utils",  
    packages=find_packages(exclude=["tests*", "examples*"]),
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
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Systems Administration",
    ],
    license="MIT",
    python_requires=">=3.7",
    install_requires=requirements,
    keywords=[
        "google-cloud-storage", 
        "gcs", 
        "secrets-manager", 
        "google-cloud", 
        "utility", 
        "zionai",
        "enterprise",
        "ai",
        "cloud"
    ],
    project_urls={
        "Bug Reports": "https://github.com/ZionClouds/zionai-utils/issues",
        "Source": "https://github.com/ZionClouds/zionai-utils",
        "Documentation": "https://pypi.org/project/zionai-utils/",
    },
)