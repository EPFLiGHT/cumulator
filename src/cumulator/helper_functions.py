import time as t


class Cumulator:

    def __init__(self):
        self.t0 = 0
        self.t1 = 0
        self.time_list = []
        self.total_time = 0
        # consumption of a typical GPU in Watts converted to kWh/s
        self.hardware_load = Joule2kWh(254)
        # average value of gCO2/kWh equivalent in the EU
        self.carbon_impact = 105
        #  avg energy impact of traffic in a typical data centers, kWh/byte converted to kWh/bit
        self.data_center_footprint = 7.2E-11 / 8

    def on(self):
        self.t0 = t.time()

    def off(self):
        self.t1 = t.time()
        self.total_time += self.t1 - self.t0
        self.time_list.append(self.t1 - self.t0)

    # time based carbon emission computation
    def carbon_footprint(self):
        return self.total_time * self.hardware_load * self.carbon_impact

    # TODO: add option to specify what is the current action to link individual
    # footprints with actions

    # sized base carbon emission
    # computes the gram CO2 equivalent based on size of the package and energy per bit consumption
    # def carbon_emission_size(self, size):
    #    return size * energyImpact * self.carbon_impact


# converts kWh in joules
def Joule2kWh(value):
    return value / 3.6e6


# converts bytes to bits
def bytes2bits(value):
    return value * 8

# computes the energy consumption per bit in kWh/bit
# def EnergyImpact(bandwidth):
#    return HardwareLoad() / bandwidth
