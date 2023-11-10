import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import time
import statistics

# CUSTOM MADE CLASSES THAT ARE MADE FOR BRAESS PARADOX

from braess_paradox_detector import BraessBaradoxDetector as bbd
from graph_generator1 import GraphGenerator1 as gg  # Class made to manipulate and change graphs
from bot_class import CreateBOT as making_bots  # Class made to creat bots
from linear_threshold_model import \
    LinearThresholdModel as information_spread_model  # Class made to simulate the spread of information among bots
from initialize_csv_file import DataStorage


class SimulationStarter:
    def __init__(self, number_of_nodes=10, max_weight=0, min_weight=0, testing=False) -> None:
        # Variables that are objects for the custom classes used in the simulation
        self.my_data_storage_object = DataStorage()
        self.my_graph_object = None
        self.my_linear_threhold_model_object = None

        # PARAMETERS REDEFINITION FOR TO OTHERS TO USE
        self.number_of_nodes = number_of_nodes
        self.max_weight = max_weight
        self.min_weight = min_weight
        self.__testing = testing

        # Variable initiation
        if self.__testing:
            self.G = nx.DiGraph()
            self.test_graph1()

        elif not self.__testing:
            self.G = nx.DiGraph()
            self.start_making_graph()

        # Varialve to conduct operations on Graph
        self.node_list = None

        # self.my_graph_object = None

        self.current_source = 0
        self.current_destinaiton = 0

        self.copy_of_original_graph = None

        # This variable stores all the paths in it
        self.all_paths_list = []
        self.all_shortest_paths = []
        self.shortest_path = []
        self.all_paths_single_cost = []

        # variables for bots
        self.bot_dict = {}  # Contains all the bots, make it easy to access
        self.bot_group_dict = {}  # Contains group number, and put all bots in to groups
        self.num_of_bots = 100  # Variable simply to initialize the number of bots
        self.num_of_groups = 5  # Variable that say how many groups are bots split in to, it changes based on number of
        # paths available from source to target

        # Variable to cull paths,
        self.percent_around = 50  # This variable is used to include paths that are n percent more than the shortest path, as this decreases the amount of paths.
        self.max_amount_of_paths_all_paths_list = 5000  # Max amount of paths to test on
        # It is starts with most minimum path there is, and increases the amount of paths till ther

        # Variables relating to spread of information
        self.my_linear_threhold_model_object = None
        self.loop_breaker_for_influence = 70.00  # This variable is to break the influence, currently it is set for maximum influence
        # Influence mximization model affects till 70 percent of the bots are affected to go to the shortest path

        # Variables for data collection, and to display it
        self.graph_average_travel_time = 0

        self.number_of_edge_list = []
        self.every_epoch_average_travel_time = []

        self.temp_list_of_average_travel_time_of_spread_influence_funciton = []

        # These variable are related to data collection, but this after the spread loop.
        self.all_bot_travel_time_average = []
        self.ratio_of_bots_on_shortest_path_to_other_paths = []

        self.all_graphs_adjacency_matrix = np.array([])
        self.all_graphs_adjacency_matrix_travel_time = np.array([])

        self.graph_spectrum = np.array([])
        self.graph_spectrum_travel_time = []
        self.initial_travel_time = None
        self.initial_travel_time_index = None
        self.braess_travel_time = None
        self.braess_travel_time_index = None

        # Variable related to moving bots in the simulation from one node to another node
        self.start_epoch = 0
        self.max_epoch = 0

        # Calling Appropriate functions automatically------------------------Main self function ----------
        self.start_doing_simulation()
        print("Simulation has finished")

        # Misc Var
        self.mis_var = None

    # FUNCTIONS THAT ARE RELATED IN CREATION OF THE GRAPH, AND MAKING THE GRAPH GROW ARE HERE
    def start_making_graph(self) -> None:
        self.my_graph_object = gg(self.number_of_nodes, self.max_weight, self.min_weight)
        self.copy_of_original_graph = self.my_graph_object.get_current_graph()
        self.G = self.my_graph_object.get_current_graph()

    def make_whole_graph_unidirectional(self):
        for i in self.G.edges():
            y = list(i)
            temp_list = list(i)[::-1]
            if tuple(temp_list) not in self.G.edges():
                self.G.add_edge(temp_list[0], temp_list[1], weight=self.G[y[0]][y[1]]['weight'])

    # This funciton basically grows the graph
    def next_spectrum(self) -> None:
        # self.previous_graph = nx.DiGraph()
        # for i in self.G.edges():
        #    self.previous_graph.add_edge(i[0], i[1], weight = self.G[i[0]][i[1]]["weight"])
        # for j in self.G.nodes():
        #    self.previous_graph.nodes()[j]["parked_bots"] = self.G.nodes()[j]["parked_bots"]
        # del self.G

        self.my_graph_object.add_edges_based_on_probability()
        self.G = self.my_graph_object.get_current_graph()

        # This is for temp graph function, where it will be used to move the bots later
        # self.temp_G = nx.DiGraph()
        # temp_list = list(
        #    map(lambda x: self.temp_G.add_edge(x[0], x[1], weight=self.G[x[0]][x[1]]["weight"]), self.G.edges()))
        # del temp_list
        # for i in self.G.nodes():
        #    self.temp_G.nodes()[i]["parked_bots"] = {}

        return None

    # Call This function everytime the graph changes
    def fill_node_list(self) -> None:
        # print(self.G.nodes())
        self.node_list = list(self.G.nodes())

    def test_graph(self) -> None:
        self.G.add_edge("A", "B", weight=10)
        self.G.add_edge("A", "C", weight=5)
        self.G.add_edge("B", "D", weight=2)
        self.G.add_edge("B", "E", weight=5)
        self.G.add_edge("C", "B", weight=5)
        self.G.add_edge("C", "E", weight=10)
        self.G.add_edge("D", "E", weight=3)
        self.G.add_edge("G", "B", weight=10)
        self.make_whole_graph_unidirectional()
        # print(self.G.edges())

    def test_graph1(self) -> None:
        self.G.add_edge("A", "B", weight=5)
        self.G.add_edge("A", "C", weight=35)
        self.G.add_edge("B", "D", weight=2)
        self.G.add_edge("B", "E", weight=35)
        self.G.add_edge("C", "B", weight=5)
        self.G.add_edge("C", "E", weight=5)
        self.G.add_edge("D", "E", weight=3)
        self.G.add_edge("G", "B", weight=35)
        self.make_whole_graph_unidirectional()
        # print(self.G.edges())

    # FUNCTIONS RELATED TO LINEAR THRESHOLD MODEL
    # These functions are to simulate spread information among the bots
    # This function is to see if the loop of spreading information should go on or not.
    def community_affected(self) -> bool:
        loop_confirmer = False

        bot_status_list = []
        bot_status_list = [self.bot_dict[index].current_status for index in self.bot_dict.keys()]
        counting_active = bot_status_list.count("active")
        percentage_active = (counting_active / len(bot_status_list)) * 100

        if percentage_active > self.loop_breaker_for_influence:
            loop_confirmer = False
        else:
            loop_confirmer = True

        bot_status_list = []

        return loop_confirmer

    def set_seed_set(self):
        for i12 in self.bot_dict.values():
            if i12.bot_info["Path Taken"] in self.shortest_path:
                i12.current_status = "active"

    def do_an_epoch_of_spread_simulation(self):
        self.my_linear_threhold_model_object.spread_at_t()

    # DATA COLLECTION, FUNCTIONS THAT ARE RELATED IN COLLECTING DATA, AND VISUALISING ARE HERE
    # This function is meant to collect all the adjacency matrix of the graphs came in to use
    def collect_adjacency_matrix(self) -> None:
        pass

    # This function is to display change of travel with respect to the addition of edges
    def show_data_after_simulation_finished(self) -> None:
        # print(len(self.number_of_edge_list), len(self.temp_list_of_average_travel_time_of_spread_influence_funciton))
        plt.plot(self.number_of_edge_list, self.temp_list_of_average_travel_time_of_spread_influence_funciton)

        # Collecitng data to store in the csv file
        self.graph_spectrum_travel_time = self.temp_list_of_average_travel_time_of_spread_influence_funciton

        plt.xlabel("Number of edges")
        plt.ylabel("Average Travel Time")
        plt.show()
        self.store_data()

        return None

    # This function is meant to collect data
    def collect_data_to_reveal_braess_paradox(self) -> None:
        self.number_of_edge_list.append(len(self.G.edges()))

        self.temp_list_of_average_travel_time_of_spread_influence_funciton.append(
            statistics.mean(self.all_bot_travel_time_average))

        return None

    # This function is to simply display data collected right after the spreading influence loop
    def show_data_under_spread_influence(self) -> None:
        plt.plot(self.ratio_of_bots_on_shortest_path_to_other_paths, self.all_bot_travel_time_average)

        plt.xlabel("Num of bots on other paths to num of bots on shortest path")
        plt.ylabel("Average Travel Time")

        print(self.ratio_of_bots_on_shortest_path_to_other_paths)
        print(self.all_bot_travel_time_average)

        plt.show()
        return None

    # This function to is to see the average of bots travel time, to how many people are on shortest path
    def collect_travel_time_to_number_of_bots_in_shortest_paths(self) -> None:
        print("Colllecting data....")
        temp_bots_array = np.array(list(self.bot_dict.values()))

        num_of_bots_in_shortest_path = sum(
            [1 for bot in temp_bots_array if bot.bot_info["Path Taken"] in self.shortest_path])
        num_of_bots_in_other_paths = abs(
            self.num_of_bots - num_of_bots_in_shortest_path)  # abs is make sure that it always stays positive
        # print(num_of_bots_in_other_paths, num_of_bots_in_shortest_path)

        if num_of_bots_in_shortest_path == 0:
            print(self.shortest_path)
            print(self.all_paths_list)
            print(self.shortest_path[0] in self.all_paths_list, "Testing")
            for i in self.bot_dict.values():
                print(i.bot_info["Path Taken"])
            breakpoint()
        bot_ratio_of_other_paths_to_num_of_of_bots_shortest_paths = num_of_bots_in_other_paths / num_of_bots_in_shortest_path

        all_destination_time = np.array([bot.time_reaching_the_destination for bot in temp_bots_array])
        average_time_reaching = np.mean(all_destination_time)

        self.all_bot_travel_time_average.append(average_time_reaching)
        self.ratio_of_bots_on_shortest_path_to_other_paths.append(
            bot_ratio_of_other_paths_to_num_of_of_bots_shortest_paths)

        return None

    # This function's goal is to plot Average travel time to number of edge ration
    def collect_number_of_edges_to_average_travel(self):

        for i in self.bot_dict:
            pass

        pass

    # ------------------------------------------------# Main function that does the simulation-------------------------------------------------------------------#
    def start_doing_simulation(self) -> None:

        self.collect_graphs()

        # We need the epoch to go till the graph becomes a complete graph.
        # The formula to obtain complete graph is num of edges = n(n-1)
        self.fill_node_list()
        self.find_target_destination()

        graph_change = 0
        current_num_of_edges = self.my_graph_object.get_current_number_of_edges()
        end_of_epoch_num_of_edges = len(self.G.nodes()) * ((len(self.G.nodes())) - 1)

        # Initialize bots before running simulation
        for i in range(self.num_of_bots):
            self.bot_dict[i] = making_bots(i)

        while current_num_of_edges != end_of_epoch_num_of_edges:
            # Test code to remove====================================
            print("Graph n of the spectrum: ", graph_change)
            print("Before entering in to spreading loop")
            # Test code to remove =======================================

            # Find all the paths
            self.find_all_shortest_paths_to_put_in_list()
            self.find_all_paths()

            # calculating the single person travel time in all paths
            self.calculate_single_travle_time()

            # Test code to see where it is slwoing down==========================================
            # print("Reached before shortening the path")
            # Test code to see where it is slowing down ==========================================

            # Shortening the long list of all paths list
            if len(self.all_paths_list) > self.max_amount_of_paths_all_paths_list:
                # self.shortening_path_list()
                # self.shortening_path_list_version1()
                self.shortening_path_numpy_optimized()
                # print("After shortening: ", len(self.all_paths_list), len(self.all_paths_single_cost))

            number_of_group = len(self.all_paths_list)
            self.num_of_groups = number_of_group

            # split bots in to groups and assign paths to them.
            self.split_bots_in_to_groups()
            self.assign_paths_to_bots()

            # Sometimes there can be a lot of paths in the path list than the amount of bots participating
            # So this function ensures atleast one randomly picked bot would get infected with the
            # knowledge of the shortest path
            self.forceful_affect_a_random_bot()

            # -------Older code not needed
            # starting the simulation by placing bots in their initial location
            # self.park_the_node_at_time_t0()
            # -------Older code not needed

            # This is loop simulates the spread of information among the bots, leading the bots to converge in following
            # the shortest path. Signifies that people eventually take the shortest path.

            loop_confirmer = True

            # inlfuence spread function
            self.my_linear_threhold_model_object = information_spread_model(self.bot_dict, True)
            self.set_seed_set()

            print("About to reach Inside influence spread loop")
            while loop_confirmer == True:
                # Calculte the total travel time for each bots based on other, bots in the edges
                # self.calculate_the_travel_time()
                # self.calculate_the_travel_time_version1()
                self.simulate_movement()
                # self.make_a_function()

                self.collect_travel_time_to_number_of_bots_in_shortest_paths()
                loop_confirmer = self.community_affected()

                # Attempt at spreading influence of shortest path once
                self.do_an_epoch_of_spread_simulation()

            self.collect_data_to_reveal_braess_paradox()
            # self.show_data_under_spread_influence()
            # self.my_graph_object.draw_graph_at_current_instace()

            print("Outside of spreading influence loop")

            # Making status of the bots inactive
            for my_bot in self.bot_dict.values():
                my_bot.current_status = "inactive"
                my_bot.current_epoch = 0



            # Growing the graph
            self.next_spectrum()

            #Collecting Graphs for data collection
            self.collect_graphs()

            current_num_of_edges = self.my_graph_object.get_current_number_of_edges()

            self.testing_current_num_of_edges = current_num_of_edges

            # self.testing_simulation_starter()

            # self.my_graph_object.draw_graph_at_current_instace()
            self.variable_reset()  # resetting the variables after epoch
            graph_change = graph_change + 1
            print(" ")

        self.show_data_after_simulation_finished()

        # breakpoint()

    # ----------------------------------------------End of the main function that does the simulation-------------------------------------------------
    # FUNCTIONS RELATED TO FINDING TARGETS AND DESTINATION
    def find_target_destination(self) -> None:
        # This function is to set to find random targets and random destinations as long there is multiple paths for it.
        self.node_list = list(self.G.nodes())
        temp_list = self.node_list
        max_random_integer = len(self.node_list) - 1

        self.current_source = temp_list[random.randint(0, max_random_integer)]
        temp_list.remove(self.current_source)
        self.current_destination = temp_list[random.randint(0, len(temp_list) - 1)]

        # print(self.current_source, self.current_destination)

    # PATH RELATED FUNCTIONS ARE HERE
    def find_all_paths(self) -> None:
        self.all_paths_list = []
        self.all_paths_list = list(
            nx.all_simple_paths(self.G, source=self.current_source, target=self.current_destination))
        # fastest_weight = (nx.path_weight(self.G, self.shortest_path[0], weight="weight"))
        # threshold_weight = fastest_weight + ((self.percent_around/100)*fastest_weight)
        # paths = []
        # for path in nx.shortest_simple_paths(self.G, self.current_source, self.current_destination, weight='weight'):
        #    total_weight = sum(self.G[u][v]['weight'] for u, v in zip(path, path[1:]))
        #    if total_weight <= threshold_weight:
        #        paths.append(path)

        # self.all_paths_list = paths

    def find_all_shortest_paths_to_put_in_list(self):
        self.shortest_path = []
        self.shortest_path = list(
            p for p in nx.all_shortest_paths(self.G, self.current_source, self.current_destination, weight='weight'))

    def calculate_single_travle_time(self):
        # print("This is under calculate travel time: ", len(self.all_paths_list))
        self.all_paths_single_cost = []
        for j in self.all_paths_list:
            self.all_paths_single_cost.append(nx.path_weight(self.G, j, weight="weight"))

    # FUNCTION THAT DECLARE WHERE BOTS ARE AND ASSIGN PATHS TO BOTS ARE BELOW
    def split_bots_in_to_groups(self):
        group_num = 0
        group_name = "group " + str(group_num)

        for j in range(self.num_of_groups):
            self.bot_group_dict[group_name] = []
            group_num = group_num + 1
            group_name = "group " + str(group_num)

        acc = 0

        for j1 in self.bot_dict.values():

            group_names = list(self.bot_group_dict.keys())
            if acc == len(group_names):
                acc = 0

            my_group_name = "group " + str(acc)
            self.bot_group_dict[my_group_name].append(j1)
            acc = acc + 1

        # print(self.bot_group_dict, "testing hear say")

    def assign_paths_to_bots(self):
        group_name = 0

        for i in range(len(self.all_paths_list)):
            group_name = "group " + str(i)
            for j in range(len(self.bot_group_dict[group_name])):
                my_t = self.bot_group_dict[group_name][j].assign_path(self.all_paths_list[i])

        # print(self.bot_group_dict)
        # self.make_a_function()

    # FUNCTIONS THAT CALCULATE THE TRAVEL TIME OF ALL THE PATHS, AND CONDUCT THE SIMULAITON IS BELOW
    def simulate_movement(self):
        epochs = 0

        while not all(bot.current_destination is None for bot in self.bot_dict.values()):
            for bot in self.bot_dict.values():
                if bot.current_epoch == epochs and bot.current_destination is not None:
                    bot.change_location(bot.current_destination)

            bot_paths = [bot.current_destination for bot in self.bot_dict.values() if
                         bot.current_destination is not None]
            group_dict = {}

            for destination in bot_paths:
                group_dict[destination] = bot_paths.count(destination)

            for bot in self.bot_dict.values():
                if bot.current_epoch == epochs and bot.current_destination is not None:
                    amount_of_bots_heading_to_the_same_location = group_dict[bot.current_destination]
                    the_same_location = group_dict[bot.current_destination]
                    cost_of_traversing = self.G[bot.current_place][bot.current_destination]["weight"]
                    bot_current_epoch = amount_of_bots_heading_to_the_same_location * cost_of_traversing
                    bot.current_epoch += bot_current_epoch

            epochs += 1

    # MISCELLANEOUS FUNCTIONS THAT ARE NEEDED
    def variable_reset(self) -> None:
        self.all_paths_list = []
        self.shortest_path = []
        self.all_paths_single_cost = []

        # DATA COLLECTION VARIABLE RESET ---------------Below two lines caused a problem so needed to be removed
        # self.all_bot_travel_time_average=[]
        # self.ratio_of_bots_on_shortest_path_to_other_paths=[]
        return None

    def forceful_affect_a_random_bot(self) -> None:
        random_value = len(self.bot_dict.values())-1
        bot_name = random.randint(0, random_value)
        del random_value
        if (len(self.shortest_path) > 1):
            random_index = random.randint(0, len(self.shortest_path))
        else:
            random_index = 0
        self.bot_dict[bot_name].assign_path(self.shortest_path[random_index])

        return None

    # As the graph grows, the number of paths increases. In a complete graph, the number of paths between is n!
    # n for being number of nodes, so this is activated to reduce the number of paths to test one, like the important paths
    # The shorter paths rather.
    def shortening_path_numpy_optimized(self) -> None:
        print("before shortening: ", len(self.all_paths_list))

        while len(self.all_paths_list) > 1000:
            # Convert the list of costs to a NumPy array
            all_paths_single_cost = np.array(self.all_paths_single_cost)

            fastest_time = np.min(all_paths_single_cost)
            fastest_time_index = np.argmin(all_paths_single_cost)
            more_var = (self.percent_around / 100) * fastest_time
            more_var = fastest_time + more_var

            # Create a mask for paths to keep
            mask = all_paths_single_cost <= more_var

            # Sort paths and their costs by cost
            sort_indices = np.argsort(all_paths_single_cost)
            all_paths_single_cost = all_paths_single_cost[sort_indices]
            self.all_paths_list = [self.all_paths_list[i] for i in sort_indices]

            # Filter the list of paths and costs based on the mask
            self.all_paths_single_cost = all_paths_single_cost[mask]
            self.all_paths_list = [path for i, path in enumerate(self.all_paths_list) if mask[i]]

            # Insert the paths from self.shortest_path at the beginning of self.all_paths_list
            self.all_paths_list = self.shortest_path + self.all_paths_list

            # Update more_var only if there are around 1000 paths remaining
            if len(self.all_paths_list) <= 1000:
                more_var = more_var - 0.1

        if np.isclose(more_var, fastest_time):
            print(
                "weird issue has been achieved where the percent more value is the same as the fastest time yet the amount of paths has not been reduced")
            breakpoint()

