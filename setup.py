
from setuptools import setup

CONFIG = {
    'description': 'Jenkins Plugin Install',
    'author': 'Adam Saleh',
    'url': 'URL',
    'author_email': 'asaleh@redhat.com',
    'version': '0.0.1',
    'install_requires': ['requests', 'docopt'],
    'packages': ['jpinstall'],
    'scripts': ['bin/jpi'],
    'name': 'jpinstall'
}

# Add in any extra build steps for cython, etc.

setup(**CONFIG)
