import json
import os
import heapq
import numpy as np
from pymongo import MongoClient
import time
from datetime import datetime



class configquorum:
    def __init__(self, MONGOURL) -> None:
        self.client = MongoClient(MONGOURL)

        with open('availability_zones.json','r') as file: 
            self.availability_zones = json.load(file)

        self.az_list = ["AZ_1","AZ_2","AZ_3","AZ_4","AZ_5"]
        
        self.az_id = {
            "IN-KN":"AZ_1",
            "IN-MU":"AZ_2",
            "IN-KT":"AZ_3",
            "IN-DLH":"AZ_4",
            "IN-PT":"AZ_5"
        }
        self.az_to_graph = {
                "IN-KN": "U",
                "IN-MU":"V",
                "IN-KT":"W",
                "IN-DLH":"X",
                "IN-PT":"Y"
            }

        self.graph_to_az = {
                "U":"IN-KN",
                "V":"IN-MU",
                "W":"IN-KT",
                "X":"IN-DLH",
                "Y":"IN-PT",
            }

        self.graph = {
                'U': {'V': 2, 'W': 5, 'X': 1},
                'V': {'U': 2, 'X': 2, 'W': 3},
                'W': {'V': 3, 'U': 5, 'X': 3, 'Y': 1,},
                'X': {'U': 1, 'V': 2, 'W': 3, 'Y': 1},
                'Y': {'X': 1, 'W': 1,},
            }
        
        docs = self.client['IN-KT']['IN-KTdb_1'].find()

        self.data_items = [doc['_id'] for doc in docs]
    
    def update_az(self):
        for az in self.availability_zones.keys():
            self.availability_zones[az]["total_ongoing_requests"] = 0
            for i in range(4):
                self.availability_zones[az]["db"][i]["requests"]=0
        
        with open('availability_zones.json','w') as file: 
            json.dump(self.availability_zones, file)
        return
    