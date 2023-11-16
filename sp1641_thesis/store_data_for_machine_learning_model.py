import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
import random

import numpy as np

from initialize_csv_file import DataStorage

#This class is specifically to simply transform data
class GetDataForGNN:
    def __init__(self)->None:
        self.my_initialize_csv_onject = DataStorage()
        self.number_of_nodes = 0

    def retrieve_data(self):
        df1 = self.my_initialize_csv_onject.retrieve_data()
        return df1

    def get_data(self, num_of_nodes):
        x_data = np.array([])
        y_data = np.array([])
        current_data = self.retrieve_data()

        self.number_of_nodes = num_of_nodes

        #Retrieving graph for num_of_nodes
        acc = 0
        max_acc = len(current_data)
        while acc<max_acc:
            row_data = current_data.loc[acc]
            if row_data["Number of Nodes"] == self.number_of_nodes:
                if row_data["Braess Paradox Exists"]:
                    my_matrix, node_value_higher = self.return_matrix(row_data["Initial Adjacency Matrix"], row_data)

                    if not node_value_higher:
                        x_data = np.append(x_data, my_matrix)
                        y_data = np.append(y_data, 1)

                elif not row_data["Braess Paradox Exists"]:
                    my_matrix = self.return_matrix_incase_of_braess_paradox_doesnt_exist(row_data["Graph Spectrum"])
                    x_data = np.append(x_data, my_matrix)
                    y_data = np.append(y_data, 0)

            acc = acc+1

        return x_data, y_data



    #FUNCTIONS TO CONVERT GIVEN DATA TO PROPER FORMAT
    def return_matrix(self, matrix_string, row_data):
        node_value_higher = False
        matrix_dict = self.my_initialize_csv_onject.turn_one_dict_string_ino_dict(matrix_string)
        G = self.my_initialize_csv_onject.return_graph_from_dict_representation(matrix_dict)
        my_matrix = nx.adjacency_matrix(G, weight="weight")
        if len(G.nodes())>self.number_of_nodes:
            node_value_higher = True

        return my_matrix, node_value_higher

    def return_matrix_incase_of_braess_paradox_doesnt_exist(self, graph_spectrum):
        my_matrix = 0
        converted_graph_spectrum  = self.my_initialize_csv_onject.column_five_element_translator(graph_spectrum)

        random_index = random.randint(0, len(converted_graph_spectrum)-1)
        matrix_dict = converted_graph_spectrum[random_index]

        G = self.my_initialize_csv_onject.return_graph_from_dict_representation(matrix_dict)
        my_matrix = nx.adjacency_matrix(G, weight="weight")

        return my_matrix

p="""
class StoreDataSet:
    def __init__(self):
        self.my_csv_file_object = DataStorage()

    def get_and_store_graph(self, G):
        self.G = G

    def turn_graph_to_matrix(self):
        self.A = nx.adjacency_matrix(self.G, weight='weight')

    def turn_matrix_into_text_file(self):
        pass



"""