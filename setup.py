import codecs

from os import path
from setuptools import find_packages, setup


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()


setup(
    author="",
    author_email="",
    description="",
    name="pinax-wiki",
    long_description=read("README.rst"),
    version=__import__("wiki").__version__,
    url="http://pinax-wiki.rtfd.org/",
    license="MIT",
    packages=find_packages(),
    tests_require=[
        "Django>=1.4",
    ],
    install_requires=[
        "django-appconf>=0.6",
        "django-user-accounts>=1.0c9",
        "creole>=1.2"
    ],
    test_suite="runtests.runtests",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
