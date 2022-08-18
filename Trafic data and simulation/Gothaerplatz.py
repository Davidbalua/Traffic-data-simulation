import win32com.client as com
from SimulationRuns import SimulationRuns
"""
this class connects this program to Vissim

"""


class Vissim:

    def __init__(self, vissim_path):
        self.__path = vissim_path
        # self.__vissim = com.gencache.EnsureDispatch("Vissim.Vissim.22")
        self.__vissim = com.Dispatch("Vissim.Vissim")
        "set the path of the file"
        self.__vissim.LoadNet(self.__path)
        # the name of links and their key numbers, on which vehicle inputs have been located
        #{key: name of the link}
        self.__key_of_street_and_name_of_street = {}
        self.__key_of_vehinput_and_key_of_street = {}

        #load the vehicle inputs
        self.__get_all_vehicle_inputs()

        self.__SimulationRuns = SimulationRuns(self.vissim)
        # self.vissim.SaveNetAs(self.__path)

    @property
    def vissim(self):
        return self.__vissim

    @property
    def simulation_runs(self):
        return self.__SimulationRuns

    def run_simulations(self,number):
        self.simulation_runs.run_the_simulations(number)


    def __get_all_vehicle_inputs(self) -> "void":
        """
        this method counts the number of vehicle inputs and extract the name of the links,
        on which vehicle inputs are located
        :return: void
        """
        # the number of vehicle inputs
        number_of_veh_inputs = self.vissim.Net.VehicleInputs.Count
        for key_of_vehinput in range(1, number_of_veh_inputs + 1):
            key_of_street = self.vissim.Net.VehicleInputs.ItemByKey(key_of_vehinput).AttValue("Link")
            name_of_street = self.vissim.Net.Links.ItemByKey(int(key_of_street)).AttValue("Name")
            self.__key_of_street_and_name_of_street[key_of_street] = name_of_street
            self.__key_of_vehinput_and_key_of_street[key_of_vehinput] = key_of_street


    def get_vehicleinput(self):
        """
        must be completed
        :return:
        """
        # self.__key_of_vehinput_and_key_of_street.items() returns key and values as a tuple
        for key_of_vehinput,key_of_street in self.__key_of_vehinput_and_key_of_street.items():
            for time_interval in range (1,25):
                volume_in_specific_time_interval = self.vissim.Net.VehicleInputs.ItemByKey(key_of_vehinput).AttValue(f"Volume({time_interval})")
                print(f"street: {self.__key_of_street_and_name_of_street[key_of_street]}, the value of {time_interval} = {volume_in_specific_time_interval}")






