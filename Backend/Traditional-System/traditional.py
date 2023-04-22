import json
import os
import heapq
import numpy as np
from pymongo import MongoClient
from configquorum import configquorum
import time
from datetime import datetime
import dotenv
from dotenv import load_dotenv


class traditional_read(configquorum):
    def __init__(self, MONGOURL, read_threshold, wal_global_file) -> None:
        super().__init__(MONGOURL)
        self.global_file = open(wal_global_file, "r")
        self.global_json = json.load(self.global_file)

        self.threshold = read_threshold
    
    def read_x(self, az=None, db_name=None, data_item=None):
        return self.client[az][db_name].find_one({"_id":data_item})['value']

    def read(self, request_json):
        t1 = time.strftime("%H:%M:%S")

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
                    if  db['designation']!="write" and db['requests']<self.threshold*limit:
                        db['requests']+=1
                        # print(self.read_x(az=name, db_name=name+db["id"], data_item=reqs[i]['data_item']))

                    # elif db['status']=='froze' and db['requests']<self.threshold*limit:
                    #     db['requests']+=1
                    #     db['consistent_state_no'] = self.unfreeze(az=name, db_name=name+db["id"], consistent_no=db['consistent_state_no'])
                    #     print(self.read_x(az=name, db_name=name+db["id"], data_item=reqs[i]['data_item']))

            else:
                new_name = self.find_nearest(name)
                if new_name!=-1:
                    id = self.az_id[new_name]
                    self.availability_zones[id]["total_ongoing_requests"]+=1
                    dbs = self.availability_zones[id]["db"]
                    limit =  self.availability_zones[id]["limit"]

                    for db in dbs:
                        if  db['designation']!="write" and db['requests']<self.threshold*limit:
                            db['requests']+=1
                            # print(self.read_x(az=name, db_name=name+db["id"], data_item=reqs[i]['data_item']))

                        # elif db['status']=='froze':
                        #     db['requests']+=1
                        #     db['consistent_state_no'] = self.unfreeze(az=name, db_name=name+db["id"],consistent_no=db['consistent_state_no'] )
                        #     db['status'] = 'active'
                        #     # print(self.read_x(az=name, db_name=name+db["id"], data_item=reqs[i]['data_item']))
        t2 = time.strftime("%H:%M:%S")
        tdelta = datetime.strptime(t2, "%H:%M:%S") - datetime.strptime(t1, "%H:%M:%S")
        # print("The time taken for read is: ")
        # print(tdelta)
        # print((t2-t1).total_seconds())

     
    def unfreeze(self, az=None, db_name=None, consistent_no=None):
        curr_id = -1

        for j in range(len(self.global_json)):
            
            file_name = self.global_json[j]['file_name']
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


class traditional_write(configquorum):
    def __init__(self, MONGOURL) -> None:
        self.global_file = "wal1/wal_global.json"
        with open('wal1/wal_global.json', "r") as op:
            self.global_json = json.load(op)
        super().__init__(MONGOURL)
        load_dotenv('config.env')

        self.global_id = int(os.environ.get('global_id2'))
        pass
    def update_db_lit(self,new_val_l):
        creation_time = time.strftime("%H_%M_%S")
        lst_up = []
        for i in range(len(new_val_l)):
            # print("H    I ")
            n = self.availability_zones[list(self.availability_zones.keys())[0]]['name']
            self.create_wal_file(f'{n}db_1', self.client[n], new_val_l[i],lst_up)
        # print(lst_up)
        with open(f'wal1/wal_report_{creation_time}.json', 'w') as wal_file:
            json.dump(lst_up, wal_file)

        # wal_file.write(lst_up)
        with open(f'wal1/wal_global.json', "r") as file:
            master = json.load(file)
            master.append({"id": self.global_id, "file_name": f"wal_report_{creation_time}.json"})
        
        
        
        with open(f'wal1/wal_global.json', "w") as file:
            json.dump(master, file)
        self.update_db()
        self.global_id += 1
        dotenv.set_key('config.env', "global_id2", str(self.global_id))

    def update_db(self):
        availability_zones_k = list(self.availability_zones.keys())
        # n = self.availability_zones[availability_zones_k[0]]['name']
        
        for i in range(len(self.availability_zones.keys())):
            
            name = self.availability_zones[availability_zones_k[i]]['name']
            db_l = self.availability_zones[availability_zones_k[i]]['db']
            # db_c = self.client[name]
            for j in range(len(db_l)):
                # if (db_l[j]['status'] != 'froze'):
                
                dd_c_id = f'{name}db_{j+1}'
                consistent_state_no = self.availability_zones[availability_zones_k[i]]['db'][j]['consistent_state_no']
                self.availability_zones[availability_zones_k[i]]['db'][j]['consistent_state_no']  = self.update_thr_file(availability_zones_k[i],dd_c_id,consistent_state_no)
                
                # self.write_update_quorum(dd_c_id, db_c, new_val,db_l[j])
    def write_update_quorum(self,id, db, new_val: dict,db_l):
        new_val_k = list(new_val.keys())
        
        for i in range(len(new_val_k)):
            # getting old values from db and update them simultaneously
            db[id].update_one({'_id': new_val_k[i]}, {
                '$set': {'value': new_val[new_val_k[i]]}})
            db_l['consistent_state_no']+=self.global_id
            

    def create_wal_file(self,id, db, new_val,lst):
        # putting all in wal for that time
        new_val_k = list(new_val.keys())
        data = {}
        for i in range(len(new_val_k)):
            data[i] = {"dataitem": new_val_k[i],
                       "old_val": db[id].find_one({'_id': new_val_k[i]})['value'], "new_val": new_val[new_val_k[i]]}
        
        # data = json.dumps(data)
        lst.append(data)
    
    def update_thr_file(self, az=None, db_name=None, consistent_no=None):
        curr_id = -1
        with open('wal1/wal_global.json', "r") as op:
            self.global_json = json.load(op)
        for j in range(len(self.global_json)):
            
            file_name = 'wal1/'+self.global_json[j]['file_name']
            curr_id = self.global_json[j]["id"]
            # print(self.global_json)
            if curr_id>consistent_no:

                updt_file = open(file_name, 'r')
                updt_jsons = json.load(updt_file) 
                # print(updt_jsons)
                for updt_json in updt_jsons:
                    keys = list(updt_json.keys())
                    for i in keys:

                        x = updt_json[i]['dataitem'] 
                        new_val = updt_json[i]['new_val']
                        self.client[az][db_name].update_one({'_id':x},{'$set':{'value':new_val}})
                        # print(x)
                updt_file.close()

        return curr_id