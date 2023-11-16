import networkx as nx
import matplotlib.pyplot as plt
from graph_generator1 import GraphGenerator1 as gg
from simulation_starter import SimulationStarter as simulating
import scipy.sparse as sp
from bot_class import CreateBOT as cb
from linear_threshold_model import LinearThresholdModel as lt




for i in range(100):
    try:
        my_simulating_object = simulating(11, 0.5, 0.01, testing=False, real_life_scenario_test=True)
        del my_simulating_object
    except:
        my_simulating_object = simulating(11, 0.5, 0.01, testing=False, real_life_scenario_test=True)
        del my_simulating_object
