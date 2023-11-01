import numpy as np
import pandas as pd
import networkx as nx
from scipy.sparse import csr_matrix
import re
import os


class DataStorage:

    def __init__(self):
        self.file_path = "ten_nodes_hundered_bots.csv"
        self.file_names = ["ten_nodes_hundered_bots.csv", "nine_nodes_hundered_bots.csv",
                           "seven_nodes_hundered_bots.csv"]

        if not os.path.exists(self.file_path):
            self.__initialize_a_csv_file()

        self.existing_df = pd.read_csv(self.file_path)


    def __initialize_a_csv_file(self):
        initial_data = {"Initial Adjacency Matrix": [], "Braess Adjacaency Matirx": [],
                        "Amount of traffic": [], "Initial Average Time": [], "Braess Average Time": [],
                        "Graph Specturm": [], "All average travel time": []}

        df = pd.DataFrame(initial_data)
        df.to_csv("ten_nodes_hundered_bots.csv", mode='a', index=False, header=True)

    def add_data(self, new_data: dict) -> None:
        new_df = pd.DataFrame(new_data)
        update_df = self.existing_df.append(new_df, ignore_index=False)
        update_df.to_csv(self.file_path, index=False)

    def retrieve_data(self):
        df1 = pd.read_csv(self.file_path)

        A = df1["Initial Adjacency Matrix"].to_list()
        data_str = A[0]

    def return_sparse_matrix(self, data_str):
        matrix_dict = {}
        data_str = data_str.replace(' ','')
        data_str = data_str.replace('\t', '')
        # Define the regular expression pattern to match text between parentheses
        pattern = r'\((.*?)\)'
        # Use re.findall to extract the matches
        matches = re.findall(pattern, data_str)

        # Print the list of matches
        for i in matches:
            print(i[0], i[2])



    #Test code
    def testing(self):
        data = {"K": [1, 3], "L": [23, 23]}
        df = pd.DataFrame(data)
        df = df.to_csv("t.csv", mode='a', index=False, header=True)
        new_data = {"K": [23], "L": [90]}
        existing_df = "t.csv"
        existing_df = pd.read_csv("t.csv")
        new_df = pd.DataFrame(new_data)
        updated_df = existing_df.append(new_df, ignore_index=False)
        updated_df.to_csv("t.csv", index=False)

        #Testing code to see if it still works as existing df keeps file open
        new_data1 = {"K": [23121], "L": [123132]}
        new_df1 = pd.DataFrame(new_data1)
        updated_df = existing_df.append(new_df1, ignore_index=False)
        updated_df.to_csv("t.csv", index=False)





















