pytest-unique
=============

`Pytest <http://pytest.org>`_ fixture to generate unique values.

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/cr3/pytest-unique/blob/master/LICENSE
   :alt: License
.. image:: https://img.shields.io/pypi/v/pytest-unique.svg
   :target: https://pypi.python.org/pypi/pytest-unique/
   :alt: PyPI
.. image:: https://img.shields.io/github/issues-raw/cr3/pytest-unique.svg
   :target: https://github.com/cr3/pytest-unique/issues
   :alt: Issues

Requirements
------------

You will need the following prerequisites to use pytest-unique:

- Python 3.9, 3.10, 3.11, 3.12, 3.13

Installation
------------

To install pytest-unique:

.. code-block:: bash

  $ pip install pytest-unique

Usage
-----

You can use the ``unique`` fixture by passing it as a test argument:

.. code-block:: python

  def test_integer(unique):
      assert unique("integer") > 0

Here are some of the plugins available by default:

* ``bytes`` with invalid UTF8 characters.
* ``digits`` with just numbers.
* ``email`` with a unique username.
* ``float`` with a whole part and a decimal part.
* ``integer`` with ``base`` and ``mod`` arguments.
* ``password`` with ``lowercase``, ``uppercase``, ``digits`` and
  ``punctuation`` arguments.
* ``text`` with ``prefix``, ``suffix`` and ``separator`` arguments.

Extensions
----------

The ``unique`` fixture can be extended with custom plugins:

.. code-block:: python

  from datetime import datetime, timezone

  def unique_datetime(unique)
      """Return a datetime unique to this factory instance."""
      timestamp = unique("integer")
      return datetime.fromtimestamp(timestamp, timezone.utc)

Then, add it to the ``pyproject.toml`` file of your project:

.. code-block:: text

  [tool.poetry.plugins."pytest_unique"]
  datetime = "your_project.unique:unique_datetime"

You can then use the plugin like all other plugins:

.. code-block:: python

  from datetime import datetime

  def test_datetime(unique):
      assert isinstance(unique("datetime"), datetime)


Limitations
-----------

The ``unique`` fixture cannot be used as parameters in parameterized tests
by virtue of being a fixture. The reason it is a fixture rather than a
function is that unique values are generated from an instance of a counter
that returns sequential values. This makes it possible to see the order
in which values were generated which can be useful when troubleshooting.

Resources
---------

- `Documentation <https://cr3.github.io/pytest-unique/>`_
- `Release Notes <http://github.com/cr3/pytest-unique/blob/master/CHANGES.rst>`_
- `Issue Tracker <http://github.com/cr3/pytest-unique/issues>`_
- `Source Code <http://github.com/cr3/pytest-unique/>`_
- `PyPi <https://pypi.org/project/pytest-unique/>`_
