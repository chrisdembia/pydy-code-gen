#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pydy-code-gen',
    version='0.1.0dev',
    author='Jason K. Moore',
    author_email='moorepants@gmail.com',
    url="https://github.com/PythonDynamics/pydy-code-gen/",
    description='Code generation for multibody dynamic systems.',
    long_description=open('README.rst').read(),
    keywords="dynamics multibody simulation code generation",
    license='LICENSE.txt',
    packages=find_packages(),
    install_requires=['sympy>=0.7.3',
                      'numpy>=1.6',
                      'scipy>=0.9',
                      'Theano>=0.6.0rc3',
                      'Cython>=0.15.1'],
    extras_require={'doc': ['sphinx', 'numpydoc']},
    tests_require=['nose'],
    test_suite='nose.collector',
    include_package_data=True,
    classifiers=[
                 'Development Status :: 2 - Pre-Alpha',
                 'Intended Audience :: Science/Research',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: Scientific/Engineering :: Physics',
                ],
)
