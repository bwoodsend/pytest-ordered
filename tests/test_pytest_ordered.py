from pathlib import Path
import shutil

import pytest_ordered


def test_expand_test_order():
    out = pytest_ordered.expand_test_order("""
        - foo/
        -     bar
        -     baz_
        -         pop
        - lemon/cake
    """)
    assert out == ["foo/", "foo/bar", "foo/baz_", "foo/baz_pop", "lemon/cake"]


MOCK_PROJECT = Path(__file__, "../../mock-project").resolve()


def test_hello_ini_setting(pytester):
    shutil.copytree(
        MOCK_PROJECT / "tests", pytester.path / "tests",
        ignore=lambda _, names: [i for i in names if i == "__pycache__"])

    pytester.makefile(".ini", pytest="")
    result = pytester.runpytest_subprocess('-vs')
    assert result.ret == 0, str(result.stdout)

    shutil.copy(MOCK_PROJECT / "pytest.ini", pytester.path)
    result = pytester.runpytest_subprocess("-vs")
    assert result.ret == 0, str(result.stdout)
    result.stdout.fnmatch_lines([
        "*test_first*",
        "*test_second.py::TestSecondFoo*",
        "*test_second.py::test_foo*",
        "*test_third*",
        "*test_fourth*",
        "*test_fifth*",
    ])

    shutil.copy(MOCK_PROJECT / "degenerate-pytest.ini",
                pytester.path / "pytest.ini")
    result = pytester.runpytest_subprocess()
    assert result.ret != 0, str(result.stdout)
    result.stderr.re_match_lines([
        r".*files \['tests/test_fifth.py'\] do not .* the \"order\" section.*"
    ])
