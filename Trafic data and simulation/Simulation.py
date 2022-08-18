"""
this class represents a Simulation
"""
class Simulation:
    def __init__(self, simulation_number, seed_number):
        # this is a property
        self.simulation_number = simulation_number

        self.__seed_seed_number = seed_number

        # {string: []}  --> {name of collection point: [], ...}
        self.__all_data_collection_points_and_values_of_each_interval = {}
        self.__all_data_collection_points_and_sum_of_values_of_intervals = {}

    @property
    def simulation_number(self):
        return self.__simulation_number
    @simulation_number.setter
    def simulation_number(self,value):
        if value < 0:
            raise ValueError("simulation number should be positive")
        self.__simulation_number = value

    @property
    def data_collection_points(self):
        """

        :return: a dictionary of  {name of collection point: value of collection point , ...}
        """
        return self.__all_data_collection_points_and_values_of_each_interval

    def add_data_collection_point_value(self, name, value):
        """
        :param name: name of the collection point (string)
        :param value: value of the collection point in each time interval (array)
        :return: void
        """
        self.__all_data_collection_points_and_values_of_each_interval[name] = value

    def get_the_sum_of_all_interval_values(self):
        f"""
        
        :return: a dictionary of {"data_collection_point_name": value of data collection point}
        """
        for sensor_name, array_of_values in self.__all_data_collection_points_and_values_of_each_interval:
            self.__all_data_collection_points_and_sum_of_values_of_intervals[sensor_name] = sum(array_of_values)
        return self.__all_data_collection_points_and_sum_of_values_of_intervals

