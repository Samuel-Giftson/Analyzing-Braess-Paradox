import networkx as nx
import matplotlib.pyplot as plt
import random


class LinearThresholdModel:
    def __init__(self, bot_dict: dict, bot_network_active: bool = False, amount_of_bots_in_seed: int = 1, seed_set: bool = False ) -> None:
        self.bot_dict = bot_dict
        self.bot_network = nx.scale_free_graph(len(self.bot_dict))
        # There shouldn't be any self loops in it, so we should clean the graph.
        self.bot_network.remove_edges_from(nx.selfloop_edges(self.bot_network))

        # Variables
        self.seed_set = seed_set

        #Variables that determine that this is for bots simulation not for demosntration
        self.bot_network_active = bot_network_active

        # Calling appropriate funcitons
        self.put_bots_in_the_graph()

        if not self.seed_set:
            self.seed_set = []
            self.initialize_seed_set()  # Initializing seed set
            for i in range(amount_of_bots_in_seed):
                self.initialize_seed_set()

        self.bot_network = nx.DiGraph(self.bot_network)
        self.assigning_weights_to_network()
        self.make_whole_graph_unidirectional()

        # self.draw_at_instance()

        #if (len(self.seed_set)) >= 1:
        #    self.spread_at_t0()

    # Functions related to making a bots network
    def put_bots_in_the_graph(self) -> None:
        self.bot_network = nx.relabel_nodes(self.bot_network, self.bot_dict)
        return None

    def assigning_weights_to_network(self) -> None:
        for i in self.bot_network.edges():
            self.bot_network[i[0]][i[1]]["weight"] = float("{:.2f}".format(random.uniform(0, 1)))
        return None

    # Define a seed set
    def initialize_seed_set(self):
        self.seed_set.append(self.choose_a_bot())

    def choose_a_bot(self):
        class_to_be_passed = self.bot_dict[random.randint(0, len(self.bot_dict) - 1)]
        class_to_be_passed.current_status = "active"
        return class_to_be_passed

    # Work on spread of influence
    #def spread_at_t0(self) -> None:
    #    for i in self.seed_set:
    #        edges_set = list(self.bot_network.edges([i]))
     #       self.affect_edges(edges_set, i)
     #   pass

    def spread_at_t(self) -> None:
        for i in self.bot_network:
            if i.current_status == "active":
                edges_set = list(self.bot_network.edges([i]))
                self.affect_edges(edges_set, i)


    # opertaions that need to performed
    # This method will  only work if you call it on bots that has alreadyh been declared
    def affect_edges(self, edges_set, node_affeciting):
        #print("reached here")
        for i in edges_set:
            if i[1].current_status == "active":
                x = "hellp"
                del x
            elif i[1].current_status == "inactive":
                i[1].current_threshold = i[1].current_threshold + (self.bot_network[node_affeciting][i[1]]["weight"])
                #print(i[1].current_threshold, i[1].max_threshold)
                if i[1].current_threshold >= i[1].max_threshold:
                    i[1].current_status = "active"

                    #This is to assign bool value to bot network
                    if self.bot_network_active:
                        i[1].bot_info["Path Taken"] = i[0].bot_info["Path Taken"]

    # THIS FUNCITON TO DISPLAY
    def draw_at_instance(self, color_information: bool = False):
        if (color_information):
            print("Active: red; Inactive: green")

        # Define colors for active and inactive nodes
        node_colors = {
            'active': 'red',  # Set the color for active nodes
            'inactive': 'green'  # Set the color for inactive nodes
        }
        # Determine node colors based on 'current_status' attribute
        # colors = [node_colors[self.bot_network.nodes[node].current_status] for node in self.bot_network.nodes]
        colors = []
        for i in self.bot_network.nodes():
            if i.current_status == "active":
                colors.append("red")
            elif i.current_status == "inactive":
                colors.append("green")
        # Draw the graph with node colors
        nx.draw(self.bot_network, with_labels=False, node_color=colors)

        # Show the plot
        plt.show(block=False)
        plt.pause(5)
        plt.close()

    # Misc methods
    def make_whole_graph_unidirectional(self):
        for i in self.bot_network.edges():
            y = list(i)
            temp_list = list(i)[::-1]
            if tuple(temp_list) not in self.bot_network.edges():
                self.bot_network.add_edge(temp_list[0], temp_list[1], weight=self.bot_network[y[0]][y[1]]['weight'])
