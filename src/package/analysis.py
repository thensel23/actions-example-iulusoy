"""
Analysis module.

Contains functionality to create, analyze and plot data.

@Thomas Arne Hensel, 04/2023
"""
import os, sys
root_path = os.path.abspath(os.path.join(os.path.split(__file__)[0], os.pardir)) # code folder of the project
sys.path.insert(0, root_path)

import pandas as pd
import numpy as np
from scipy.stats import poisson
from scipy.fft import fft
import matplotlib.pyplot as plt

def create_data(freq_list, file_path):
    """
    Generate a dataset with sinusoidal functions, Poissonian noise and save as csv file.

    :param list(freq_list): A list of frequencies for sinusoidal functions.
    :param str(file_path): A string with file path to save dataset as csv file.

    :return: None

    The function generates a dataset with sinusoidal functions, Poissonian noise and saves the 
    dataset as a comma-separated (.csv) file at the specified file path. The function takes two 
    arguments, freq_list and file_path. freq_list is a list of frequencies for sinusoidal functions 
    and file_path is a string with file path to save dataset as csv file.

    Example:
        create_data(freq_list=[1, 3, 5], file_path='./dataset.csv')
    """
    min_freq = min(freq_list)
    x = np.linspace(0, 2*np.pi/(min_freq), 1000)
    y = len(freq_list)+np.sum([np.sin(f*x) for f in freq_list], axis=0) # sum of different harmonic functions
    noise = np.random.default_rng().poisson(y) # generate poissonian noise
    y += noise # add noise to the data
    data = pd.DataFrame({'X': x, 'Y': y})
    data.to_csv(file_path, index=False)
    pass

def analyze_data(file_path):
    """
    Analyzes the data from the file located at file_path using Fourier Transform.

    :param file_path: A string, the file path to the csv file containing the data.
    :return: A tuple of three 1D numpy arrays - frequencies, amplitudes, and phases. Each array contains the values
             for the top 5 frequencies in the data.
    :raises: FileNotFoundError : If the file at the given path does not exist.
             pandas.errors.EmptyDataError : If no data is found in the csv file.
             ValueError : If the data in the csv file is not in the expected format.

    This function uses the Fourier Transform to analyze the data from the csv file at file_path. It first reads the
    data from the csv file using pandas.read_csv() and extracts the data columns X and Y. It then calculates the
    number of data points N, the time step dt, and the frequency values for the Fast Fourier Transform.

    The function then applies the Fast Fourier Transform on the data to obtain the complex frequency domain data.
    The absolute values of the complex data is computed to obtain the amplitude, and the angle of the complex data is
    computed to obtain the phase.

    The top 5 frequencies in the data are determined by finding the indices with the highest amplitudes and returning
    the corresponding frequencies, amplitudes, and phases.\n    """
    data = pd.read_csv(file_path)
    x = data['X']
    y = data['Y']
    N = len(x)
    dt = x[1] - x[0]
    frequencies = np.linspace(0.0, 0.5/dt, N//2)

    Y = np.abs(fft(y.values))
    amplitudes = 2.0/N * np.abs(Y[:N//2])
    phases = np.angle(Y[:N//2])

    idx = np.argsort(amplitudes)[::-1][:5]
    frequencies = frequencies[idx]
    amplitudes = amplitudes[idx]
    phases = phases[idx]

    return frequencies, amplitudes, phases

def visualize_data(file_path: str, frequencies: list[float], amplitudes: list[float], phases: list[float]) -> None:
    """
    Visualize a set of harmonic signals corresponding to specified frequencies, amplitudes, and phases.

    :param file_path: A string representing the file path to the CSV file containing x and y data.
    :type file_path: str
    :param frequencies: A list of frequencies for the harmonic signals.
    :type frequencies: List[float]
    :param amplitudes: A list of amplitudes for the harmonic signals.
    :type amplitudes: List[float]
    :param phases: A list of phases for the harmonic signals.\n    :type phases: List[float]
    :return: None
    :rtype: None

    Reads in a CSV file containing x and y data, and generates a plot of the original data overlaid with the
    harmonic signals. The harmonic signal has the form y(t) = A * sin(2*pi*f*t + phi), where A is the amplitude,\n    f is the frequency, and phi is the phase shift.

    The function saves the plot as a PDF in the same directory as the input file with a name of the form
    \"<filename>_harmonic.pdf".

    Usage:

        >>> visualize_data('/path/to/data.csv', [1, 2, 3], [1, 0.5, 0.25], [0, 0, 0])

    This will generate a plot of the original data overlaid with the harmonic signals with frequencies of 1, 2,\n    and 3 Hz, amplitudes of 1, 0.5, and 0.25, and no phase shifts.
    """
    data = pd.read_csv(file_path)
    x = data['X']
    y = data['Y']
    N = len(x)
    dt = x[1] - x[0]
    t = np.linspace(0, N*dt, N)

    y_combined = np.zeros_like(y)
    for i in range(len(frequencies)):
        y_combined += amplitudes[i] * np.sin(2*np.pi*frequencies[i]*t + phases[i])
    y_combined += np.mean(y)

    plt.plot(x, y, label='Original data')
    plt.plot(x, y_combined, label='Harmonic signals')
    plt.legend()
    # Save plot as a PDF
    file_dir = os.path.dirname(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    plot_path = os.path.join(file_dir, f"{file_name}_harmonic.pdf")
    plt.savefig(plot_path)
    pass


