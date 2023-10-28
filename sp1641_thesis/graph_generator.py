import networkx as nx
import matplotlib.pyplot as plt
import random


#n is number of nodes
class GraphGenerator:
    def __init__(self, n, min_weight, max_weight):
        self.n = n
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.main_graph = nx.DiGraph()

    def beginning_of_spectrum(self):
        low_g = nx.path_graph(self.n)
        edges_in_low_g = list(low_g.edges())
        G = nx.DiGraph()
        for i in edges_in_low_g:
            G.add_edge(i[0], i[1])
            G[i[0]][i[1]]["weight"] = random.randint(self.min_weight, self.max_weight)
        self.__low_g = None # add

    def middle_spectrum(self):
        pass # add

    def get_low_spectrum(self):
        return self.__low_g
#-------------------------------------------------------------------------------





#--------------------------------------------------------------------------------
    #This should be end of the spectrum.
    #Maxiimum number of edges a directed graph can have would be E=n(n-1)
    #N is number of nodes
    def complete_graph(self):
        if self.main_graph:
            pass
        elif not self.main_graph:
            pass # add




