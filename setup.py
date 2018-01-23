from setuptools import find_packages, setup

VERSION = "1.0.0"
LONG_DESCRIPTION = """
.. image:: http://pinaxproject.com/pinax-design/patches/blank.svg
    :target: https://pypi.python.org/pypi/pinax-wiki/

==========
Pinax Wiki
==========

.. image:: https://img.shields.io/pypi/v/pinax-wiki.svg
    :target: https://pypi.python.org/pypi/pinax-wiki/

\ 

.. image:: https://img.shields.io/circleci/project/github/pinax/pinax-wiki.svg
    :target: https://circleci.com/gh/pinax/pinax-wiki
.. image:: https://img.shields.io/codecov/c/github/pinax/pinax-wiki.svg
    :target: https://codecov.io/gh/pinax/pinax-wiki
.. image:: https://img.shields.io/github/contributors/pinax/pinax-wiki.svg
    :target: https://github.com/pinax/pinax-wiki/graphs/contributors
.. image:: https://img.shields.io/github/issues-pr/pinax/pinax-wiki.svg
    :target: https://github.com/pinax/pinax-wiki/pulls
.. image:: https://img.shields.io/github/issues-pr-closed/pinax/pinax-wiki.svg
    :target: https://github.com/pinax/pinax-wiki/pulls?q=is%3Apr+is%3Aclosed

\ 

.. image:: http://slack.pinaxproject.com/badge.svg
    :target: http://slack.pinaxproject.com/
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT

\ 

``pinax-wiki`` lets you easily add a wiki to your Django site.

Supported Django and Python Versions
------------------------------------

+-----------------+-----+-----+-----+-----+
| Django / Python | 2.7 | 3.4 | 3.5 | 3.6 |
+=================+=====+=====+=====+=====+
|  1.11           |  *  |  *  |  *  |  *  |
+-----------------+-----+-----+-----+-----+
|  2.0            |     |  *  |  *  |  *  |
+-----------------+-----+-----+-----+-----+
"""
   
setup(
    author="Pinax Team",
    author_email="team@pinaxproject.com",
    description="a wiki app for Django sites",
    name="pinax-wiki",
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    url="http://github.com/pinax/pinax-wiki/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "pinax_wiki": []
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "django>=1.11",
        "django-appconf>=1.0.1",
        "python-creole>=1.3.1"
    ],
    tests_require=[
    ],
    test_suite="runtests.runtests",
    zip_safe=False
)
