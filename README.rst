========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/cumulator/badge/?style=flat
    :target: https://readthedocs.org/projects/cumulator
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/tristantreb/cumulator.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/tristantreb/cumulator

.. |codecov| image:: https://codecov.io/gh/tristantreb/cumulator/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/tristantreb/cumulator

.. |version| image:: https://img.shields.io/pypi/v/cumulator.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/cumulator

.. |wheel| image:: https://img.shields.io/pypi/wheel/cumulator.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/cumulator

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/cumulator.svg
    :alt: Supported versions
    :target: https://pypi.org/project/cumulator

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/cumulator.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/cumulator

.. |commits-since| image:: https://img.shields.io/github/commits-since/tristantreb/cumulator/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/tristantreb/cumulator/compare/v0.0.0...master



.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: MIT license

Installation
============

::

    pip install cumulator

You can also install the in-development version with::

    pip install https://github.com/tristantreb/cumulator/archive/master.zip


Documentation
=============


https://cumulator.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
