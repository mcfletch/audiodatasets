#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'numpy',
    'librosa>=0.5.0',
    'sounddevice',
    'soundfile',
    'sphfile',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='audiodatasets',
    version='1.0.0',
    description="Pulls and pre-processes major Open Source (non-commercial mostly) datasets for spoken audio",
    long_description=readme,
    author="Mike C. Fletcher",
    author_email='mcfletch@vrplumber.com',
    url='https://github.com/mcfletch/audiodatasets',
    packages=[
        'audiodatasets',
    ],
    package_dir={'audiodatasets':
                 'audiodatasets'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='audiodatasets',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'audiodatasets-download=audiodatasets.preprocess:download',
            'audiodatasets-preprocess=audiodatasets.preprocess:preprocess',
            'audiodatasets-search=audiodatasets.searchwords:main',
        ],
    },
)
