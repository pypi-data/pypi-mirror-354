from setuptools import setup, find_packages
import subprocess
import sys

def download_spacy_model():
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    except subprocess.CalledProcessError:
        print("Warning: Failed to download spaCy model. You may need to run 'python -m spacy download en_core_web_sm' manually.")

setup(
    name="canonmap",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "spacy>=3.7.2",
        "rapidfuzz",
        "Metaphone",
        "scikit-learn",
        "chardet",
        "torch",
    ],
    author="Vince Berry",
    author_email="vince.berry@gmail.com",
    description="CanonMap - A Python library for entity canonicalization and mapping",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vinceberry/canonmap",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
)

# Run post-install script
download_spacy_model() 