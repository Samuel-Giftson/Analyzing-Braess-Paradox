import networkx as nx
import matplotlib.pyplot as plt
from graph_generator1 import GraphGenerator1 as gg
from simulation_starter import SimulationStarter as simulating
import scipy.sparse as sp
from bot_class import CreateBOT as cb
from linear_threshold_model import LinearThresholdModel as lt





my_simulating_object = simulating(10, 100, 10, testing=False, real_life_scenario_test=False)
del my_simulating_object

