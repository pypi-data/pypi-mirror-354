# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['honeyshare', 'honeyshare.api']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'honeyshare',
    'version': '0.1.0',
    'description': 'Python API client for HoneyShare.live',
    'long_description': None,
    'author': 'Pedro Melgueira',
    'author_email': 'pedromelgueira@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
