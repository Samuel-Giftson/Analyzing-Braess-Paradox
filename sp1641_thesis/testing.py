import networkx as nx
import matplotlib.pyplot as plt
from graph_generator1 import GraphGenerator1 as gg
from simulation_starter import SimulationStarter as simulating
from bot_class import CreateBOT as cb
from linear_threshold_model import LinearThresholdModel as lt

#my_simulating_object = simulating(10, 100, 10, testing=False)


#Below code is used to test the linear threshold model that was created.
my_bot_dict ={}
for i in range(200):
    my_bot_dict[i] = cb(i)

my_model_object = lt(my_bot_dict)
loop_closer = True
while loop_closer==True:
    my_model_object.draw_at_instance()
    my_model_object.spread_at_t()


    my_list = [my_bot_dict[index].current_status for index in my_bot_dict.keys()]
    counting_active = my_list.count("active")

    percentage_active = (counting_active/len(my_list)) * 100
    print("Currently Active: ", counting_active)
    print("Percentage Active: ", percentage_active)
    print(" ")
    if percentage_active==90.00:
        loop_closer=False
    else:
        loop_closer=True
    threshold_value = [my_bot_dict[index].max_threshold for index in my_bot_dict.keys()]

    #print(my_list)
    #print(threshold_value)


#Time to test the bot network list and spread of information, this was a success
#my_bot_dict = {}
#for i in range(200):
#    my_bot_dict[i] = cb(i)

#print(list(my_bot_dict.values()), "Before linear threshold model: ")
#my_mode_object = lt(my_bot_dict)
#print("After Passing through linear threshold model")
#print(" ")
#for i in range(len(my_bot_dict.keys())):
#    print(i, my_bot_dict[i], my_bot_dict[i].test_var)

#print(my_mode_object.bot_network.nodes())
#for i in range(1000):
#    my_mode_object.spread_at_t()
#    my_mode_object.draw_at_instance()


#my_simulating_object.show_current_graph()
#Testing Graph Generator class

x="""

num_of_nodes = 3
graph_object = gg(num_of_nodes, 100, 1)
number_of_edges = graph_object.get_current_number_of_edges()
limiter = num_of_nodes*(num_of_nodes-1)
print(type(limiter))
#graph_object.draw_graph_at_current_instace()
epoch_counter = 0

def make_(graph, num):
    print("Number of edges: ", num)
    for i in graph.edges():
        print("Edge: ", i[0], i[1], graph[i[0]][i[1]]["weight"])


    #print(G.edges())
    #my_graph_object.display_graph()


while number_of_edges<limiter:
    #epoch_counter = epoch_counter +1
    #print("number of edges: ", number_of_edges, "max limit: ", limiter, "loop counter: ", epoch_counter)
    #number_of_edges  = graph_object.get_current_number_of_edges()
    make_(graph_object.get_current_graph(), graph_object.get_current_number_of_edges())
    graph_object.add_edges_based_on_probability()
    G1 = graph_object.get_current_graph()
    number_of_edges = graph_object.get_current_number_of_edges()
    make_(G1, number_of_edges)
    #graph_object.draw_graph_at_current_instace()
print(number_of_edges)





"""


"""
# Create a scale-free network
G = nx.scale_free_graph(11)
nx.draw(G, with_labels=True)
plt.show()
# Find two nodes with high degree centrality (you can customize this selection)
sorted_nodes = sorted(nx.degree_centrality(G).items(), key=lambda x: x[1], reverse=True)
selected_nodes = [node for node, _ in sorted_nodes[:2]]

# Create a new graph (path graph)
H = nx.Graph()

# Add the selected nodes and an edge between them (to form a path graph)
H.add_nodes_from(selected_nodes)
H.add_edge(selected_nodes[0], selected_nodes[1])

# Display the path graph
nx.draw(H, with_labels=True)
plt.show()

"""