import json
import os
import heapq
import numpy as np
from pymongo import MongoClient
from configquorum import configquorum
import time
from datetime import datetime

class readquorum(configquorum):
    def __init__(self, MONGOURL, read_threshold, wal_global_file) -> None:
        super().__init__(MONGOURL)
        self.global_file = open(wal_global_file, "r")
        self.global_json = json.load(self.global_file)

        self.threshold = read_threshold

    def read_x(self, az=None, db_name=None, data_item=None):
        return self.client[az][db_name].find_one({"_id":data_item})['value']

    def read(self, request_json):

        reqs = request_json["requests"]
        n = request_json["total_requests"]

        for i in range(n):
            id = reqs[i]["az"]
            name = self.availability_zones[id]['name']

            if self.availability_zones[id]["total_limit"]>self.threshold*self.availability_zones[id]["total_ongoing_requests"]:

                self.availability_zones[id]["total_ongoing_requests"]+=1
                dbs = self.availability_zones[id]["db"]
                limit =  self.availability_zones[id]["limit"]

                

                for db in dbs:
                    if db['status']=='active' and db['designation']!="write" and db['requests']<self.threshold*limit:
                        db['requests']+=1
                        v = self.read_x(az=name, db_name=name+db["id"], data_item=reqs[i]['data_item'])
                        # print(self.read_x(az=name, db_name=name+db["id"], data_item=reqs[i]['data_item']))

                    elif db['status']=='froze' and db['requests']<self.threshold*limit:
                        db['requests']+=1
                        db['consistent_state_no'] = self.unfreeze(az=name, db_name=name+db["id"], consistent_no=db['consistent_state_no'])
                        v = self.read_x(az=name, db_name=name+db["id"], data_item=reqs[i]['data_item'])

                        # print(self.read_x(az=name, db_name=name+db["id"], data_item=reqs[i]['data_item']))

            else:
                new_name = self.find_nearest(name)
                if new_name!=-1:
                    id = self.az_id[new_name]
                    self.availability_zones[id]["total_ongoing_requests"]+=1
                    dbs = self.availability_zones[id]["db"]
                    limit =  self.availability_zones[id]["limit"]

                    for db in dbs:
                        if db['status']=='active' and db['designation']!="write" and db['requests']<self.threshold*limit:
                            db['requests']+=1
                            v = self.read_x(az=name, db_name=name+db["id"], data_item=reqs[i]['data_item'])

                            # print(self.read_x(az=name, db_name=name+db["id"], data_item=reqs[i]['data_item']))

                        elif db['status']=='froze':
                            db['requests']+=1
                            db['consistent_state_no'] = self.unfreeze(az=name, db_name=name+db["id"],consistent_no=db['consistent_state_no'] )
                            # db['status'] = 'active'
                            v = self.read_x(az=name, db_name=name+db["id"], data_item=reqs[i]['data_item'])
                            # print(self.read_x(az=name, db_name=name+db["id"], data_item=reqs[i]['data_item']))
                            

        # print((t2-t1).total_seconds())

     
    def unfreeze(self, az=None, db_name=None, consistent_no=None):
        curr_id = -1

        for j in range(len(self.global_json)):
            
            file_name = 'wal/'+self.global_json[j]['file_name']
            curr_id = self.global_json[j]["id"]
            if curr_id>consistent_no:

                updt_file = open(file_name, 'r')
                updt_json = json.load(updt_file) 

                keys = list(updt_json.keys())

                for i in keys:

                    x = updt_json[i]['dataitem'] 
                    new_val = updt_json[i]['new_val']
                    self.client[az][db_name].update_one({'_id':x},{'$set':{'value':new_val}})

        return curr_id


    def find_nearest(self, az):
        distances = self.calculate_distances(self.az_to_graph[az])
        keys = list(distances.keys())
        vals = list(distances.values())

        for i in range(len(keys)):
            ind = vals.index(min(vals))
            min_node = keys[ind]

            az_node = self.az_id[self.graph_to_az[min_node]]
            if self.availability_zones[az_node]["total_ongoing_requests"]<self.availability_zones[az_node]["total_limit"]:
                return az_node
            else:
                keys.pop(ind)
                vals.pop(ind)
        return -1

    def calculate_distances(self, starting_vertex):
        distances = {vertex: float('infinity') for vertex in self.graph}
        distances[starting_vertex] = 0

        pq = [(0, starting_vertex)]
        while len(pq) > 0:
            current_distance, current_vertex = heapq.heappop(pq)
            if current_distance > distances[current_vertex]:
                continue

            for neighbor, weight in self.graph[current_vertex].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        return distances
