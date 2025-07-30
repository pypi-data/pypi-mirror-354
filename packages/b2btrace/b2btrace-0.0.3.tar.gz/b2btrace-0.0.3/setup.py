#this is a setup.py file
from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'BAM-to-barcode tracing of sequences'
LONG_DESCRIPTION = 'Python package that enables tracing target sequences and retrieving the correspond cell barcodes in single-cell experiments. https://github.com/BKover99/b2btrace '


setup(
    name="b2btrace",
    version=VERSION,
    author="Bence Kover",
    author_email="<kover.bence@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[
	'numpy',
	'pandas'
	],
    extras_require={
        "external": ["samtools"]
    },
    keywords=['samtools','singlecell','barcode','bam'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X"
    ]
)

