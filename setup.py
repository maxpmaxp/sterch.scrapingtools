import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='sterch.scrapingtools',
    version='0.7.11',
    url='http://sterch.net',
    license='ZPL',
    description='Library for building scrapers',
    author='Polshcha Maksym',
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
      'zope.schema',
      'setuptools',
     ],
    zip_safe=False,
    include_package_data=True
)
