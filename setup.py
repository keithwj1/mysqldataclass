import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mysqldataclass",
    version="0.0.1",
    author="Keith Jones",
    author_email="keithwj1@gmail.com",
    description="Allows easy creation of data objects from a database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XeonZenn/MeggittProjects",
    project_urls={
        "Bug Tracker": "https://github.com/XeonZenn/MeggittProjects/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)