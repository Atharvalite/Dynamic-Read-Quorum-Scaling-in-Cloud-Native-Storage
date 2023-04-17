import json
import os
import heapq
import numpy as np
from pymongo import MongoClient
import time
from datetime import datetime



class configquorum:
    def __init__(self, MONGOURL) -> None:
        client = MongoClient(MONGOURL)

        self.availability_zones = {
            "AZ_1": {
                'name': "IN-KN",
                "az_status": "Working",
                "total_ongoing_requests": 0,
                "total_limit": 60,
                "limit": 20,
                "db": [
                    {"id": 'db_1', 'status': 'active',
                        'designation': 'write', 'requests': 0,'consistent_state_no':-1},
                    {"id": 'db_2', 'status': 'active',
                        'designation': 'write/read', 'requests': 0,'consistent_state_no':-1},
                    {"id": 'db_3', 'status': 'active',
                        'designation': 'write/read', 'requests': 0,'consistent_state_no':-1},
                    {"id": 'db_4', 'status': 'froze', 'designation': 'read', 'requests': 0,'consistent_state_no':-1}
                ]
            },
            "AZ_2": {
                'name': "IN-MU",
                'az_status': 'Working',
                "total_ongoing_requests": 0,
                "total_limit": 60,
                "limit": 20,
                "db": [
                    {"id": 'db_1', 'status': 'active',
                        'designation': 'write', 'requests': 0,'consistent_state_no':-1},
                    {"id": 'db_2', 'status': 'active',
                        'designation': 'write/read', 'requests': 0,'consistent_state_no':-1},
                    {"id": 'db_3', 'status': 'active',
                        'designation': 'write/read', 'requests': 0,'consistent_state_no':-1},
                    {"id": 'db_4', 'status': 'froze', 'designation': 'read', 'requests': 0,'consistent_state_no':-1}
                ]
            },
            "AZ_3": {
                'name': "IN-KT",
                'az_status': 'Working',
                "total_ongoing_requests": 0,
                "total_limit": 60,
                "limit": 20,
                "db": [
                    {"id": 'db_1', 'status': 'active',
                        'designation': 'write', 'requests': 0,'consistent_state_no':-1},
                    {"id": 'db_2', 'status': 'active',
                        'designation': 'write/read', 'requests': 0,'consistent_state_no':-1},
                    {"id": 'db_3', 'status': 'active',
                        'designation': 'write/read', 'requests': 0,'consistent_state_no':-1},
                    {"id": 'db_4', 'status': 'froze', 'designation': 'read', 'requests': 0,'consistent_state_no':-1}
                ]
            },
            "AZ_4": {
                'name': "IN-DLH",
                'az_status': 'Working',
                "total_ongoing_requests": 0,
                "total_limit": 60,
                "limit": 20,
                "db": [
                    {"id": 'db_1', 'status': 'active',
                        'designation': 'write', 'requests': 0,'consistent_state_no':-1},
                    {"id": 'db_2', 'status': 'active',
                        'designation': 'write/read', 'requests': 0,'consistent_state_no':-1},
                    {"id": 'db_3', 'status': 'active',
                        'designation': 'write/read', 'requests': 0,'consistent_state_no':-1},
                    {"id": 'db_4', 'status': 'froze', 'designation': 'read', 'requests': 0,'consistent_state_no':-1}
                ]
            },
            "AZ_5": {
                'name': "IN-PT",
                'az_status': 'Working',
                "total_ongoing_requests": 0,
                "total_limit": 60,
                "limit": 20,
                "db": [
                    {"id": 'db_1', 'status': 'active',
                        'designation': 'write', 'requests': 0,'consistent_state_no':-1},
                    {"id": 'db_2', 'status': 'active',
                        'designation': 'write/read', 'requests': 0,'consistent_state_no':-1},
                    {"id": 'db_3', 'status': 'active',
                        'designation': 'write/read', 'requests': 0,'consistent_state_no':-1},
                    {"id": 'db_4', 'status': 'froze', 'designation': 'read', 'requests': 0,'consistent_state_no':-1}
                ]
            }
        }

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
        
        docs = client['IN-KT']['IN-KTdb_1'].find()

        self.data_items = [doc['_id'] for doc in docs]