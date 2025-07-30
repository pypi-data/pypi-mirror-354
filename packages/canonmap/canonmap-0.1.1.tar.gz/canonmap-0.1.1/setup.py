from setuptools import setup, find_packages

setup(
    name="canonmap",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "spacy",
        "rapidfuzz",
        "Metaphone",
        "scikit-learn",
        "chardet",
    ],
    author="Vince Berry",
    author_email="vince.berry@example.com",  # Please replace with your actual email
    description="CanonMap - A Python library for data mapping and canonicalization",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vinceberry/canonmap",  # Please replace with your actual repo URL
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