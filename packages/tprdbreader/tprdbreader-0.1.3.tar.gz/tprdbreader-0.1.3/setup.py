# setup.py
from setuptools import setup, find_packages

setup(
    name="tprdbreader",            # Name of your package
    version="0.1.3",               # Initial release version
    packages=find_packages(),      # Automatically find packages in the directory
    install_requires=[             # List of dependencies that will be installed via pip
        "pandas",
        "google-cloud-storage",
    ],
    author="Devisri",
    author_email="bandarudevisri.ds@gmail.com",
    description="A library to read Translation Process Research Database (TPR-DB) tables from Google Cloud Storage.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",        
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
