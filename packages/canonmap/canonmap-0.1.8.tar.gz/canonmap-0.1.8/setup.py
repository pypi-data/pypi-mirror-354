from setuptools import setup, find_packages, Command
import subprocess
import sys

class DownloadSpacyModel(Command):
    description = "Download spaCy model"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        except subprocess.CalledProcessError:
            print("Warning: Failed to download spaCy model. You may need to run 'python -m spacy download en_core_web_sm' manually.")

setup(
    name="canonmap",
    version="0.1.8",
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
    cmdclass={
        'download_spacy': DownloadSpacyModel,
    },
) 