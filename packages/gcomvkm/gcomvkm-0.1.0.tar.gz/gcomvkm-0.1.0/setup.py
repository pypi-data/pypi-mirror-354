from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gcomvkm",
    version="0.1.0",
    author="Kristina P. Sinaga",
    author_email="kristinasinaga41@gmail.com",
    description="Globally Collaborative Multi-View k-Means Clustering Algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kpsinaga/gcomvkm",
    project_urls={
        "Bug Tracker": "https://github.com/kpsinaga/gcomvkm/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    packages=find_packages(),
    package_data={
        'gcomvkm': ['data/*.mat'],
    },
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.18.0",
        "scipy>=1.4.0",
        "matplotlib>=3.1.0",
        "scikit-learn>=0.22.0",
        "seaborn>=0.11.0"
    ],
    entry_points={
        'console_scripts': [
            'gcomvkm=gcomvkm.cli:main',
        ],
    },
)
