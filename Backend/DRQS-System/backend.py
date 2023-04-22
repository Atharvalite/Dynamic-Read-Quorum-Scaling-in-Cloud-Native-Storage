from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS
import numpy as np
import time
import os
from datetime import datetime
from readquorum import readquorum
from writequorum import writequorum
from masternode import MasterNode
from traditional import traditional_read, traditional_write
import dotenv
from dotenv import load_dotenv
import json
load_dotenv('config.env')



app = Flask(__name__)

port=5000

cors = CORS(app)

api = Api(app)

res = [0]

class Testing(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.node = MasterNode()
        # self.res = [0]


    def post(self):
        # print("Hello World")
        data = request.get_json()
        print(data)
        r = data["read"]
        w = data["write"]
        # print("Read: ",r)
        # print("Write: ",w)
        # jsonify(self.node.service_req(r, w))
        res = self.node.service_req(r, w)

        with open('result.json','w') as file: 
            json.dump({"result":res}, file)
        print("Request Served")
        return res
    
    def get(self):
        with open('result.json','r') as file: 
            r = json.load(file)
        return r["result"]
    
api.add_resource(Testing,'/')

if __name__ == '__main__':
  
    app.run(debug = True, port=port)