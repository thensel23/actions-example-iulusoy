import os
import sys

from package.analysis import *
from package.transform import area_circ

root_path = os.path.abspath(
    os.path.join(os.path.split(__file__)[0], os.pardir)
)  # code folder of the project
sys.path.insert(0, root_path)

if __name__ == "__main__":

    freq_list = [1, 2, 3]
    file_name = "data.csv"
    file_path = root_path + "/output/" + file_name

    create_data(freq_list, file_path)

    frequencies, amplitudes, phases = analyze_data(file_path)

    visualize_data(file_path, frequencies, amplitudes, phases)

    area_circ(2.3)
