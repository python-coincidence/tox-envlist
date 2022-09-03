############
tox-envlist
############

.. start short_desc

**Allows selection of a different tox envlist.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/python-coincidence/tox-envlist/workflows/Linux/badge.svg
	:target: https://github.com/python-coincidence/tox-envlist/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/python-coincidence/tox-envlist/workflows/Windows/badge.svg
	:target: https://github.com/python-coincidence/tox-envlist/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/python-coincidence/tox-envlist/workflows/macOS/badge.svg
	:target: https://github.com/python-coincidence/tox-envlist/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/python-coincidence/tox-envlist/workflows/Flake8/badge.svg
	:target: https://github.com/python-coincidence/tox-envlist/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/python-coincidence/tox-envlist/workflows/mypy/badge.svg
	:target: https://github.com/python-coincidence/tox-envlist/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/python-coincidence/tox-envlist/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/python-coincidence/tox-envlist/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/python-coincidence/tox-envlist/master?logo=coveralls
	:target: https://coveralls.io/github/python-coincidence/tox-envlist?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/python-coincidence/tox-envlist?logo=codefactor
	:target: https://www.codefactor.io/repository/github/python-coincidence/tox-envlist
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/tox-envlist
	:target: https://pypi.org/project/tox-envlist/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/tox-envlist?logo=python&logoColor=white
	:target: https://pypi.org/project/tox-envlist/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/tox-envlist
	:target: https://pypi.org/project/tox-envlist/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/tox-envlist
	:target: https://pypi.org/project/tox-envlist/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/python-coincidence/tox-envlist
	:target: https://github.com/python-coincidence/tox-envlist/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/python-coincidence/tox-envlist
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/python-coincidence/tox-envlist/v0.3.0
	:target: https://github.com/python-coincidence/tox-envlist/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/python-coincidence/tox-envlist
	:target: https://github.com/python-coincidence/tox-envlist/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2022
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/tox-envlist
	:target: https://pypi.org/project/tox-envlist/
	:alt: PyPI - Downloads

.. end shields


Configuration
----------------

In your ``tox.ini`` file, add the following:

.. code-block:: ini

	[envlists]
	test = py36, py37, py38
	qa = mypy,lint
	cov = py36,coverage

This will configure three envlists:

* **test**, which runs the environments ``py36``, ``py37`` and ``py38``
* **qa**, which runs the environments ``mypy`` and ``lint``
* **cov**, which runs the environments ``py36`` and ``coverage``

You are free to customise these envlists and add new ones.


Usage
-------

Run tox using the ``-n`` / ``--envlist-name [name]`` option, where ``name`` is the name of the envlist.


Installation
--------------

.. start installation

``tox-envlist`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install tox-envlist

.. end installation

``tox-envlist`` requires Python 3.7 or later to run,
but can be used to configure envlists which use earlier Python version.