# FUNCTIONS TO COLLECT AND STORE APPROPRIATE DATA, IN THE CSV FILE BUILT FROM ANOTHER CLASS
    # Main function of the store_data function, that sends the data over to csv file
    def store_data(self) -> None:
        user_answer = input("Store Data(Y/N): ")
        answer_array = np.array(["Y", "N", "n", "y"])
        # Ensuring user didn't type anything else
        while user_answer not in answer_array:
            print("Please type (Y/N), thank you. ")
            print(" ")
            user_answer = input("Store Data(Y/N): ")

        if user_answer.upper() == "Y":
            #Call function, to get certain value,
            self.turn_data_to_proper_storage()


            number_of_bots = str(self.num_of_bots) #input("Number of Bots in Experimnet: ")
            number_of_nodes = str(self.number_of_nodes) #input("Number of Nodes in Experiment: ")
            experiment_number = input("What number experiment is this: ")

            experiment_name = number_of_bots + "BOTS" + number_of_nodes + "NODES"+experiment_number+"EXPERIMENT"

            initial_adjacency_matrix = -1
            braess_adjacency_matrix = -1
            braess_paradox_exists=False

            if self.braess_travel_time!=None:

                try:
                    initial_adjacency_matrix = self.graph_spectrum[self.initial_travel_time_index]
                    braess_adjacency_matrix = self.graph_spectrum[self.braess_travel_time_index]
                    braess_paradox_exists = True
                except:
                    print(self.initial_travel_time_index, "initial_travel_time_index")
                    print(self.braess_travel_time_index, "braess_travel_time_index")
                    print(len(self.graph_spectrum))
                    print("Error jhas been recahed")

            elif self.braess_travel_time==None:
                braess_paradox_exists = False

            if braess_paradox_exists:
                print("Existence of Braess Paradox has been confirmed.")

            elif not braess_paradox_exists:
                print("Braess Paradox has not been detected in this simulation. ")



            data_to_be_added = {
                "Initial Adjacency Matrix": [initial_adjacency_matrix],
                "Braess Adjacency Matrix": [braess_adjacency_matrix],
                "Amount of Traffic": [self.num_of_bots],
                "Initial Average Travel Time": [self.initial_travel_time],
                "Braess Average Travel Time": [self.braess_travel_time],
                "Graph Spectrum": [self.graph_spectrum],
                "All Average Travel Time": [self.graph_spectrum_travel_time],
                "Number of Nodes": [self.number_of_nodes],
                "Experiment Name": [experiment_name],
                "Braess Paradox Exists": [braess_paradox_exists]
            }

            self.my_data_storage_object.add_data(data_to_be_added)
            del data_to_be_added

        elif user_answer.upper() == "N":
            print("This simulation has been ended, and exiting out of store_data_method.......")

        return None

    #This function sole purpose is to collect graphs.
    def collect_graphs(self)->None:
        # Data collection
        dict_representation_of_graph = self.my_data_storage_object.create_dict_representation(self.G)
        self.graph_spectrum = np.append(self.graph_spectrum, dict_representation_of_graph)
        return None

    # Formatting the data gathered
    def turn_data_to_proper_storage(self):
        # Passing the list to find the braess paradox
        self.initial_travel_time, self.initial_travel_time_index, self.braess_travel_time, self.braess_travel_time_index = self.find_first_increasing_element(
            self.graph_spectrum_travel_time)

        return None

    # Find the first increasing number
    def find_first_increasing_element(self, arr):
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

    # TEST FUNCTIONS THAT WERE USED TO ENSURE THAT CODE WORKS
    def make_a_function(self):
        path_taken_dict = {}
        for i in self.all_paths_list:
            path_taken_dict[tuple(i)] = 0
        for j in self.bot_dict.values():
            path_taken_dict[tuple(j.bot_info["Path Taken"])] = path_taken_dict[tuple(j.bot_info["Path Taken"])] + 1
        print(path_taken_dict)

    def testing_simulation_starter(self):
        # Test code=======================================================================================
        print("Outside of the loop")
        print("1)This is the length of all_path_list ", len(self.all_paths_list))
        print("2)This is the length of all_path_single_cost: ", len(self.all_paths_single_cost))
        print("3) Shortest Path: ", self.shortest_path)
        print("4) Current source, and destination: ", self.current_source, self.current_destination)
        print("5) Current number of edges: ", self.testing_current_num_of_edges)
        print("6) Number of bots: ", len(self.bot_dict.keys()))
        index1 = self.all_paths_list.index(self.shortest_path[0])
        print("7) Fastet Time: ", self.all_paths_single_cost[index1])
        print("End of simulation before starting next one==========================================")
        print(" ")
        # Test code to be deleted at the end ============================================================

    # ------------------------------------------------END OF FUNCTIONS THAT ARE USED -------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # BELOW FUNCTIONS ARE PROPOSED IN THE INITIAL STAGES, AND MOSTLY REPLACED BY BETTER IMPLEMENTATION TO FASTEN THE SIMULATION

    def shortening_path_list(self) -> None:
        print("before shortening: ", len(self.all_paths_list))

        fastest_time = min(self.all_paths_single_cost)
        fastest_time_index = self.all_paths_single_cost.index(fastest_time)
        more_var = (self.percent_around / 100) * fastest_time
        more_var = fastest_time + more_var

        while len(self.all_paths_list) > self.max_amount_of_paths_all_paths_list:
            for i in reversed(self.all_paths_single_cost):
                if i > more_var:
                    index__ = self.all_paths_single_cost.index(i)
                    # print(i, index__, more_var)
                    self.all_paths_single_cost.remove(i)
                    del self.all_paths_list[index__]

            more_var = more_var - 0.1
            if more_var == fastest_time:
                print(
                    "weird issue has been achieved where the percent more value is same as fastest time yet the amount of paths has not been reduced")
                breakpoint()

        return None

    def shortening_path_list_version1(self):
        print("before shortening: ", len(self.all_paths_list))

        # Convert the list of costs to a NumPy array
        all_paths_single_cost = np.array(self.all_paths_single_cost)

        fastest_time = np.min(all_paths_single_cost)
        fastest_time_index = np.argmin(all_paths_single_cost)
        more_var = (self.percent_around / 100) * fastest_time
        more_var = fastest_time + more_var

        # Create a mask for paths to keep
        mask = all_paths_single_cost <= more_var

        # Filter the list of paths and costs based on the mask
        self.all_paths_single_cost = all_paths_single_cost[mask]
        self.all_paths_list = [path for i, path in enumerate(self.all_paths_list) if mask[i]]

        # Update more_var
        more_var = more_var - 0.1

        if np.isclose(more_var, fastest_time):
            print(
                "weird issue has been achieved where the percent more value is the same as the fastest time yet the amount of paths has not been reduced")
            breakpoint()

    def cull_all_paths_list(self) -> None:
        print("Reached Cull list funciton")

        index_1 = self.all_paths_list.index(self.shortest_path[0])
        fastest_time = self.all_paths_single_cost[index_1]
        # fastest_time = self.all_paths_single_cost[self.all_paths_single_cost.index(self.all_paths_list.index(self.all_shortest_paths[0]))]
        print("Fastest time under cull funciton: ", fastest_time)
        more_var = (self.percent_around / 100) * fastest_time
        more_var = fastest_time + more_var
        print(len(self.all_paths_list), len(self.all_paths_single_cost), more_var)
        # breakpoint()
        for i in reversed(self.all_paths_single_cost):
            if i > more_var:
                index__ = self.all_paths_single_cost.index(i)
                # print(i, index__, more_var)
                self.all_paths_single_cost.remove(i)
                del self.all_paths_list[index__]

        print("after culling: ", len(self.all_paths_list), len(self.all_paths_single_cost))

        return None

    # ----------------------------------------------------------------------------------------
    # Functions for the simulation

    def create_dict_parked_bots(self):
        for i in self.G.nodes():
            self.G.nodes()[i]["parked_bots"] = {}

    # ---------------------------------------------------

    # This part of the code, conducts the moving simulation, by moving the bots from node to node on every epoch
    def calculate_the_travel_time_version1(self):

        destination_of_every_bot = np.array([bot.current_destination for bot in self.bot_dict.values()])

        my_count = np.sum(destination_of_every_bot == None)
        length_of_array = destination_of_every_bot.shape[0]

        current_epoch = 0
        loop_counter = 0
        while my_count != length_of_array:
            if loop_counter > 1000000:
                print("reached breaking point")
                breakpoint()
            loop_counter = loop_counter + 1
            print(loop_counter)

            destination_of_every_bot = self.conduct_simulation_by_moving_bots(current_epoch, destination_of_every_bot)
            my_count = np.sum(destination_of_every_bot == -1)
            current_epoch = current_epoch + 1

    def calculate_amount_of_bot_travel_to_same_location(self, current_epochss):
        grouping_dict = {}
        current_epcoh_destination = []

        for bot in self.bot_dict.values():
            if bot.current_epoch == current_epochss and bot.current_destination != None:
                current_epcoh_destination.append(bot.current_destination)

        # trying to come up wiht unique values
        unique_values = set(current_epcoh_destination)

        for item in unique_values:
            grouping_dict[item] = current_epcoh_destination.count(item)

        return grouping_dict

    def conduct_simulation_by_moving_bots(self, current_epochss, destination_of_every_bot):

        group_dict = self.calculate_amount_of_bot_travel_to_same_location(current_epochss)

        for bot in self.bot_dict.values():
            # print(bot.current_epoch, current_epochss)

            if bot.current_epoch == current_epochss and bot.current_destination != None:

                amount_of_bots_heading_to_same_location = group_dict[bot.current_destination]
                cost_of_traversing = self.G[bot.current_place][bot.current_destination]["weight"]

                bot_current_epoch = amount_of_bots_heading_to_same_location * cost_of_traversing

                bot.current_epoch = bot_current_epoch + bot.current_epoch
                bot.change_location(bot.current_destination)

                if bot.current_destination == None:
                    destination_of_every_bot[bot.bot_name] = -1

        return destination_of_every_bot

    def calculate_the_travel_time(self):

        # Epochs the experiment is conducted of how the bots move.
        epoch_start = 0
        epoch_end = 15000

        while epoch_start != epoch_end:

            temp_G = nx.DiGraph()
            temp_list = list(map(lambda x: temp_G.add_edge(x[0], x[1], weight=self.temp_G[x[0]][x[1]]["weight"]),
                                 self.temp_G.edges()))
            del temp_list
            for i in self.G.nodes():
                temp_G.nodes()[i]["parked_bots"] = {}

            self.move_bot_next_node_current_epoch(epoch_start, temp_G)
            epoch_start = epoch_start + 1

        # for i in self.bot_group_dict.keys():
        # print("group name ", i)
        # for j in self.bot_group_dict[i]:
        #    print(j, j.time_reaching_the_destination, j.current_place)

    # Sub functions of the calculate_the_travel_time()--------------------------------------------------------------------------------------------
    def create_bots_parked_dictionary(self):
        for i in self.G.nodes():
            self.G.nodes()[i]["parked_bots"] = {}
        return None

    def park_the_node_at_time_t0(self):
        for j in self.bot_dict.values():
            path_taken = j.get_path_taken()
            self.G.nodes()[path_taken[0]]["parked_bots"][j] = j.current_epoch

    def move_bot_next_node_current_epoch(self, current_epoch_local, temp_G):

        # print("Begginning of the epoch: ", current_epoch_local)
        # for op in self.G.nodes():
        #    print(op, self.G.nodes[op]["parked_bots"])
        # print(" ")

        # print("Current Epoch: Beginning", current_epoch_local)
        # for i12 in self.G.nodes():
        #    print("Node: ", i12, "Len of Bots", len(self.G.nodes()[i12]["parked_bots"].keys()))
        #    for i123 in self.G.nodes()[i12]["parked_bots"].keys():
        #        print("current Location: ", i123.current_place, "destination: ", i123.current_destination)

        for i in self.G.nodes():

            # Code explaination beginning--gets all the bots that are in current epoch
            my = []
            for key in self.G.nodes()[i]["parked_bots"].keys():
                if key.current_epoch == current_epoch_local and key.current_destination != None:
                    my.append(key)

            # my = list(filter(
            #    lambda key: self.G.nodes()[i]["parked_bots"][key] == current_epoch_local and key.current_destination != None,
            #    self.G.nodes()[i]["parked_bots"].keys()))

            # Code explaination, gets all the bots that are not in the current epoch, and puts them in a list
            # This can be added to the next epoch
            my1 = []
            for bots in self.G.nodes()[i]["parked_bots"].keys():
                if bots.current_epoch != current_epoch_local or bots.current_destination == None:
                    my1.append(bots)

            # print("len of my1", my1)
            # list(filter(
            # lambda key: self.G.nodes()[i]["parked_bots"][key] != current_epoch_local,
            # self.G.nodes()[i]["parked_bots"].keys()))
            # code explaination ending, it puts all the bots that are in current epoch and not in current eepcoh
            # in two separate lists.

            epoch_of_the_group = 0

            grouping_dict = {x: x.current_destination for x in my}

            if len(grouping_dict) != 0:
                grouping_dict1 = {}
                for j in grouping_dict.values():
                    if j in grouping_dict1.keys():
                        grouping_dict1[j] = grouping_dict1[j] + 1
                    elif j not in grouping_dict1.keys():
                        grouping_dict1[j] = 0
            else:
                grouping_dict1 = {}

            # print(i, my, "my")
            for k in my:
                k.current_epoch = ((self.temp_G[k.current_place][k.current_destination]["weight"]) * grouping_dict1.get(
                    k.current_destination)) + k.current_epoch
                past_current_destination = k.current_destination
                k.change_location(k.current_destination)
                temp_G.nodes()[past_current_destination]["parked_bots"][k] = k.current_epoch

            # print(i, my1, "my1")

            for k1 in my1:
                # print("reached here")
                temp_G.nodes()[k1.current_place]["parked_bots"][k1] = k1.current_epoch

            del my, my1

        del self.G
        self.G = nx.DiGraph()

        for my_edges in temp_G.edges():
            self.G.add_edge(my_edges[0], my_edges[1], weight=temp_G[my_edges[0]][my_edges[1]]['weight'])

        for noders in temp_G.nodes():
            self.G.nodes()[noders]["parked_bots"] = temp_G.nodes()[noders]["parked_bots"]

        # temp_list = list(map(lambda x: self.G.add_edge(x[0], x[1], weight = temp_G[x[0]][x[1]]["weight"]), temp_G.edges()))
        # del temp_list

        # temp_list = list(map(lambda node: self.G.nodes[node].update(
        #    {"parked_bots": temp_G.nodes.get(node, {}).get("parked_bots", {})}), self.G.nodes()))
        # del temp_list

        # print("THis is grouping dict", grouping_dict)

        # temp_list = list(map(lambda v: v.change_location(grouping_dict[v]), grouping_dict.keys()))
        # del temp_list

        # print("end of epoch: ", current_epoch_local)
        # for op in self.G.nodes():
        #    print(len(self.G.nodes[op]["parked_bots"]), op, self.G.nodes[op]["parked_bots"])
        # print(" ")
        # self.G = temp_G
        # print("Current Epoch: End", current_epoch_local)
        # for i12 in self.G.nodes():
        #    print("Node: ", i12, "Len of Bots", len(self.G.nodes()[i12]["parked_bots"].keys()))
        #    for i123 in self.G.nodes()[i12]["parked_bots"].keys():
        #        print("current Location: ", i123.current_place, "destination: ", i123.current_destination)

        del temp_G

    # ------------------------------------------------------------------------------------------------------------------------------------

    # Misc methods----------------------------------------------------------------------------------------------

    def make_whole_graph_unidirectional(self):
        for i in self.G.edges():
            y = list(i)
            temp_list = list(i)[::-1]
            if tuple(temp_list) not in self.G.edges():
                self.G.add_edge(temp_list[0], temp_list[1], weight=self.G[y[0]][y[1]]['weight'])

    def visualizing_growing_graph(self):
        self.my_graph_object.display_graph()

        for i in range(100):
            self.my_graph_object.add_edges_based_on_probability()
            G = self.my_graph_object.get_current_graph()
            t = self.my_graph_object.is_complete_graph_(G)
            self.my_graph_object.display_graph()
            self.my_graph_object.random_value_ = self.my_graph_object.random_value_ + 1
            print(self.my_graph_object.random_value_, "length of edges= ", len(G.edges()),
                  self.my_graph_object.is_complete_graph_(G))
            print(t)

    def show_current_graph(self):
        nx.draw(self.G, with_labels=True)
        plt.show()
    # ------------------------------------------------------------------------------------------------------------
