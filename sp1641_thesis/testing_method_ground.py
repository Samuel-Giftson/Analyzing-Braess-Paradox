import networkx as nx
import matplotlib.pyplot as plt
import random
from initialize_csv_file import DataStorage
from scipy.sparse import csr_matrix
import pandas as pd
import numpy as np

G = nx.scale_free_graph(10)
G = nx.DiGraph(G)
G.remove_edges_from(nx.selfloop_edges(G))
G.remove_nodes_from(nx.isolates(G))
#Make graph Unidirectional
for i in G.edges():
    G[i[0]][i[1]]["weight"]= random.randint(10, 100)

for i in G.edges():
    my_edge_reverse = (i[1], i[0])
    if my_edge_reverse not in G.edges():
        G.add_edge(my_edge_reverse[0], my_edge_reverse[1])
        G[my_edge_reverse[0]][my_edge_reverse[1]]["weight"] = random.randint(10, 100)

A = nx.adjacency_matrix(G, weight="weight")


#G2 = nx.DiGraph(A)


my_data_storage_object = DataStorage()
#initial_data = {"Initial Adjacency Matrix": [A], "Braess Adjacaency Matirx": [A],
#                        "Amount of traffic": [1000], "Initial Average Time": [52], "Braess Average Time": [64],
#                        "Graph Specturm": [A], "All average travel time": [[20, 30]]}

#my_data_storage_object.add_data(initial_data)

# TESTING THE EXISTING CSV FILE NOW
my_data_storage_object.retrieve_data()
print("Done")