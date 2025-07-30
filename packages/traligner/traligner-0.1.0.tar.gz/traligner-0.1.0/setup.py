from setuptools import setup, find_packages

setup(
    name="traligner",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "numpy",
        "pandas",
        "Levenshtein",
        "python-hebrew-numbers",
        "trelasticext",  # Your previously published package
        "regex",
        "fasttext",  # Only if needed for core functionality
    ],
    python_requires=">=3.6",
    url="https://github.com/millerhadar/traligner",  # Fixed URL with your actual GitHub username
    project_urls={
        "Bug Tracker": "https://github.com/millerhadar/traligner/issues",
        "Documentation": "https://github.com/millerhadar/traligner",
        "Source Code": "https://github.com/millerhadar/traligner",
    },
    description="A text alignment library with special support for Hebrew texts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)