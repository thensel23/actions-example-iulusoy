import os
import sys

root_path = os.path.abspath(
    os.path.join(os.path.split(__file__)[0], os.pardir, os.pardir)
)  # code folder of the project
sys.path.insert(0, root_path)

import numpy as np
import pandas as pd
import pytest
import shutil

from package.analysis import create_data


@pytest.mark.data
def test_create_data():
    # create a dataset with a single frequency and check if it exists
    freq_list = [1]
    file_name = "data.csv"
    file_path = root_path + "/output/" + file_name
    dir, f = os.path.split(file_path)
    os.makedirs(dir, exist_ok=True)
    # file_path = './test_dataset_1.csv'
    create_data(freq_list, file_path)
    assert os.path.isfile(file_path)

    # create a dataset with multiple frequencies and check if it exists
    freq_list = [1, 3, 5]
    file_name = "data.csv"
    file_path = root_path + "/output/" + file_name
    create_data(freq_list, file_path)
    assert os.path.isfile(file_path)

    # check if the generated file contains two columns
    data = pd.read_csv(file_path)
    assert len(data.columns) == 2

    # check if the generated file contains expected data type
    assert isinstance(data["X"][0], np.float64)
    assert isinstance(data["Y"][0], np.float64)

    # remove the test files after testing
    shutil.rmtree(dir)
