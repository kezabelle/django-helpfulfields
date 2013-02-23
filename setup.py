# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from helpfulfields import version

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SHORT_DESC = (u'A reusable Django application for viewing and debugging '
              u'all the data that has been pushed into Haystack')

REQUIREMENTS = open(os.path.join(BASE_DIR,
                                 'helpfulfields',
                                 'requirements.txt')).readlines()
REQUIREMENTS = [x.strip() for x in REQUIREMENTS]

TROVE_CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Natural Language :: English',
    'Topic :: Internet :: WWW/HTTP :: Site Management',
    'License :: OSI Approved :: BSD License',
]

PACKAGES = find_packages()

README = open(os.path.join(BASE_DIR, 'README.rst')).read()

setup(
    name='django-helpfulfields',
    version=version,
    description=SHORT_DESC,
    author='Keryn Knight',
    author_email='python-package@kerynknight.com',
    license="BSD License",
    keywords="django",
    long_description=README,
    url='https://github.com/kezabelle/django-helpfulfields/tree/master',
    packages=PACKAGES,
    install_requires=REQUIREMENTS,
    classifiers=TROVE_CLASSIFIERS,
    platforms=['OS Independent'],
)
