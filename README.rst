==========================
Welcome to pytest-ordered!
==========================

A pytest plugin to control the order in which tests are run in.

∘
`MIT license <https://github.com/bwoodsend/pytest-ordered/blob/master/LICENSE>`_
∘
`Source code <https://github.com/bwoodsend/pytest-ordered>`_
∘
`Bug reports <https://github.com/bwoodsend/pytest-ordered/issues>`_
∘
`Support <https://github.com/bwoodsend/pytest-ordered/discussions>`_

``pytest-ordered`` allows you to declare the order in which test files are ran
using the ``pytest.ini``. The order in which individual tests within each file
is left unaltered and defaults each test function's line number.

A similar project, `pytest-order <https://pypi.org/project/pytest-order/>`_,
allows you to order files by adding a ``pytestmark = pytest.mark.order(x)`` line
to each file or decorating each function with ``@pytest.mark.order(x)`` (where
``x`` is some integer enumeration used to sort tests by). I personally didn't
like this design because your configuration is scattered across each file rather
than all in one place and because whenever you need to insert a file into the
middle of your test suite, you need to re-enumerate all the files that come
afterwards... hence this project.


Installation
------------

To install pytest-ordered, run the following in your terminal:

.. code-block:: console

    pip install "git+https://github.com/bwoodsend/pytest-ordered"

.. _PyPI: https://pypi.org/project/pytest-ordered/


Usage
-----

Inside the ``[pytest]`` section of your ``pytest.ini``, list the filenames in
the order you want them to execute:

.. code-block:: ini

    [pytest]
    order =
      - tests/test_foo.py
      - tests/test_bar.py
      - tests/more_tests/test_pop.py

In the spirit of reducing lengthy duplication, in particular when dealing with
sub-directories of tests, an indented line inherits the prefix of the line
before. i.e. The following:

.. code-block:: ini

    [pytest]
    order =
      - tests/
      -   test_
      -     first.py
      -     second.py
      -   sub-tests/test_
      -     third.py
      -     fourth.py
      -   test_fifth.py

is equivalent to but less cumbersome than:

.. code-block:: ini

    [pytest]
    order =
      - tests/test_first.py
      - tests/test_second.py
      - tests/sub-tests/test_third.py
      - tests/sub-tests/test_fourth.py
      - tests/test_fifth.py

For simply laid out test suites (i.e. one ``tests`` directory with no
sub-directories), you can normally just use:

.. code-block:: ini

    [pytest]
    order =
      - tests/test_
      -   foo.py
      -   bar.py
      -   whizz.py


Why order tests?
----------------

This is a philosophy which I'm slightly obsessed with. I believe that it makes
even the biggest, most complicated projects easy to diagnose test failures in.
Hold tight, this is going to be a disproportionately large piece of text. ⛑

If you imagine a reasonably well laid out code project, you can think of it in
layers. You have low level functions which perform basic tasks and reference
little or none of the rest of your code. You have higher level functions which
utilise those low level functions. Then you have more functions on top of those
which use that previous layer of functions and so on until you eventually start
to hit your public API (if you're writing a library), or command line or
graphical interface (if you're writing CLI tool or GUI).

If you intend to preserve your sanity, your test suite will mirror that
structure. i.e. There will be low level tests which test the low level functions
and a gradient of progressively higher level tests testing higher level
functions before ultimately testing real use cases. These high level tests
typically are a lot slower and, if something goes wrong at lower level, a
nightmare to debug. Hence, you always want to catch and debug failures at the
lowest possible level.

Now then, suppose that something changes so that one of those low level
functions is now broken. This can be due to anything from trying a new operating
system/version or Python version to a dependency being updated or some
refactoring being done. Because that low level function will be used by other
functions, those other functions will also likely be broken meaning that huge
numbers of tests will fail. ``pytest`` will go nuts and print several kilometres
worth of stack-traces whilst you stare in despair at it before ultimately
resigning yourself to trudging through the failures, looking to group similar
stack-traces before picking a failure at random and debugging it.

Alternatively, if your tests are deliberately ordered so that they run low level
tests first, then progress up the stack until they reach the complex, end usage
type tests and if you use::

    pytest -x

then the test to fail (and abort the test run) will be the test which
corresponds to the broken function. Because it tests that function directly
rather than testing some other function which depends on the former, that test
is your simplest and quickest possible reproducer of the bug. Additionally,
since all tests before have passed, you know that any lower level functions the
broken uses are unlikely to be the cause of the failure as their tests have
already run. Unless you're in the habit of writing very long functions, this
probably only leaves you with a few lines of previously untested code in which
to search for the bug. Quite often, I find that I can diagnose and fix a failure
without even looking at the traceback - just knowing which test pytest halted on
is enough. This knowing which lines of code to suspect is extremely valuable
if you're diagnosing something remotely on CI/CD which you can't reproduce
on a machine in front of you.

After you've fixed the first failure with surprising ease, you can go back to
running ``pytest -x`` until the whole suite passes.
