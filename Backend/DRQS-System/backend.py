from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import numpy as np
import time
import os
from datetime import datetime
from readquorum import readquorum
from writequorum import writequorum
from traditional import traditional_read, traditional_write
import dotenv
from dotenv import load_dotenv
load_dotenv('config.env')

app = Flask(__name__)

api = Api(app)

class MasterNode(Resource):
    def __init__(self) -> None:
        super().__init__()
        url = os.environ.get('MONGOURL')
        threshold = 1
        wal_global_file = 'wal/wal_global.json'

        self.readq = readquorum(url, threshold, wal_global_file)
        self.writeq = writequorum(url)

        self.tradwrite = traditional_write(url)
        self.tradread = traditional_read(url, threshold, wal_global_file)
        
        pass
    
    def get(self):
        # print(request.data.decode('utf-8'))
        return jsonify({"Response":"Yes"})
    def post(self):
        print("Hello")
        # data = request.get_json()
        data = request.data.decode('utf-8')
        print(data)

        # read_num = int(data['read'])
        # write_num = int(data['write'])
        # print("Hello: ",write_num)

        # # res = self.service_req(read_num, write_num)

        # return jsonify({"Response":"Yes", "ReadNum":read_num})
    
    def service_req(self, read_num, write_num):
        res = []
        trad_res = []
        ri = 0
        rj = int(0.2*read_num)
        wi = 0
        wj = int(0.2*write_num)

        while(ri<read_num or wi<write_num):
            read_req = self.generate_random_read(rj)
            write_req = self.generate_random_write(wj)

            if wi<write_num:
                t1 = time.strftime("%H:%M:%S")
                self.writeq.update_db_lit(write_req)
                t2 = time.strftime("%H:%M:%S")
                res.append(datetime.strptime(t2, "%H:%M:%S") - datetime.strptime(t1, "%H:%M:%S"))

            if ri<read_num:
                t1 = time.strftime("%H:%M:%S")
                self.readq.read(read_req)
                t2 = time.strftime("%H:%M:%S")
                res.append(datetime.strptime(t2, "%H:%M:%S") - datetime.strptime(t1, "%H:%M:%S"))

            if wi<write_num:
                t1 = time.strftime("%H:%M:%S")
                self.tradwrite.update_db_lit(write_req)
                t2 = time.strftime("%H:%M:%S")
                res.append(datetime.strptime(t2, "%H:%M:%S") - datetime.strptime(t1, "%H:%M:%S"))

            if ri<read_num:
                t1 = time.strftime("%H:%M:%S")
                self.tradread.read(read_req)
                t2 = time.strftime("%H:%M:%S")
                trad_res.append(datetime.strptime(t2, "%H:%M:%S") - datetime.strptime(t1, "%H:%M:%S"))

            ri+=rj
            wi+=wj
            
        return {
            "Result":res,
            "Traditional Result":trad_res
        }
    
    
    def generate_random_read(self, num):
        read_json = {
            "total_requests":num,
            "requests":[]
        }
        az_list = self.readq.az_list

        data_item_list = self.readq.data_items
        low_val = 10
        high_val = 1000

        for i in range(num):
            req_json = {
                "az":az_list[np.random.randint(low=0, high=len(az_list))],
                "data_item": data_item_list[np.random.randint(low=0, high=len(data_item_list))]
            }
            read_json['requests'].append(req_json)
        return read_json
    
    def generate_random_write(self, num):
        response = []
        data_item_list = self.writeq.data_items
        low_val = 10
        high_val = 1000
        for i in range(num):
            write_json = {
                data_item_list[np.random.randint(low=0, high=len(data_item_list))]: np.random.randint(low=10, high=1000),
                data_item_list[np.random.randint(low=0, high=len(data_item_list))]: np.random.randint(low=10, high=1000)
            }
            response.append(write_json)
        return response


api.add_resource(MasterNode,'/')

if __name__ == '__main__':
  
    app.run(debug = True)
