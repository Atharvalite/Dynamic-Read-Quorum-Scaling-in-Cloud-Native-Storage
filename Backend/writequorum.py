import json
import os
import heapq
import numpy as np
from pymongo import MongoClient
from configquorum import configquorum
import time
import dotenv
from dotenv import load_dotenv


class writequorum(configquorum):
    def __init__(self, MONGOURL) -> None:
        super().__init__(MONGOURL)

        load_dotenv('config.env')

        self.global_id = int(os.environ.get('global_id'))

        pass
    def update_db_lit(self,new_val_l):
        creation_time = time.strftime("%H_%M_%S")
        lst_up = []
        for i in range(len(new_val_l)):
            n = self.availability_zones[list(self.availability_zones.keys())[0]]['name']
            self.create_wal_file(f'{n}db_1', self.client[n], new_val_l[i],lst_up)
            self.update_db(new_val_l[i])

        with open(f'wal/wal_report_{creation_time}.json', 'w') as wal_file:
            json.dump(lst_up, wal_file)

        # wal_file.write(lst_up)
        with open(f'wal/wal_global.json', "r") as file:
            master = json.load(file)
        master.append(
            {"id": self.global_id, "file_name": f"wal_report_{creation_time}.json"})
        
        
        self.global_id += 1
        dotenv.set_key('config.env', "global_id", str(self.global_id))
        
        with open(f'wal/wal_global.json', "w") as file:
            json.dump(master, file)
          

    def update_db(self, new_val):
        availability_zones_k = list(self.availability_zones.keys())
        n = self.availability_zones[availability_zones_k[0]]['name']
        # self.create_wal_file(f'{n}db_1', self.client[n], new_val)
        for i in range(len(self.availability_zones.keys())):
            name = self.availability_zones[availability_zones_k[i]]['name']
            db_l = self.availability_zones[availability_zones_k[i]]['db']
            db_c = self.client[name]
            for j in range(len(db_l)):
                if (db_l[j]['status'] != 'froze'):
                    dd_c_id = f'{name}db_{j}'
                    self.write_update_quorum(dd_c_id, db_c, new_val,db_l[j])

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
        
   