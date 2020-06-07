import time as t

class Cumulator:

    def __init__(self):
        self.t0 = 0
        self.t1 = 0
        # times are in seconds
        self.time_list = []
        self.cumulated_time = 0
        # file sizes are in bytes
        self.file_size_list = []
        self.cumulated_data_traffic = 0

        # assumptions to approximate the carbon footprint
        # computation costs: consumption of a typical GPU in Watts converted to kWh/s
        self.hardware_load = joule_to_kwh(250)
        # communication costs: average energy impact of traffic in a typical data centers, kWh/byte
        self.one_byte_model = 6.894E-11
        # conversion to carbon footprint: average carbon intensity value in gCO2eq/kWh in the EU
        self.carbon_intensity = 447

    # starts accumulating time
    def on(self):
        self.t0 = t.time()

    # stops accumulating time and records the value
    def off(self):
        self.t1 = t.time()
        self.cumulated_time += self.t1 - self.t0
        self.time_list.append(self.t1 - self.t0)

    # records the amount of data transfered, file_size in bytes
    def data_transfered(self, file_size):
        self.file_size_list.append(file_size)
        self.cumulated_data_traffic += file_size

    # computes time based carbon footprint due to computations
    def computation_costs(self):
        return self.cumulated_time * self.hardware_load * self.carbon_intensity

    # computes the carbon footprint due to communication
    def communication_costs(self):
        return self.one_byte_model * self.cumulated_data_traffic

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

# energy conversion
def joule_to_kwh(value):
    return value / 3.6e6
