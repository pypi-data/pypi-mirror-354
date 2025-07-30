import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="InitDecaytor",
    version="0.1.2",
    author="Kevin De Bruycker and Stijn D'hollander",
    author_email="kevindebruycker@gmail.com",
    description="Simulation of the thermal decomposition of free-radical initiators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    license="MIT License",
    packages=setuptools.find_packages(),
    install_requires=[
        "dash",
        "matplotlib",
        "numba",
        "numpy",
        # "openpyxl",
        "pandas",
        "plotly",
        "scipy",
        # "statsmodels",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)