import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast

from scipy.sparse import csr_matrix
import re
import os


class DataStorage:

    def __init__(self):
        self.file_path = "simulation_data.csv"

        if not os.path.exists(self.file_path):
            self.initialize_a_csv_file()

        self.existing_df = pd.read_csv(self.file_path)

        self.columns_names = np.array(
            ["Initial Adjacency Matrix",
             "Braess Adjacency Matrix",
             "Amount of Traffic",
             "Initial Average Travel Time",
             "Braess Average Travel Time",
             "Graph Spectrum",
             "All Average Travel Time",
             "Number of Nodes",
             "Experiment Name",
             "Braess Paradox Exists"]
        )

    def initialize_a_csv_file(self):
        initial_data = {
            "Initial Adjacency Matrix": [],
            "Braess Adjacency Matrix": [],
            "Amount of Traffic": [],
            "Initial Average Travel Time": [],
            "Braess Average Travel Time": [],
            "Graph Spectrum": [],
            "All Average Travel Time": [],
            "Number of Nodes": [],
            "Experiment Name": [],
            "Braess Paradox Exists": []
        }

        df = pd.DataFrame(initial_data)
        df.to_csv(self.file_path, mode='a', index=False, header=True)

    def add_data(self, new_data: dict) -> None:
        new_df = pd.DataFrame(new_data)
        update_df = self.existing_df.append(new_df, ignore_index=False)
        update_df.to_csv(self.file_path, index=False)

    # This is used later to retrieve out for machine learning
    def retrieve_data(self):
        df1 = pd.read_csv(self.file_path)



        return df1
        #self.test_retrieval(df1)
        # print(data_str)
        # breakpoint()
        # self.testing_if_data_stored_correctly(df1)

    # FUNCTIONS TO TRANSLATE CSV DATA TO ORIGINIAL DATA STRUCTURE
    def create_dict_representation(self, G: nx.classes.digraph.DiGraph) -> dict:
        dict_representation = {}
        for i in G.edges():
            dict_representation[i] = G[i[0]][i[1]]['weight']
        return dict_representation

    def return_graph_from_dict_representation(self, G_dict: dict):
        G = nx.DiGraph()
        for i in G_dict:
            G.add_edge(i[0], i[1], weight=G_dict[i])

        #nx.draw(G, with_labels=True)
        #plt.show()
        return G

    # FUNCTIONS THAT ARE USED TO TRANSLATE DATA STORED IN THE CSV FILE TO USABLE DATA

    # This function is used to turn dicts from string Turning "Graph Spectrum"
    def extract_dicts_from_string_array(self, string_array):
        string = string_array[0]
        dict_list = re.findall(r'{[^}]*}', string)
        return np.array([eval(d) for d in dict_list])

    # This function is used to convert an string in to numpy array, this is used for "All Average Travel Time" column.
    def extract_numpy_array_from_string(self, s) -> np.ndarray:

        # Remove leading and trailing brackets and spaces
        s = s.strip('[]').strip()

        # Split the string using both '.' and ' ' as delimiters, convert to integers, and create a NumPy array
        elements = [int(x) for x in s.replace(',', '').split('.') if x]  # Remove empty strings
        arr = np.array(elements)

        return arr

    # This function is used to convert a string that has one dicitonary in it. It works for the columns named
    # Initial Adjaceny Matrix and Braess Adjacency Matrix
    def turn_one_dict_string_ino_dict(self, my_string):
        output_dict = ast.literal_eval(my_string)

        return output_dict

    def column_five_element_translator(self, string_list):
        my_returning_array = np.array([])
        string_list = string_list.split("\n")

        # Clean the array first element
        string_list[0] = string_list[0].replace("[", "")

        # Clean last element
        string_list[-1] = string_list[-1].replace("]", "")

        for i in string_list:
            string_convereted = self.turn_one_dict_string_ino_dict(i)
            my_returning_array = np.append(my_returning_array, string_convereted)

        del string_list
        return my_returning_array

    # This function made to provide reference of how data is stored in the csv file.
    def help_(self) -> None:
        # Reference for developer
        # Below are columns.
        # initial_data = {
        # "Initial Adjacency Matrix": {edge->tuple:weight->int)}
        # "Braess Adjacency Matirx": {edge->tuple:weight->int)},
        # "Amount of traffic": Int
        # "Initial Average Travel Time": Float,
        # "Braess Average Travel Time": Float,
        # "Graph Specturm": np.array([{edge->tuple:weight->int)}, {edge->tuple:weight->int)}]),
        # "All Average Travel Time": list->int,
        # "Number of Nodes": Int
        # "Experiment Name": Str
        # }

        print("""
        Below is the description of how the data is stored in the csv file.
        
        It was aimed to store less data as possible for the machine learning model without
        loosing the important part of it. 
        
        Data generated by the simulation is stored with option of user. 
        
        The CSV file has 7 headers with it
        
        Initial Adjacency Matrix
        ------The graph before the braess paradox occurred. 
        -----(The graph is store as a dictionary, Dict->{(edge):(edge_weight)}
        
        
        Braess Adjacency Matrix
        ------The graph after the braess paradox has occured., The graph is store as a dictionary. 
        -----(The graph is store as a dictionary, Dict->{(edge):(edge_weight)}
        
        Amount of Traffic
        ------Amount of Bots involed in it. 
        -----(Data in this column is a integer)
        
        Initial Average Travel Time
        ------Average travel time of the graph before the braess paradox has occurred. 
        -----(Data in this column is a floating number)
        
        Braess Average Travel Time
        ------Average travel time of the graph after the braess paradox has occurred.
        -----(Data in this column is a floating number.)
        
        Graph Spectrum
        ------Contains all the graphs in the spectrum involved in the simulation.
         -----The data in this column is a numpy array of all the graphs, where
         ----(The graph is store as a dictionary, Dict->{(edge):(edge_weight)})
        
        All Average Travel Tim
        --Travel Time Associated with it.
        ------Every Graph has an average travel time. 
        -----(The data in this column is stored as a list of integer)
        
        Number of Nodes
        ------Number of nodes the graph has
        
        Experiment Name
        -----Name of the experiment
        ----It is named in the format follow NBOTSNNODES
        ---The other two nodes except N from Nodes will be an integer. N bots dictates the number of bots, N nodes
        ---dictates the number of nodes
        
        """)

    # Test code----------------------------TEST CODES AND FUNCTIONS
    # Testing if data stored properly in the csv file
    def test_retrieval(self, df):
        for i in df[self.columns_names[0]]:
            print(self.turn_one_dict_string_ino_dict(i))
        print("column 0 finished")
        print(" ")
        for i in df[self.columns_names[1]]:
            print(self.turn_one_dict_string_ino_dict(i))
        print("column 1 finished")
        print(" ")

        for i in df[self.columns_names[2]]:
            print(int(i))
        print("Column 2 finished")
        print(" ")

        for i in df[self.columns_names[3]]:
            print(float(i))
        print("column 3 finished")
        print(" ")

        for i in df[self.columns_names[4]]:
            print(float(i))
        print("Column 4 finihsed")
        print(" ")

        t = df[self.columns_names[5]].values
        for i in t:
            my_array = self.column_five_element_translator(i)
            print(my_array)
        print("Column 5 finished")
        print(" ")
        for i in df[self.columns_names[6]]:
            print(self.extract_numpy_array_from_string(i))

        print("Column 6 finished")
        print(" ")

        for i in df[self.columns_names[7]]:
            print(i)
        print("Column 7 finihsed")
        print(" ")

        for i in df[self.columns_names[8]]:
            print(i)

        return None

    def testing_if_data_stored_correctly(self, data_str):
        # self.return_graph_from_dict_representation(data_str[self.columns_names[0]])

        def extract_dicts_from_string_array(string_array):
            string = string_array[0]
            dict_list = re.findall(r'{[^}]*}', string)
            return np.array([eval(d) for d in dict_list])

        # Example usage:
        string_array = data_str[self.columns_names[5]].values
        print(string_array)
        reconstructed_array = extract_dicts_from_string_array(string_array)
        print(reconstructed_array)
        breakpoint()

        for i in reconstructed_array:
            print(type(i))
            self.return_graph_from_dict_representation(i)
        breakpoint()
        print(self.columns_names[6], len(data_str[self.columns_names[6]]))
        print(self.columns_names[7], data_str[self.columns_names[7]])
        return None

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

        # Testing code to see if it still works as existing df keeps file open
        new_data1 = {"K": [23121], "L": [123132]}
        new_df1 = pd.DataFrame(new_data1)
        updated_df = existing_df.append(new_df1, ignore_index=False)
        updated_df.to_csv("t.csv", index=False)
