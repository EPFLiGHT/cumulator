=========
CUMULATOR
=========

A tool to quantify and report the carbon footprint of machine learning computations and communication in academia and healthcare

Aim
___
Raise awareness about the carbon footprint of machine learning methods and to encourage further optimization and the rationale use of AI-powered tools.
This work advocates for sustainable AI and the rational use of IT systems.

Key Carbon Indicators
_____________________
* **One hour of GPU load is equivalent to 112 gCO2eq**
* **1 GB of data traffic through a data center is equivalent to 31 gCO2eq**

Install and use
_______________

Free software: MIT license

``pip install cumulator`` <- installs CUMULATOR

``from cumulator import base`` <- imports the script

``cumulator = base.Cumulator()`` <- creates an Cumulator instance 

**Measure cost of computations.** Activate or deactivate chronometer by using ``cumulator.on()``, ``cumulator.off()`` whenever you perform ML computations (typically within each interation). It will automatically record each time duration in ``cumulator.time_list`` and sum it in ``cumulator.cumulated_time()``. Then return carbon footprint due to all computations using ``cumulator.computation_costs()``.

**Measure cost of communications.** Each time your models sends a data file to another node of the network, record the size of the file which is communicated (in kilo bytes) using ``cumulator.data_transferred(file_size)``. The amount of data transferred is automatically recorded in ``cumulator.file_size_list`` and accumulated in ``cumulator.cumulated_data_traffic``. Then return carbon footprint due to all communications using ``cumulator.communication_costs()``.

Return the total carbon footprint using ``cumulator.total_carbon_footprint()``. You can also display the carbon footprint in terminal using ``display_carbon_footprint()``

**Default assumptions (can be manually modified for better estimation):**

``self.hardware_load = 250 / 3.6e6`` <- computation costs: power consumption of a typical GPU in Watts converted to kWh/s

``self.one_byte_model = 6.894E-8`` <- communication costs: average energy impact of traffic in a typical data centers, kWh/kB

``self.carbon_intensity = 447`` <- conversion to carbon footprint: average carbon intensity value in gCO2eq/kWh in the EU in 2014

``self.n_gpu = 1`` <- number of GPU used in parallel

    
Project Structure
_________________

:: 

    src/
    ├── cumulator  
        ├── base.py           <- implementation of the Cumulator class
        └── bonus.py          <- Impact Statement Protocol

ChangeLog
_________
* 18.06.2020: 0.0.6 update README.rst
* 11.06.2020: 0.0.5 add number of processors (0.0.4 failed)
* 08.06.2020: 0.0.3 added bonus.py carbon impact statement
* 07.06.2020: 0.0.2 added communication costs and cleaned src/
* 21.05.2020: 0.0.1 deployment on PypI and integration with Alg-E

Links
_____
* Material: https://drive.google.com/drive/u/1/folders/1Cm7XmSjXo9cdexejbLpbV0TxJkthlAGR
* GitHub: https://github.com/epfl-iglobalhealth/cumulator
* PyPI: https://pypi.org/project/cumulator/
