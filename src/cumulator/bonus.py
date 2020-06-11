'''
This script empowers the protocol to quantify the carbon footprint in research projects

Assumptions (can be modified as function argument):
- Project duration: 14 weeks
- Duration of a virtual meeting: 45 min
- Power consumption of the main device used during the research
(screening time, video-conferencing): 40 W

User-provided information (as function argument):
- Weekly screening time in s (influences carbon footprint of screening time and meetings)
- Carbon footprint of due to data traffic through your Internet browser (from Carbonalyser) in gCO2
- Carbon cost of ML simulations (using CUMULATOR base tool) in gCO2

Source: project report of Tristan Trébaol made in Spring 2020.
'''

# Heuristics

# total energy consumption during virtual meeting
virtual_meeting_consumption = 187.6  # in W
# carbon intensity (avg in EU in 2014)
carbon_intensity = 447  # in gCO2eq/kWh
# 1byte model in Wh/byte
one_byte_model = 6.894E-11
# Average WLTP emissions in (km/gCO2)
car = 1/148.1

# Method

# prints and returns the total carbon footprint
def project_carbon_footprint(carbonalyser, ml_simulations, screening_time,
                             n_weeks=14, meeting_duration=45, hardware_consumption=40):
    meetups = joule_to_kwh(virtual_meeting_consumption * \
                           meeting_duration * 60 * \
                           n_weeks) * carbon_intensity
    screening = joule_to_kwh(n_weeks * screening_time * hardware_consumption) * carbon_intensity
    # total carbon footprint in gC02eq
    carbon_emissions = meetups + screening + carbonalyser + ml_simulations
    car_distance = car * carbon_emissions

    print('##############################################################'
          '\nTotal carbon emissions for this project: %s gCO2eq'
          '\nYou could have powered the average passenger car for %i km'
          '\nwith all that compute effort.'
          '\n--------------------------------------------------------------' % ("{:.2e}".format(carbon_emissions),
                                                                                car_distance))
    print('ML models: %s gCO2eq' % "{:.2e}".format(ml_simulations))
    print('Internet data traffic: %s gCO2eq' % "{:.2e}".format(carbonalyser))
    print('Meetings: %s gCO2eq' % "{:.2e}".format(meetups))
    print('Screening: %s gCO2eq' % "{:.2e}".format(screening))
    print('--------------------------------------------------------------'
          '\n##############################################################')
    return carbon_emissions


# energy conversion
def joule_to_kwh(value):
    return value / 3.6e6
