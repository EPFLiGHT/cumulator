========
Overview
========

An API to evaluate the carbon footprint of computation and communcation of machine learning methods (or any other computing system).


.. start-badges

.. list-table::
    :stub-columns: 1

    * - package
      - | |version|
        | |commits-since|

.. |version| image:: https://img.shields.io/pypi/v/cumulator.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/cumulator

.. |commits-since| image:: https://img.shields.io/github/commits-since/tristantreb/cumulator/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/tristantreb/cumulator/compare/v0.0.0...master

.. end-badges


Background
__________
Current researchers produce methods and tools to evaluate and optimize the efficiency (from both time and spatial scales) of large-scale ML computations.

Aim
__________
Raise awareness about the carbon footprint of machine learning methods and to encourage further optimization and the rationale use of AI-powered tools

Method
__________
Create Cumulator, a simple API to evaluate the carbon footprint of communication and computation of a machine learning models which provides effortless integration within any python framework.


* Free software: MIT license

Installation
============

Use the following command:

    pip install cumulator


Functionalities
=============
At the moment Cumulator has the following functionalities: 

* Chronometer activation and deactivation
* Time aggregation (cumulative time of activation/deactivation) per instance of the cumulator class
* Display of the carbon footprint
Hence, to compare n different network topologies, one can create n cumulator instance and display the relative carbon footprint after computation.

Test
=============
Cumulator was integrated within the Alg-E platform
