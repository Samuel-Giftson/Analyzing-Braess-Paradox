import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
from initialize_csv_file import DataStorage
from scipy.sparse import csr_matrix
from graph_generator1 import GraphGenerator1 as gg
from analyzing_results import AnalyzingResults


my_data_storage_object = DataStorage()

p="""
#Testing DataStorage class
spectrum_dict = np.array([])
all_average_travle_time = np.array([])

my_graph_object = gg(5, 100, 10)
#
G = my_graph_object.get_current_graph()



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
                "Number of Nodes": len(G.nodes()), "Experiment Name":"test1"}
my_data_storage_object.add_data(initial_data)

#Testing, extract duct from a string
"""


# TESTING THE EXISTING CSV FILE NOW
#my_data_storage_object.retrieve_data()
#print("Done")

#Testing Analyzing Results
my_analyzing_result_object = AnalyzingResults()
my_analyzing_result_object.see_difference_of_braess_paradox_to_no_of_nodes()