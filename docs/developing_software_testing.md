# DCR - Developing - Software Testing

![Coveralls GitHub](https://img.shields.io/coveralls/github/KonnexionsGmbH/dcr.svg)
![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/KonnexionsGmbH/dcr/0.9.1)

----

[pytest](https://github.com/pytest-dev/pytest){:target="_blank"} is used as a software testing framework with the following plugins::

- [pytest-cov](https://github.com/pytest-dev/pytest-cov){:target="_blank"} for coverage reporting,
- [pytest-deadfixture](https://github.com/jllorencetti/pytest-deadfixtures){:target="_blank"} to list unused or duplicate fixtures, and
- [pytest-random-order](https://github.com/jbasko/pytest-random-order){:target="_blank"} to randomise the order of the tests.

On the one hand, the tests must be as complete as possible, i.e. a test coverage of 100% is aimed for, but on the other hand, the scope of the test code should be minimal, i.e. unnecessary repetitions must be strictly avoided. 
The best strategy for this is to first create a test case for the normal case and then add special tests for the special cases not yet covered.

Finally, the tool [Coveralls for Python](https://github.com/TheKevJames/coveralls-python){:target="_blank"} is used to enable a connection to [Coveralls](https://coveralls.io/github/KonnexionsGmbH/dcr){:target="_blank"}.
