import os
import sys

root_path = os.path.abspath(
    os.path.join(os.path.split(__file__)[0], os.pardir, os.pardir)
)  # code folder of the project
sys.path.insert(0, root_path)

import pytest
from package.transform import area_circ


def test_area_circ():
    # Test with a positive radius
    assert area_circ(2) == 12.566370614359172
    # Test with zero radius
    assert area_circ(0) == 0
    # Test with a negative radius
    with pytest.raises(ValueError):
        area_circ(-1)
