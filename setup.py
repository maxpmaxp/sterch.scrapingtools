import os
import sys
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='sterch.scrapingtools',
    version='0.2.9',
    url='http://pypi.sterch.net',
    license='ZPL',
    description='Library for building scrapers',
    author='Polsha Maxim',
    author_email='maxp@sterch.net',
    long_description='\n\n'.join([
        open('README.txt').read()
        ]),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'': ['*.*']},
    namespace_packages=['sterch'],
    install_requires=[
      'zope.component',
      'setuptools',
     ],
    zip_safe=False,
    include_package_data=True
)
