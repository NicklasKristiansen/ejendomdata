from setuptools import setup, find_packages



setup(
    name="dkejendomme",
    version="0.1.0",
    description="Et bibliotek til ejendomsdata og funktioner",
    packages=find_packages(),  # Finder automatisk 'dkejendomme'
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
