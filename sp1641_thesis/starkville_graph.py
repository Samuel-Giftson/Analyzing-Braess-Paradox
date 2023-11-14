import networkx as nx
import os
import matplotlib.pyplot as plt
import pandas as pd

from initialize_csv_file import DataStorage


class MainMSUCampusGraph:
    def __init__(self):
        self.file_name = "msu_campus_graph.csv"

        #Default Graph unit measaurement
        self.weights_unit = "feet"

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

    def __feet_weights_dict(self, units):

        feet_edge_weight = {(1,2):1056, (2,1):1056,
                            (2,3):1056, (3,2):1056,
                            (3,4):1056, (4,3):1056,
                            (4,5): 2112, (5,4):2112,
                            (5, 6): 1584, (6, 5): 1584,
                            (6, 7): 1584, (7, 6): 1584,
                            (7, 8): 250, (8, 7): 250,
                            (8, 9): 1335.84, (9, 8): 1335.84,
                            (9, 10): 1584, (10, 9): 1584,
                            (10, 11): 1584, (11, 10): 1584,
                            (11, 12): 380.16, (12, 11): 380.16,
                            (12, 13): 1056, (13, 12): 1056,
                            (13, 14): 528, (14, 13): 528,
                            (14, 15): 1056, (15, 14): 1056,
                            (15, 16): 1056, (16, 15): 1056,
                            (16, 4): 394, (4, 16): 394,
                            (14, 2): 1056, (2, 14): 1056,
        }
        miles_edge_weight={ (1,2): 0.4, (2,1): 0.4,
                            (2,3): 0.2, (3,2): 0.2,
                            (3,4): 0.2, (4,3): 0.2,
                            (4,5): 0.4, (5,4): 0.4,
                            (5, 6): 0.3, (6, 5): 0.3,
                            (6, 7): 0.3, (7, 6): 0.3,
                            (7, 8): 0.0473485, (8, 7): 0.0473485,
                            (8, 9): 0.253, (9, 8): 0.253,
                            (9, 10): 0.3, (10, 9): 0.3,
                            (10, 11): 0.3, (11, 10): 0.3,
                            (11, 12): 0.072, (12, 11): 0.072,
                            (12, 13): 0.2, (13, 12): 0.2,
                            (13, 14): 0.1, (14, 13): 0.1,
                            (14, 15): 0.2, (15, 14): 0.2,
                            (15, 16): 0.2, (16, 15): 0.2,
                            (16, 4): 0.07462, (4, 16): 0.07462,
                            (14, 2): 0.3, (2, 14): 0.3,
        }
        if units == "miles":
            return miles_edge_weight
        elif units =="feet":
            return feet_edge_weight

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
        G.add_edge(10, 11); G.add_edge(11, 10)
        G.add_edge(11, 12); G.add_edge(12, 11)
        G.add_edge(12, 13); G.add_edge(13, 12)
        G.add_edge(13, 14); G.add_edge(14, 13)
        G.add_edge(14, 15); G.add_edge(15, 14)
        G.add_edge(15, 16); G.add_edge(16, 15)

        #Directed graph above, below other connections
        G.add_edge(16, 4); G.add_edge(4, 16)
        G.add_edge(14, 2); G.add_edge(2, 14)

        #adding weights
        weight_dictionary = self.__feet_weights_dict(self.weights_unit)

            #-----------------ISSUE FIXED------------------
        #print(len(weight_dictionary.keys()))------TEST CODE
        #print(" ")--------------------------------TEST CODE

        for i in G.edges():
            print(i)
            G[i[0]][i[1]]["weight"]=(weight_dictionary[i]*0.01)

        #print(len(list(G.edges())))---------------TEST CODE
        #for i in weight_dictionary.keys():--------TEST CODE
        #    if i not in list(G.edges()):----------TEST CODE
        #        print(i)--------------------------TEST CODE

        return G



    def load_graph(self):
        my_data_storage_object = DataStorage()
        df1 = pd.read_csv(self.file_name)
        graph_dictionary = df1["Graph Dictionary"][0]
        graph_dictionary = my_data_storage_object.turn_one_dict_string_ino_dict(graph_dictionary)
        G = my_data_storage_object.return_graph_from_dict_representation(graph_dictionary)
        return G

    def display_current_graph(self, G):
        nx.draw(G, with_labels=True)
        plt.show()


