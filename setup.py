from codecs import open
from os import path
from setuptools import setup
from setuptools import find_packages

import codecs


# Workaround for bdist_wininst build on Linux
try:
    codecs.lookup('mbcs')
except LookupError:
    codecs.register(lambda name,
                    enc=codecs.lookup('ascii'):
                    {True: enc}.get(name == 'mbcs'))

# use README as long_description
here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Dependencies
requires = ['lxml>=3.7.3', 'pygdal']
extras = {
    'dev': ['virtualenv'],
    'test': ['check_manifest', 'coverage', 'flake8', 'nose', 'tox']}


setup(
    name="fgdconv",
    version="0.3.0",
    description="FGD GML v4 converter.",
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
    keywords="FGD GIS GML geospatial KIBAN",
    url="https://github.com/miurahr/fgdconv",
    packages=find_packages(exclude=['docs', 'tests']),
    package_data={'fgdconv': ['sax/data/FGD_GMLSchema.xsd']},
    install_requires=requires,
    extras_require=extras,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points="""
        [console_scripts]
        fgdconv=fgdconv.fgd2ogr:main
    """,
)
