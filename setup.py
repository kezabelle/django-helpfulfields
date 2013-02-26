# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from helpfulfields import version

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SHORT_DESC = (u'A reusable Django application for viewing and debugging '
              u'all the data that has been pushed into Haystack')


def tidy_requirements(requirement_file):
    """
    simplistic parsing of our requirements files to generate dependencies for
    the setup file.
    """
    outdata = []
    with open(requirement_file) as dependencies:
        for line in dependencies:
            line = line.strip()
            if line and not line.startswith('#') and line not in outdata:
                outdata.append(line)
    return outdata

REQUIREMENTS = tidy_requirements(os.path.join(BASE_DIR, 'requirements.txt'))
TEST_REQUIREMENTS = tidy_requirements(os.path.join(BASE_DIR,
                                                   'requirements_dev.txt'))

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
    tests_require=TEST_REQUIREMENTS,
    test_suite='setuptest.setuptest.SetupTestSuite',
    classifiers=TROVE_CLASSIFIERS,
    platforms=['OS Independent'],
)
