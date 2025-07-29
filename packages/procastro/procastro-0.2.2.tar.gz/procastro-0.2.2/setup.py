# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['procastro',
 'procastro.astro',
 'procastro.astro.tests',
 'procastro.core',
 'procastro.core.tests',
 'procastro.obsrv',
 'procastro.obsrv.deprecated',
 'procastro.obsrv.tests',
 'procastro.photography',
 'procastro.tests',
 'procastro.timeseries',
 'procastro.timeseries.example',
 'procastro.timeseries.tests']

package_data = \
{'': ['*'],
 'procastro': ['defaults/*'],
 'procastro.astro': ['images/*'],
 'procastro.core.tests': ['data/*'],
 'procastro.obsrv': ['doc/*'],
 'procastro.timeseries.example': ['data/*', 'data/raw/*']}

install_requires = \
['ExifRead>=3.0.0,<4.0.0',
 'asdf-astropy>=0.4.0,<0.5.0',
 'astropy>=6,<7',
 'astroquery>=0.4.6,<0.5.0',
 'cartopy>=0.23.0,<0.24.0',
 'lxml>=5.2.1,<6.0.0',
 'matplotlib>=3.5.3,<4.0.0',
 'numpy>=1.23.2,<2.0.0',
 'pandas>=2,<3',
 'pyvo>=1.3,<2.0',
 'scipy>=1.9.1,<2.0.0',
 'tomli>=2.0.1,<3.0.0',
 'tomli_w>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'procastro',
    'version': '0.2.2',
    'description': 'Framework to process astronomical data files',
    'long_description': '# procastro\n\n**Saving time for astronomers handling data everywhere**\n\nprocastro is a framework created to intuitively handle astronomical data files\nin an pythonic style\n\n\n\n\n## Installation\n\nYou can install procastro by using pip\n\n\t$ pip install procastro\n\n## Documentation\n\nPlease, check https://procastro.readthedocs.io/en/latest/\n\n',
    'author': 'Patricio Rojo',
    'author_email': 'pato@das.uchile.cl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/duckrojo/procastro',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
