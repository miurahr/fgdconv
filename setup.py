import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "jpgisgml2gml",
    version = "0.0.1",
    author = "mizutuu",
    author_email = "",
    description = ("JPGIS(GML) v4 to GML converter."),
    license = "MIT License",
    keywords = "JPGIS GML geo GSI",
    url = "",
    packages=['jpgisgml2gml'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    package_data={'jpgisgml2gml': ['data/FGD_GMLSchema.xsd']},
   install_requires=['lxml'],
    entry_points="""
        [console_scripts]
        jpgisgml2gml=jpgisgml2gml:main
    """,
)
