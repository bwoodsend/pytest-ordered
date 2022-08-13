import re
import os

import pytest


def pytest_addoption(parser):
    parser.addini("order", "The order in which to run tests.", type="linelist")


def pytest_collection_modifyitems(session, config, items):
    if not config.getini("order"):
        return
    order = expand_test_order(config.inicfg["order"])
    ranks = []
    for test in items:
        location = test.location[0].replace(os.path.sep, "/")
        key = lambda item: location == item[1]
        best_match = max(enumerate(order), key=key)
        if not key(best_match):
            raise pytest.UsageError(
                f'Test file "{test.location[0]}" does not match any of the '
                f'test file names listed in the "order" section of the '
                f'pytest.ini/setup.cfg file.'
            )
        ranks.append(best_match[0])
    args = sorted(range(len(items)), key=ranks.__getitem__)
    items[:] = [items[i] for i in args]


def expand_test_order(x):
    lines = re.findall("-( *)(.+)", x)
    out = []
    levels = {}
    for _prefix, _name in lines:
        levels[len(_prefix)] = _name
        out.append("".join(j for (i, j) in levels.items() if i <= len(_prefix)))
    return out
