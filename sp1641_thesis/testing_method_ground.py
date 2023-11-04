import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
from initialize_csv_file import DataStorage
from scipy.sparse import csr_matrix
from graph_generator1 import GraphGenerator1 as gg




t = [23, 20, 17, 15, 10, 12, 0]


# Find the first increasing number
def find_first_increasing_element(arr):
    prev_elem = arr[0]
    prev_elem_idx = 0
    increasing_elem = None
    increasing_elem_idx = None

    for idx, elem in enumerate(arr[1:], start=1):
        if elem > prev_elem:
            increasing_elem = elem
            increasing_elem_idx = idx
            break
        prev_elem = elem
        prev_elem_idx = idx

    return prev_elem, prev_elem_idx, increasing_elem, increasing_elem_idx
print(find_first_increasing_element(t))
breakpoint()
# Testing DataStorage class
#spectrum_dict = np.array([])
#all_average_travle_time = np.array([])

#my_graph_object = gg(5, 100, 10)
#
#G = my_graph_object.get_current_graph()
#my_data_storage_object = DataStorage()

p="""
epoch = len(G.edges())
max_epoch = len(G.nodes()) * ((len(G.nodes())) - 1)

while epoch < max_epoch:
    spectrum_dict = np.append(spectrum_dict, my_data_storage_object.create_dict_representation(G))
    all_average_travle_time = np.append(all_average_travle_time, random.randint(10, 100))

    my_graph_object.add_edges_based_on_probability()
    G = my_graph_object.get_current_graph()
    epoch = len(G.edges())

A = spectrum_dict[0]
A1 = spectrum_dict[1]

# G2 = nx.DiGraph(A)


initial_data = {"Initial Adjacency Matrix": [A], "Braess Adjacency Matrix": [A],
                "Amount of Traffic": [1000], "Initial Average Travel Time": [52], "Braess Average Travel Time": [64],
                "Graph Spectrum": [spectrum_dict], "All Average Travel Time": [all_average_travle_time],
                "Number of Nodes": len(G.nodes())}
my_data_storage_object.add_data(initial_data)

"""

# TESTING THE EXISTING CSV FILE NOW
my_data_storage_object.retrieve_data()
print("Done")
