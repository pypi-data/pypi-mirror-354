# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cli', 'utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.8,<9.0.0', 'evergreen-py>=3.10.6,<4.0.0']

entry_points = \
{'console_scripts': ['analyze-patch = cli.analyze_patch:main',
                     'viewless-suites = cli.viewless_suites:main']}

setup_kwargs = {
    'name': 'evergreen-scripts',
    'version': '0.4.1',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
