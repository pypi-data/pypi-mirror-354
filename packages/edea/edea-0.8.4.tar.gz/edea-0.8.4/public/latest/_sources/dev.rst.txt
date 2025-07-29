Developer documentation
========================

Running the tests
-----------------

The tests should run in the virtualenv to make sure the development tools are there:

.. code-block:: bash

    # outside the poetry environment:
    poetry run pytest
    # or
    poetry shell
    # now we're inside the virtualenv and can run like before, but now with test coverage
    pytest --cov-report term-missing --cov=edea

    # it's also possible to run a single test or a test class
    pytest -k test_parse


Long running test
-----------------

``test_parse_all`` and ``test_serialize_all`` process a lot of KiCad files which
can take a long time. They get by default if the files are not there but
you can enable them by retrieving the files.

.. code-block:: bash

    # the files are in the kicad-test-files git submodule, retrieve them
    git submodule update --init
    # we'd like to parallelize the tests using pytest-xdist to speed things up
    # automatically detecting the optimal number of processes for your machine
    poetry run pytest -n auto

Performance
-----------

.. tip::
    The ``devconainer`` has all required tools for performance optimization.

Profiling
^^^^^^^^^

The `tests/kicad_projects/benchmarks` submodule includes many benchmark files to profile different components of `edea`.
Some targets are in `tests/benchmark` and can run them using the following commands:

|

.. code-block:: bash
    
    poetry shell
    git submodule init tests/kicad_projects/benchmarks && git submodule update --depth 1 tests/kicad_projects/benchmarks
    poe profile --file tests/benchmark/cli_version.py


This profiles the benchmark and opens the `pyinstrument` HTML report in the browser.

Benchmarking
^^^^^^^^^^^^

You can use `hyperfine` for benchmarking the performance of `edea`:

|

.. code-block:: bash

    poetry shell
    git submodule init tests/kicad_projects/benchmarks && git submodule update --depth 1 tests/kicad_projects/benchmarks
    poe benchmark --file tests/benchmark/cli_version.py

This benchmark the benchmark using `hyperfine <https://github.com/sharkdp/hyperfine>`_.`

Continuous benchmarking
^^^^^^^^^^^^^^^^^^^^^^^

You can see continuous benchmarking results at `bencher <https://bencher.dev/perf/edea>`_ . The CI job is in `.gitlab-ci.benchmark.yml`.
