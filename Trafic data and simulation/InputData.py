import pandas as pd

"""
create a new object of this class
call load_data() method to load the first source of data into the program
call filter_data(fromTime,toTime) to filter all data according to the time
call store_all_data()
 
"""

class InputData:

    def __init__(self):
        # {"name of induction loop":[value1, value2, ...]}
        self.__induction_loops = {}
        self.__files = []

    @property
    def induction_loops(self):
        return self.__induction_loops

    def load_data(self):
        """
        it loads all csv files
        :return:
        """
        # the following could be also automated
        self.first_file = pd.read_csv(
            "data/induction loops data/1_EF_LSA_K251_q/pwpTMP_2021-11-19_14 31 10_Diagramm1.csv", sep="\t",
            encoding='latin-1')
        self.second_file = pd.read_csv(
            "data/induction loops data/2_EF_LSA_K252_q/pwpTMP_2021-11-19_14 36 36_Diagramm2.csv", sep=";")
        self.third_file = pd.read_csv(
            "data/induction loops data/2_EF_LSA_K252_q/pwpTMP_2021-11-19_14 45 37_Diagramm3.csv", sep=";")
        self.fourth_file = pd.read_csv(
            "data/induction loops data/3_EF_LSA_K283_q/pwpTMP_2021-11-19_14 46 59_Diagramm4.csv", sep=";")
        self.fifth_file = pd.read_csv(
            "data/induction loops data/4_EF_MQS_TEU133&134_q_v/pwpTMP_2021-11-19_14 46 59_Diagramm5 (TEU, q).csv",
            sep=";")
        self.sixth_file = pd.read_csv(
            "data/induction loops data/4_EF_MQS_TEU133&134_q_v/pwpTMP_2021-11-19_14 46 59_Diagramm6 (TEU, v).csv",
            sep=";")

        # change the format of time
        self.first_file['Zeit'] = pd.to_datetime(self.first_file['Zeit'],
                                                 format="%a %b %d %Y %H:%M:%S GMT+0100 (Mitteleuropäische Normalzeit)")
        self.second_file['Zeit'] = pd.to_datetime(self.second_file['Zeit'],
                                                  format="%a %b %d %Y %H:%M:%S GMT+0100 (Mitteleuropäische Normalzeit)")
        self.third_file['Zeit'] = pd.to_datetime(self.third_file['Zeit'],
                                                 format="%a %b %d %Y %H:%M:%S GMT+0100 (Mitteleuropäische Normalzeit)")
        self.fourth_file['Zeit'] = pd.to_datetime(self.fourth_file['Zeit'],
                                                  format="%a %b %d %Y %H:%M:%S GMT+0100 (Mitteleuropäische Normalzeit)")
        self.fifth_file['Zeit'] = pd.to_datetime(self.fifth_file['Zeit'],
                                                 format="%a %b %d %Y %H:%M:%S GMT+0100 (Mitteleuropäische Normalzeit)")
        self.sixth_file['Zeit'] = pd.to_datetime(self.sixth_file['Zeit'],
                                                 format="%a %b %d %Y %H:%M:%S GMT+0100 (Mitteleuropäische Normalzeit)")

    def filter_data(self, from_time=16, to_time=18):
        """
        this method will filter the data according to the time
        :param from_time: integer
        :param to_time:   integer
        :return: void
        """

        self.first_file = self.first_file.loc[
            (self.first_file['Zeit'] > f'Tue Nov 10 2021 {from_time}:00:00')
            & (self.first_file['Zeit'] <= f'Tue Nov 10 2021 {to_time}:00:00')]

        self.second_file = self.second_file.loc[
            (self.second_file['Zeit'] > f'Tue Nov 10 2021 {from_time}:00:00')
            & (self.second_file['Zeit'] <= f'Tue Nov 10 2021 {to_time}:00:00')]

        self.third_file = self.third_file.loc[
            (self.third_file['Zeit'] > f'Tue Nov 10 2021 {from_time}:00:00')
            & (self.third_file['Zeit'] <= f'Tue Nov 10 2021 {to_time}:00:00')]
        #
        self.fourth_file = self.fourth_file.loc[
            (self.fourth_file['Zeit'] > f'Tue Nov 10 2021 {from_time}:00:00')
            & (self.fourth_file['Zeit'] <= f'Tue Nov 10 2021 {to_time}:00:00')]
        #
        self.fifth_file = self.fifth_file.loc[
            (self.fifth_file['Zeit'] > f'Tue Nov 10 2021 {from_time}:00:00')
            & (self.fifth_file['Zeit'] <= f'Tue Nov 10 2021 {to_time}:00:00')]
        #
        self.sixth_file = self.sixth_file.loc[
            (self.sixth_file['Zeit'] > f'Tue Nov 10 2021 {from_time}:00:00')
            & (self.sixth_file['Zeit'] <= f'Tue Nov 10 2021 {to_time}:00:00')]

        self.__files = [self.first_file, self.second_file, self.third_file, self.fourth_file, self.fifth_file,
                        self.sixth_file]

    def store_all_data(self):
        """
        this method will get the name of the induction loops along with their values and stores it in
        self.__induction_loops = {}
        :return: void
        """
        for file in self.__files:
            # loop_name_values = [[name of induction loop, [values]], [name of induction loop, [values]], ...]
            loop_name_values = self.__calculate_values_of_each_induction_loop(file)
            for induction_loop in loop_name_values:
                self.__induction_loops[induction_loop[0]] = induction_loop[1]



    def __calculate_values_of_each_induction_loop(self, file):
        """
        :param file: DataFrame generated from the csv file
        :return: [[name of induction loop, [values]]]
        """
        columns_of_file = file.columns
        # {name of induction loop: [values]}
        induction_loop_name_and_array_of_values = []
        # find all induction loops in the file
        for induction_loop_number in range(1, len(columns_of_file)):
            # extract the name of induction loop
            name_of_induction_loop = columns_of_file[induction_loop_number].strip().split(sep="-")[0].strip()
            # get the values of cars
            dictionary_of_row_value_of_respective_induction_loop = file[columns_of_file[induction_loop_number]].to_dict()
            values_of_induction_loop = [value for value in
                                        dictionary_of_row_value_of_respective_induction_loop.values()]
            # add it to array
            induction_loop_name_and_array_of_values.append([name_of_induction_loop,values_of_induction_loop])
        return induction_loop_name_and_array_of_values
