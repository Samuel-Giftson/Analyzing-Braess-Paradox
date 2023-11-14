import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from initialize_csv_file import DataStorage


class AnalyzingResults:
    def __init__(self):
        self.my_data_storage_object = DataStorage()

    def separate_data_according_to_nodes(self, data):
        self.eight_node_experiment_braess_average_travel_time =np.array([])
        self.nine_node_experiment_braess_average_travel_time = np.array([])
        self.ten_node_experiment_braess_average_travel_time = np.array([])
        self.eleven_node_experiment_braess_average_travel_time = np.array([])

        self.eight_node_experiment_number_of_nodes = np.array([])
        self.nine_node_experiment_number_of_nodes = np.array([])
        self.ten_node_experiment_number_of_nodes = np.array([])
        self.eleven_node_experiment_number_of_nodes = np.array([])



        acc = 0
        max_acc = len(data)
        while acc<max_acc:
            row_data = data.loc[acc]
            if row_data["Number of Nodes"] == 8:
                if not pd.isna(row_data["Braess Average Travel Time"]):
                    self.eight_node_experiment_braess_average_travel_time = np.append(self.eight_node_experiment_braess_average_travel_time, row_data["Braess Average Travel Time"])
                    number_of_nodes = self.find_number_of_edges(row_data["Braess Adjacency Matrix"])
                    self.eight_node_experiment_number_of_nodes = np.append(self.eight_node_experiment_number_of_nodes, number_of_nodes)

            if row_data["Number of Nodes"] == 9:
                if not pd.isna(row_data["Braess Average Travel Time"]):
                    self.nine_node_experiment_braess_average_travel_time = np.append(self.nine_node_experiment_braess_average_travel_time,
                                                                                     data["Braess Average Travel Time"])
                    number_of_nodes = self.find_number_of_edges(row_data["Braess Adjacency Matrix"])
                    self.nine_node_experiment_number_of_nodes = np.append(self.nine_node_experiment_number_of_nodes, number_of_nodes)


            if row_data["Number of Nodes"] == 10:
                if not pd.isna(row_data["Braess Average Travel Time"]):
                    self.ten_node_experiment_braess_average_travel_time = np.append(self.ten_node_experiment_braess_average_travel_time,
                                                                                    row_data["Braess Average Travel Time"])
                    number_of_nodes = self.find_number_of_edges(row_data["Braess Adjacency Matrix"])
                    self.ten_node_experiment_number_of_nodes = np.append(self.ten_node_experiment_number_of_nodes, number_of_nodes)

            if row_data["Number of Nodes"] == 11:
                if not pd.isna(row_data["Braess Average Travel Time"]):
                    self.eleven_node_experiment_braess_average_travel_time = np.append(
                        self.eleven_node_experiment_braess_average_travel_time,
                        row_data["Braess Average Travel Time"])
                    number_of_nodes = self.find_number_of_edges(row_data["Braess Adjacency Matrix"])
                    self.eleven_node_experiment_number_of_nodes = np.append(self.eleven_node_experiment_number_of_nodes,
                                                                         number_of_nodes)

            acc = acc+ 1



    def see_difference_of_braess_paradox_to_no_of_nodes(self):
        num_of_nodes_to_average_travel_time = {8:0, 9:0, 10:0}

        data = self.my_data_storage_object.retrieve_data()
        self.separate_data_according_to_nodes(data)
        self.display_from_data_collected()

        #first_row = data.loc[3]
        #number_of_nodes = first_row["Braess Adjacency Matrix"]
        #number_of_nodes = self.find_number_of_edges(number_of_nodes)
        #print(number_of_nodes)

    def display_from_data_collected(self):

        category = ["8 Nodes", "9 Nodes", "10 Nodes", "11 Nodes"]
        values = [np.mean(self.eight_node_experiment_number_of_nodes), np.mean(self.nine_node_experiment_number_of_nodes), np.mean(self.ten_node_experiment_number_of_nodes), np.mean(self.eleven_node_experiment_number_of_nodes)]
        colors = ["green", "blue", "red", "blue"]
        plt.bar(category, values, color = colors)
        plt.show()
        #Ready the graph for 8 nodes

        #Ready the graph for 9 nodes
        #Ready the graph for 10 nodes
        #Ready the graph for 11 nodes
        return None

    def find_number_of_edges(self, adjaceny_matrix):
        dict_representation_of_graph = self.my_data_storage_object.turn_one_dict_string_ino_dict(adjaceny_matrix)
        number_of_nodes = len(dict_representation_of_graph.keys())
        return number_of_nodes