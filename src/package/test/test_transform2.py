import os
import sys

root_path = os.path.abspath(
    os.path.join(os.path.split(__file__)[0], os.pardir, os.pardir)
)  # code folder of the project
sys.path.insert(0, root_path)

import pytest
import numpy as np
import package.transform as tf


@pytest.mark.circles
@pytest.mark.skip(reason="Trying out the skip feature")
def test_area_circ():
    """Test the area values against a reference for r >= 0."""
    assert tf.area_circ(1) == np.pi, "should return pi"
    assert tf.area_circ(0) == 0
    assert tf.area_circ(2.1) == np.pi * 2.1**2


@pytest.mark.circles
def test_values():
    """Make sure value errors are recognized for area_circ."""
    with pytest.raises(ValueError):
        tf.area_circ(-5)
