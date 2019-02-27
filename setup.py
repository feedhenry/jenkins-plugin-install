# -*- coding: utf-8 -*-
"""``jpinstall`` is a CLI utility.

It lives in `Feedhenry organization <https://github.com/feedhenry/jenkins-plugin-install>`_.
"""

from setuptools import setup

CONFIG = {
    'description': 'Jenkins Plugin Install',
    'author': 'Adam Saleh',
    'url': 'URL',
    'author_email': 'adam@asaleh.net',
    'version': '0.0.1',
    'install_requires': ['requests', 'docopt'],
    'packages': ['jpinstall'],
    'scripts': ['bin/jpi'],
    'name': 'jpinstall'
}

setup(**CONFIG)
