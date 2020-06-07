# Cumulator overview

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

# Installation

::

    pip install cumulator

You can also install the in-development version with::

    pip install https://github.com/tristantreb/cumulator/archive/master.zip


# Documentation

An API to evaluate the carbon footprint of communication costs between two nodes of a network

## Background
Current researchers produce methods and tools to evaluate and optimize the efficiency (from both time and spatial scales) of large-scale ML computations.
MLbench focus on distributed ML. One of its objective is to provide a way to benchmark ML algorithms.

## Objectives
* For the MLO: add a environmental impact concern into MLBench
* Immediate application with AlgE: find an optimal network topology to perform the trainings of medical datasets distributed between different data centers in Africa, with this environmental impact point of view

## Method
Create Cumulator, an API to evaluate the carbon footprint of communication costs between two nodes of a network
Hypothesis: checkpoint files is typically the kind of files which will be exchanges between nodes of a distributed ML algorithm.
I did a test on an image classification problem with CNN on MNIST. I used cumulator to compute the carbon footprint of loading the checkpoints file.

## Results (to be extended depending on the needs of the MLO)
At the moment Cumulator has the following functionalities: 

* Chronometer activation and deactivation
* Time aggregation (cumulative time of activation/deactivation) per instance of the cumulator class
* Display of the carbon footprint
Hence, to compare n different network topologies, one can create n cumulator instance and display the relative carbon footprint after computation.
