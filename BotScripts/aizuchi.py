from utilities.utilitie import *

class Aizuchi:
    def __init__(self):
        aizuchi_file_name = 'CSVFiles/AIZUCHI/AizuchiResponse.csv'
        self.aizuchis = [aizuchi[0] for aizuchi in read_csv(aizuchi_file_name)]

    def aizuchi(self):
        return random.choice(self.aizuchis)