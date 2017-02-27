import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "jpgis-converter",
    version = "0.0.1",
    author = "",
    author_email = "",
    description = ("JPGIS(GML) v4 to GML converter."),
    license = "MIT",
    keywords = "JPGIS GML geo",
    url = "",
    packages=['jpgis-converter'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    data_files=[('', ['jpgis-converter/FGD_GMLSchema.xsd'])]
)
