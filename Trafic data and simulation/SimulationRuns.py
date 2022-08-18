import math
import random
from Simulation import Simulation
import pandas as pd

"""
The necessary number of simulation runs with different random seed numbers is unknown and 
Has to be guessed
1.	Choose a validation parameter:                              Vehicle Volume (Veh/hr)
2.	Simulate a few runs (10 simulations):                       10 runs
3.	Estimate standard deviation from these runs:                for each induction loop in Vissim, calculate the standard deviation. 
4.	Calculate the number of runs with the chosen accuracy:      0.975
5.	Repeat calculation of number of runs till number is large enough
"""


class SimulationRuns:

    def __init__(self, vissim):
        self.__vissim = vissim
        self.__random_seed_numbers = []
        # array of simulations. each object will be of the type Simulation
        self.__simulations = []
        #{name of collection point(string): standard deviation(double)}
        self.__standard_deviation_of_each_data_collection_point = {}

        # self.run_the_simulations(10)


    @property
    def vissim(self):
        return self.__vissim

    @property
    def get_random_seed_numbers(self):
        return self.__random_seed_numbers

    # array of simulations
    @property
    def simulations(self):
        return self.__simulations

    def run_the_simulations(self, number_of_simulation_runs=2):
        """
        specify the seed numbers, run the simulations, specify the total number of runs to reach a certain accuracy
        :param number_of_simulation_runs:
        :return:
        """

        # Delete all previous simulation runs first:
        for simRun in self.__vissim.Net.SimulationRuns:
            self.__vissim.Net.SimulationRuns.RemoveSimulationRun(simRun)

        if number_of_simulation_runs < 0:
            raise ValueError("the number of simulation runs must be a positive number")
        # first calculate randomly the random seed number values for each simulation. the number of seeds equal the number of simulation runs
        self.__random_seed_numbers = [random.randint(10, 10000) for i in range(1, number_of_simulation_runs + 1)]

        # Activate QuickMode:
        self.__vissim.Graphics.CurrentNetworkWindow.SetAttValue("QuickMode", 1)
        # stop updating of the complete Vissim workspace (network editor, list, chart and signal time table windows)
        self.__vissim.SuspendUpdateGUI()
        # set the the maximum speed
        self.vissim.Simulation.SetAttValue('UseMaxSimSpeed', True)

        # run the simulations one by one
        for simulation_run in range(1, number_of_simulation_runs + 1):
            # set the seed number for each simulation run
            self.vissim.Simulation.SetAttValue('RandSeed', self.__random_seed_numbers[simulation_run - 1])
            # run the simulation
            self.vissim.Simulation.RunContinuous()
            # add this simulation to the array of simulations
            self.simulations.append(Simulation(simulation_run, self.__random_seed_numbers[simulation_run - 1]))

        # allow updating of the complete Vissim workspace (network editor, list, chart and signal time table windows)
        self.__vissim.ResumeUpdateGUI(True)
        self.__vissim.Graphics.CurrentNetworkWindow.SetAttValue("QuickMode", 0)  # deactivate QuickMode
        # Access the values of the induction loops
        self.access_data_collection_points(number_of_simulation_runs, 24)

    def access_data_collection_points(self, number_of_simulation_runs, number_of_intervals=24):
        # 33
        the_number_of_collection_points = self.__vissim.Net.DataCollectionPoints.Count
        # Data Collection
        # for each simulation run
        # time complexity is n3
        for simulation in self.simulations:
            # for each data collection point
            for key_of_collection_point in range(1, the_number_of_collection_points + 1):
                values_in_intervals = []
                DC_measurement = self.__vissim.Net.DataCollectionMeasurements.ItemByKey(key_of_collection_point)
                # record the name of data collection
                name_of_collection_point = DC_measurement.AttValue("Name")

                for interval in range(1, number_of_intervals + 1):
                    # if it's the last simulation
                    if simulation.simulation_number == len(self.simulations):
                        value_of_interval = DC_measurement.AttValue(f'Vehs(Current,{interval},All)')
                        values_in_intervals.append(value_of_interval)
                    else:
                        value_of_interval = DC_measurement.AttValue(
                            f'Vehs({simulation.simulation_number},{interval},All)')
                        values_in_intervals.append(value_of_interval)

                simulation.add_data_collection_point_value(name_of_collection_point, values_in_intervals)
        self.get_SD_and_AV_of_each_datacollectionpoint()

    def get_SD_and_AV_of_each_datacollectionpoint(self):
        """
        this method gets the standard deviation of each data collection point for the complete simulation run from Vissim
        :return: void
        """

        if len(self.simulations) == 1:
            raise Exception("The number of simulations must be more than one")
        else:
            # derive the number of data collection points, in this case: 33
            the_number_of_collection_points = self.__vissim.Net.DataCollectionPoints.Count

            # for each data collection point
            for key_of_collection_point in range(1, the_number_of_collection_points + 1):
                DC_measurement = self.__vissim.Net.DataCollectionMeasurements.ItemByKey(key_of_collection_point)
                # record the name of data collection
                name_of_collection_point = DC_measurement.AttValue("Name")
                # derive standard deviation for this data collection point
                standard_deviation_of_collection_point = DC_measurement.AttValue(f'Vehs(StdDev,Total,All)')
                # store the result in a dictionary of {sensor_name(string):standard deviation (double)}
                self.__standard_deviation_of_each_data_collection_point[
                    name_of_collection_point] = standard_deviation_of_collection_point
                # troubleshooting
        # for sensor_name,sd in self.__standard_deviation_of_each_data_collection_point.items():
        #     print(f'Name: {sensor_name},sd: {sd}')
        self.determine_number_of_simulation_runs(15)


    def determine_number_of_simulation_runs(self, n):
        """
        for each induction loop, there is only one standard deviation.
        this method finds the median standard deviation from all sensors.
        it calculates the number of simulation runs according to this standard deviation, which is a median value.
        :return: void
        """
        # from self.__standard_deviation_of_each_data_collection_point, find the Median of standard deviations with pandas.
        name_sd = [(sensor_name, sd) for sensor_name, sd in self.__standard_deviation_of_each_data_collection_point.items()]
        data_frame_of_sensorname_sd = pd.DataFrame(name_sd, columns=["sensor_name", "sd"])

        # find the median
        median = data_frame_of_sensorname_sd["sd"].median()

        # extract the name of the sensor, which has standard deviation, which is a median value among other sensors
        chosen_sensor = data_frame_of_sensorname_sd[data_frame_of_sensorname_sd["sd"] == median]
        # median_sensor is Tuple (sensor_name, sd). the sensor has the median standard deviation among other other sensors
        median_sensor = (chosen_sensor.iloc[0]['sensor_name'], chosen_sensor.iloc[0]['sd'])
        #print(median_sensor)

        # Error smaller than ten cars, confidence level of 95
        # How many simulation runs are required to give the value of the induction loop with an error smaller than ten cars at a confidence level of 95?
        # 0.95 is confidence level
        # n = 15 = number, which is used to derive a number from student table
        # t(0.95,15-1) = 1.75
        # sd = standard deviation
        # n_necessary = ((t^2 * sd^2)) / 10 ^ 2
        #TODO: create student's t table in a new class
        median_sd = median_sensor[1]
        n_necessary = ((math.pow(1.75, 2) * math.pow(median_sd, 2)) / 100)

        print(f"confidence level of 95:the value of n_necessary is {n_necessary}, and the value is {15}")
        if n_necessary > n:
            print("n_necessary > n , try again")
        else:
            print(f"the number of simulation runs is {n}")

            # Error smaller than ten cars, confidence level of 97.5
            # How many simulation runs are required to give the value of the induction loop with an error smaller than ten cars at a confidence level of 95?
            # 0.975 is confidence level
            # n = 15 = number, which is used to derive a number from student table
            # t(0.975,15-1) = 2.13
            # sd = standard deviation
            # n_necessary = ((t^2 * sd^2)) / 10 ^ 2
            # TODO: create student's t table in a new class
            n_necessary = ((math.pow(2.13, 2) * math.pow(median_sd, 2)) / 100)

            print(f"confidence level of 97.5: the value of n_necessary is {n_necessary}, and the value is {15}")
            if n_necessary > n:
                print("n_necessary > n , try again")
            else:
                print(f"the number of simulation runs is {n}")

















