'''
This is the base class of cumulator.
'''

import json
import time as t
import geocoder
import random
import pandas as pd
from geopy.geocoders import Nominatim
import GPUtil
import cpuinfo
import os
import re
import numpy as np

from cumulator.prediction_feature.prediction_helper import get_predictions, compute_features
from cumulator.prediction_feature.visualization_helper import scatterplot

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

country_dataset_path = 'countries_data/country_dataset_adjusted.csv'
gpu_dataset_path = 'hardware_data/gpu.csv'
metrics_dataset_path = 'metrics_conversion_data/CO2_metrics.json'
cpu_dataset_path = 'hardware_data/cpu.csv'
regexp_cpu = '(Core|Ryzen).* (i\d-\d{3,5}.?|\d \d{3,5}.?)'


class Cumulator:
    def __init__(self, hardware="cpu"):
        # default value of TDP
        self.carbon_intensity = 334
        self.TDP = 250
        self.set_hardware(hardware)

        # define consumption on the current position, standard carbon footprint value: average carbon intensity value in gCO2eq/kWh in the EU in 2019
        self.position_carbon_intensity(default_Carbon_Intensity=334)
        self.t0 = 0
        self.t1 = 0
        # times are in seconds
        self.time_list = []
        self.cumulated_time = 0

        # file sizes are in bytes
        self.file_size_list = []
        self.cumulated_data_traffic = 0
        # number of GPU
        self.n_gpu = 1
        # assumptions to approximate the carbon footprint
        # computation costs: consumption of a typical GPU in Watts converted to kWh/s
        self.hardware_load = self.TDP / 3.6e6
        # communication costs: average energy impact of traffic in a typical data centers, kWh/kB
        self.one_byte_model = 7.20E-8

    # starts accumulating time
    def on(self):
        self.t0 = t.time()


    def estimate_gradients_size(self, model, num_parameters = 1, dtype = 'float32', compression_ratio = 1.0, epochs = 1):
        """
        Estimates the size of gradients in bytes based on the given variables.

        Parameters:
        - model : The model being studied (can be any model representation).
        - num_parameters (int): Number of parameters in the model. Defaults to 1 for the simplest model. 
          To be set to zero if an automatic detection is to be done
        - dtype (str, optional): Data type used for representing the gradients. Defaults to 'float32'.
        - compression_ratio (float, optional): Compression ratio applied to the gradients. Defaults to 1.0 (no compression).
        - epochs (int, optional): Number of training epochs. Defaults to 1.

        """
        # Find the number of parameters
        if num_parameters == 0:
            if hasattr(model, 'parameters'):
                # PyTorch framework
                num_parameters = sum(p.numel() for p in model.parameters()) * epochs
            elif hasattr(model, 'coef_') and hasattr(model, 'intercept_'):
                # Sklearn framework
                if model.intercept_.size > 1:
                    num_parameters = (sum([a.size for a in model.coef_]) +  sum([a.size for a in model.intercept_])) * epochs
                else:
                    num_parameters = (sum([a.size for a in model.coef_]) + model.intercept_.size) * epochs
            elif hasattr(model, 'coefs_') and hasattr(model, 'intercepts_'):
                # Sklearn framework
                num_parameters = (sum([a.size for a in model.coefs_]) +  sum([a.size for a in model.intercepts_])) * epochs
                epochs *= model.n_iter_
            elif hasattr(model, 'n_neighbors'):
                num_parameters = model.n_neighbors
            else:
                num_parameters = 1 * epochs

        # Determine the number of bytes per element based on the data type
        bytes_per_element = np.dtype(dtype).itemsize

        # Compute the uncompressed size of gradients in bytes
        uncompressed_size_bytes = num_parameters * bytes_per_element

        # Apply the compression ratio to estimate the final size of gradients
        self.cumulated_data_traffic += int(uncompressed_size_bytes * compression_ratio)


    def set_hardware(self, hardware):
        if hardware == "gpu":
            # search_gpu will try to detect the gpu on the device and set the corresponding TDP value as TDP value of Cumulator
            self.detect_gpu()
        elif hardware == "cpu":
            # search_cpu will try to detect the cpu on the device and set the corresponding TDP value as TDP value of Cumulator
            self.detect_cpu()
        # in case of wrong value of hardware_data let default TDP
        else:
            print(f'hardware_data expected to be "cpu" or "gpu". TDP set to default value {self.TDP}')
    
    
    # function for trying to detect gpu and set corresponding TDP value as TDP value of cumulator
    def detect_gpu(self):
        try:
            gpus = GPUtil.getGPUs()
            gpu_name = gpus[0].name

            dirname = os.path.dirname(__file__)
            relative_gpu_dataset_path = os.path.join(dirname, gpu_dataset_path)
            df = pd.read_csv(relative_gpu_dataset_path)
            # it uses contains for more flexibility
            row = df[df['name'].str.contains(gpu_name)]
            if row.empty:
                # if gpu not found then leave standard TDP value
                print(f'GPU not found. Standard TDP={self.TDP} assigned.')
            else:
                # otherwise assign gpu's TDP
                self.TDP = row.TDP.values[0]
        # ValueError arise when GPUtil can't communicate with the GPU driver
        except (ValueError, IndexError):
            # in case no GPU can be found
            print(f'GPU not found. Standard TDP={self.TDP} assigned.')

    def detect_cpu(self):
        try:
            cpu_name = cpuinfo.get_cpu_info()['brand_raw']
            result = re.search(regexp_cpu, cpu_name)
            if result is not None:
                cpu_name = result.group(1) + ' ' + result.group(2)
            dirname = os.path.dirname(__file__)
            relative_cpu_dataset_path = os.path.join(dirname, cpu_dataset_path)
            df = pd.read_csv(relative_cpu_dataset_path)
            # it uses contains for more flexibility
            row = df[df['name'].str.contains(cpu_name)]
            if row.empty:
                # if gpu not found then leave standard TDP value
                print(f'CPU not found. Standard TDP={self.TDP} assigned.')
            else:
                # otherwise, assign CPU's TDP
                self.TDP = row.TDP.values[0]
                print(f'CPU recognized: TDP set to {row.TDP.values[0]}')

        except:
            # in case no CPU can be found
            print(f'[except] CPU not found. Standard TDP={self.TDP} assigned.')

    # stops accumulating time and records the value
    def off(self):
        self.t1 = t.time()
        self.cumulated_time += self.t1 - self.t0
        self.time_list.append(self.t1 - self.t0)

    def run(self, function, *args, **kwargs):
        """
        Measure the carbon footprint of `function`.

        Example
        --------
        >>> # imports
        >>> from sklearn.linear_model import LinearRegression
        >>> from sklearn import datasets
        >>> # initialization
        >>> cumulator = Cumulator()
        >>> model = LinearRegression()
        >>> diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True)
        >>> # without output and with keywords arguments
        >>> cumulator.run(model.fit, X=diabetes_X, y=diabetes_y)
        >>> # with output and without keywords arguments
        >>> y = cumulator.run(model.predict, diabetes_X)
        >>> # show results
        >>> cumulator.display_carbon_footprint()


        :param function: function to measure.
        :param args: positional arguments of `function`.
        :param kwargs: keywords arguments of `function`.
        :return: output of `function`.
        """
        self.on()
        output = function(*args, **kwargs)
        self.off()
        return output

    def position_carbon_intensity(self, default_Carbon_Intensity = 334):

        try:
            dirname = os.path.dirname(__file__)
            relative_country_dataset_path = os.path.join(dirname, country_dataset_path)

            geolocator = Nominatim(user_agent="cumulator")
            g = geocoder.ip('me')
            df_data = pd.read_csv(relative_country_dataset_path)

            location = geolocator.reverse(g.latlng)
            address = location.raw['address']
            code = address.get('country_code').upper()
            df_row = df_data[df_data['country'] == code]
            self.carbon_intensity = float(
                df_row['co2_per_unit_energy'] if not df_row.empty else None)
            if self.carbon_intensity is None:
                raise AttributeError
        except (AttributeError, FileNotFoundError):
            print(f'Current position not found. Standard Carbon Intensity={default_Carbon_Intensity} assigned.')
            self.carbon_intensity = default_Carbon_Intensity

    # records the amount of data transferred, file_size in kilo bytes
    
    def data_transferred(self, file_size):
        self.file_size_list.append(file_size)
        self.cumulated_data_traffic += file_size

    # computes time based carbon footprint due to computations
    def computation_costs(self):
        return self.cumulated_time * self.n_gpu * self.hardware_load * self.carbon_intensity

    # computes the carbon footprint due to communication
    def communication_costs(self):
        return self.one_byte_model * self.cumulated_data_traffic * self.carbon_intensity

    # computes the total carbon footprint
    def total_carbon_footprint(self):
        return self.computation_costs() + self.communication_costs()

    # prints the carbon footprint in the terminal
    def display_carbon_footprint(self):
        print('########\nOverall carbon footprint: %s gCO2eq\n########' %
              "{:.2e}".format(self.total_carbon_footprint()))
        print('Carbon footprint due to computations: %s gCO2eq' %
              "{:.2e}".format(self.computation_costs()))
        print('Carbon footprint due to communications: %s gCO2eq' %
              "{:.2e}".format(self.communication_costs()))
        # loading metrics_conversion_data dataset
        dirname = os.path.dirname(__file__)
        relative_metric_dataset_path = os.path.join(dirname, metrics_dataset_path)

        with open(relative_metric_dataset_path) as file:
            metrics = json.load(file)
            # computing equivalent of gCO2eq
            for metric in metrics:
                metric['equivalent'] = float(metric['eq_factor']) * (self.total_carbon_footprint())
            # select random equivalent metrics_conversion_data and print
            metric = metrics[random.randint(0, len(metrics) - 1)]
            print('This carbon footprint is equivalent to {:0.2e} {}.'.format(metric['equivalent'],
                                                                              metric['measure'].lower()))

    def return_total_carbon_footprint(self):
        return self.total_carbon_footprint()

    def predict_consumptions_f1(self, dataset, target):
        """
        Predict the consumption and f1 scores of classification task on a given dataset with 4 different models: Linear model, Decision tree, Random forest, Neural network
        Parameters
        ----------
        dataset dataset as a Pandas dataframe

        Returns
        -------

        """
        # Get x vector from dataset
        x = compute_features(dataset, target)

        # Predict times and consumptions, and put them in lists in the following order: Linear - Decision tree -
        # Random forest - Neural network
        consumption_costs, scores, consumption_costs_rmse, scores_rmse = get_predictions(x)

        # Show results
        scatterplot(consumption_costs, scores)
