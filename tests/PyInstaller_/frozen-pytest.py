# -*- coding: utf-8 -*-
"""
Freeze pytest.main() with pytest_ordered included.
"""
import sys
import pytest_ordered

import pytest

sys.exit(pytest.main(sys.argv[1:] + ["--no-cov", "--tb=native"]))
