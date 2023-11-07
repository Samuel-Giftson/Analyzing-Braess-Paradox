import networkx as nx
import os
import matplotlib.pyplot as plt
import pandas as pd

from initialize_csv_file import DataStorage


class MainMSUCampusGraph:
    def __init__(self):
        self.file_name = "msu_campus_graph.csv"
        if not os.path.exists(self.file_name):
            self.__initialize_a_csv_file()
        self.existing_df = pd.read_csv(self.file_name)


    #Initialize the file, if it doesnt exist
    def __initialize_a_csv_file(self):
        my_data_storage_object = DataStorage()

        G = self.__initiate_graph()
        dict_representation = my_data_storage_object.create_dict_representation(G)

        initial_data = {
            "Graph Dictionary":[dict_representation]
        }
        df = pd.DataFrame(initial_data)
        df.to_csv("msu_campus_graph.csv", mode = 'a', index = False, header = True)

    def add_data(self, new_data: dict) -> None:
        new_df = pd.DataFrame(new_data)
        update_df = self.existing_df.append(new_df, ignore_index=False)
        update_df.to_csv(self.file_name, index=False)


    def __initiate_graph(self):
        G = nx.DiGraph()
        G.add_edge(1, 2); G.add_edge(2, 1)
        G.add_edge(2, 3); G.add_edge(3, 2)
        G.add_edge(3, 4); G.add_edge(4, 3)
        G.add_edge(4, 5); G.add_edge(5, 4)
        G.add_edge(5, 6); G.add_edge(6, 5)
        G.add_edge(6, 7); G.add_edge(7, 6)
        G.add_edge(7, 8); G.add_edge(8, 7)
        G.add_edge(8, 9); G.add_edge(9, 8)
        G.add_edge(9, 10); G.add_edge(10, 9)
        G.add_edge(10, 11); G.add_edge(10, 11)
        G.add_edge(11, 12); G.add_edge(12, 11)
        G.add_edge(12, 13); G.add_edge(13, 12)
        G.add_edge(13, 14); G.add_edge(14, 13)
        G.add_edge(14, 15); G.add_edge(15, 14)
        G.add_edge(15, 16); G.add_edge(16, 15)

        #Directed graph above, below other connections
        G.add_edge(16, 4); G.add_edge(4, 16)
        G.add_edge(14, 2); G.add_edge(2, 14)

        return G


    def load_graph(self):
        my_data_storage_object = DataStorage()
        df1 = pd.read_csv(self.file_name)
        graph_dictionary = df1["Graph Dictionary"][0]
        G = my_data_storage_object.return_graph_from_dict_representation(graph_dictionary)
        return G

    def display_current_graph(self, G):
        nx.draw(G, with_labels=True)
        plt.show()


