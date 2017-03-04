from codecs import open
from os import path
from setuptools import setup
from setuptools import find_packages


here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

requires = ['lxml>=3.7.3']
extras = {
    'dev': ['virtualenv'],
    'test': ['check_manifest', 'coverage', 'flake8', 'nose', 'tox']}

setup(
    name="jpgisgml2gml",
    version="0.1.0",
    description="JPGIS(GML) v4 to GML converter.",
    author="Hiroshi Miura",
    author_email="miurahr@linux.com",
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: Text Processing',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords="GIS GML geospatial KIBAN",
    url="https://github.com/miurahr/jpgisv4togml",
    packages=find_packages(exclude=['docs', 'tests']),
    package_data={'jpgisgml2gml': ['data/FGD_GMLSchema.xsd']},
    install_requires=requires,
    extras_require=extras,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points="""
        [console_scripts]
        jpgisgml2gml=cli:main
    """,
)
