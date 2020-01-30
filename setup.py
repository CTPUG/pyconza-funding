import sys

from setuptools import find_packages, setup

REQUIRES = [
    'wafer >= 0.7.0',
]

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name="pyconza_funding",
    version="0.1.0",
    url='http://github.com/CTPUG/pyconza-funding',
    license='ISC',
    description="A Funding application for PyCon ZA for use with wafer.",
    long_description=long_description,
    author='CTPUG',
    author_email='ctpug@googlegroups.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIRES,
    setup_requires=[
        # Add setuptools-git, so we get correct behaviour for
        # include_package_data
        'setuptools_git >= 1.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
