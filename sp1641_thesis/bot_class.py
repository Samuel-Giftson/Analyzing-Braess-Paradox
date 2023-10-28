import random

import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime, date


class CreateBOT:
    def __init__(self, bot_name)->None:
        self.bot_name = bot_name
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.__time_it_was_created = current_time
        self.__date_created = date.today()


        #Call appropriate functions
        self.bot_profile()

        #Variables regarding the time
        self.time_reaching_the_destination  =0

        #Variables for influence maximization model
        self.max_threshold = random.uniform(0,1)
        self.max_threshold = float("{:.2f}".format(self.max_threshold))
        self.current_threshold = 0 #Starts at 0, unless decided otherwise
        self.current_status = "inactive" #starts inactive unless becomes active or part of seed set

        #Misc variable to help with the simulations
        self.current_epoch = 0 #Variable that determine how much travel time it has taken so far
        self.test_var = None


    def bot_profile(self)->None:
        self.bot_info = {"Bot name": self.bot_name, "Date created": self.__date_created,
                           "Time created": self.__time_it_was_created}



    def assign_path(self, path_taking)->None:
        self.bot_info["Path Taken"] = path_taking

        #Initial setting the next destination and current place
        self.traveling()


    def assign_group(self, group_number:int)->None:
        self.__group_number = group_number

    def traveling(self):
        self.current_place = self.bot_info["Path Taken"][0]
        self.current_destination = self.bot_info["Path Taken"][1]

    #Change Functions
    def change_location(self, current_place_)->None:

        self.current_place = current_place_
        next_index = self.bot_info["Path Taken"].index(self.current_place)+1

        if(next_index==len(self.bot_info["Path Taken"])):
            self.current_destination = None
        else:
            self.current_destination = self.bot_info["Path Taken"][next_index]

        if(self.current_destination==None):
            self.time_reaching_the_destination= self.current_epoch

    #Get functions
    def get_bot_name(self)->int:
        return self.bot_name

    def get_group_number(self)->int:
        return self.__group_number

    def get_path_taken(self)->list:
        return self.bot_info["Path Taken"]