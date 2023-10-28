import networkx as nx
import matplotlib.pyplot as plt
import random


class GraphGenerator1:
    def __init__(self, number_of_nodes: int, max_edge_weight: int =0, min_edge_weight :int  =0) -> None:
        self.number_of_nodes = number_of_nodes
        self.G = nx.scale_free_graph(number_of_nodes)
        self.max_edge_weight= max_edge_weight
        self.min_edge_weight = min_edge_weight

        # Clean the generated graph
        self.__clean_the_graph()

        # Finding the hubs
        self.__find_hubs()

        # Focused graph holds the main scale free graph
        self.focused_graph = self.G

        # spannig path graph
        self.__span_path_graph()
        self.begginning_of_the_spectrum = self.G
        self.make_path_graph_into_unidirectional_graph()
        self.add_weights_to_graph()

        #Variable to determine the curent number of edges
        self.number_of_edges = len(self.G.edges())

        #misc Variable
        self.random_value_ = 0

    def __clean_the_graph(self) -> None:
        # There shouldn't be any self loops in it, so we should clean the graph.
        self.G.remove_edges_from(nx.selfloop_edges(self.G))

        # There shouldn't be any isolated vertices
        self.G.remove_nodes_from(nx.isolates(self.G))

        # There shouldn't be any duplicate edges between same pair of nodes
        self.G = nx.DiGraph(self.G)

        # It should be a two way directional nodes, one from node a to node b, and back to node b to node a,
        # to imitate real cities and road ways
        for i in self.G.edges():
            temp = list(i)[::-1]
            self.G.add_edge(temp[0], temp[1])

    def __find_hubs(self) -> None:
        degree_centrality = nx.degree_centrality(self.G)
        sorted_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
        self.sorted_nodes = sorted_nodes

    def __span_path_graph(self) -> None:
        self.G = nx.path_graph(self.number_of_nodes)
        self.temp_graph = nx.DiGraph()
        temp_list = list(map(lambda x: self.temp_graph.add_edge(x[0], x[1]), self.G.edges()))
        del temp_list
        self.G = self.temp_graph

    def make_path_graph_into_unidirectional_graph(self)->None:
        for i in self.G.edges():
            temp = list(i)[::-1]
            self.G.add_edge(temp[0], temp[1])

    def add_edges_based_on_probability(self)->None:
        #print(self.sorted_nodes)
        for i in self.sorted_nodes:
            target_node = random.randint(0, self.number_of_nodes - 1)

            # picking another node to make a connection with.
            while (target_node, i[0]) in self.G.edges():
                target_node = random.randint(0, self.number_of_nodes - 1)
            if target_node==i[0]:
                continue


            if random.random() < i[1]:
                #--Testing Code---- print("reached here")
                assigned_weight = random.randint(self.min_edge_weight, self.max_edge_weight)
                self.G.add_edge(target_node, i[0], weight = assigned_weight )

                #If we are gonna keep  it realistic, we have
                #add roads in out of city to city this makes
                #roads to go both direction
                uni_direction = (i[0], target_node)

                if uni_direction not in self.G.edges():
                    self.G.add_edge(i[0], target_node, weight = assigned_weight)

        self.number_of_edges = len(self.G.edges())
        #print(len(self.G.edges()))

    def get_current_graph(self):
        return self.G

    def get_current_number_of_edges(self):
        return self.number_of_edges

    def display_graph(self)->None:

        nx.draw(self.G, with_labels=True)
        plt.show(block=False)
        plt.pause(10)
        plt.close()
        self.random_value_=self.random_value_+1
        print(self.random_value_)
        print(self.is_complete_graph_(self.G))

    def draw_graph_at_current_instace(self):
        nx.draw(self.G, with_labels=True)
        plt.show()

    def add_weights_to_graph(self):
        #Testing error of empty range, should work properly now
        #print(self.min_edge_weight, self.max_edge_weight)
        for i in self.G.edges():
            self.G[i[0]][i[1]]['weight'] = random.randint(self.min_edge_weight, self.max_edge_weight)

#-------------------------------------------------
#This functions are to miscellaneous

    def is_complete_graph_(self, G)->bool:
        checker = len(G.nodes())*(len(G.nodes)-1)
        if (len(G.edges()) == checker):
            return True
        elif (len(G.edges) != checker):
            return False

