import networkx as nx
import matplotlib
import random

class StoreDataSet:
    def __init__(self):
        pass

    def get_and_store_graph(self, G):
        self.G = G

    def turn_graph_to_matrix(self):
        self.A = nx.adjacency_matrix(self.G, weight='weight')

    def turn_matrix_into_text_file(self):
        pass



