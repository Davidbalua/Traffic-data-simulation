import unittest
import pandas as pd

from InputData import InputData


class InputDataTest(unittest.TestCase):
    def setUp(self) -> None:
        # simulation is from 16 to 18 for two hours, with 24 intervals. each 5 minutes.
        # the below is the simulation result
        self.simulation_results = {
            "EF_LSA_K251_D001_IS1_1": [25, 34, 12, 23, 23, 23, 34, 45, 56, 23, 34, 45, 56, 45, 56, 54, 45, 12, 23, 34,
                                       54, 56, 67, 68],
            "EF_LSA_K251_D002_IS1": [25, 34, 12, 23, 23, 23, 34, 45, 56, 23, 34, 45, 56, 45, 56, 54, 45, 12, 23, 34, 54,
                                     56, 67, 68]}
        self.input_data = InputData()
        self.input_data.load_data()

    def test_something(self):
        for key, values in self.simulation_results.items():
            self.assertEqual(24,len(values))

    def test_number_of_rows_in_files(self):
        self.assertEqual(864,len(self.input_data.first_file))
        self.assertEqual(864,len(self.input_data.second_file))
        self.assertEqual(864,len(self.input_data.third_file))
        self.assertEqual(864,len(self.input_data.fourth_file))
        self.assertEqual(864,len(self.input_data.fifth_file))
        self.assertEqual(864,len(self.input_data.sixth_file))

    def see_if_filter_of_time_works_well(self):
        self.input_data.filter_data(16, 18)
        self.assertEqual(24,len(self.input_data.first_file))
        self.assertEqual(24,len(self.input_data.second_file))
        self.assertEqual(24,len(self.input_data.third_file))
        self.assertEqual(24,len(self.input_data.fourth_file))
        self.assertEqual(24,len(self.input_data.fifth_file))
        self.assertEqual(24,len(self.input_data.sixth_file))

    def test_the_number_of_stored_induction_loops(self):
        self.input_data.filter_data(16, 18)
        self.input_data.store_all_data()
        print(self.input_data.induction_loops)
        print(len(self.input_data.induction_loops))






if __name__ == '__main__':
    unittest.main()
