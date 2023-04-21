from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS
import numpy as np
import time
import os
from datetime import datetime
# from readquorum import readquorum
# from writequorum import writequorum
from masternode import MasterNode
from traditional import traditional_read, traditional_write
import dotenv
from dotenv import load_dotenv
load_dotenv('config.env')



app = Flask(__name__)

cors = CORS(app)

api = Api(app)


class Testing(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.node = MasterNode()


    def post(self):
        data = request.get_json()
        r = data["read"]
        w = data["write"]

        return jsonify(self.node.service_req(r, w))
    
    def get(self):
        return jsonify({"Res: ":"Hello"})
    
api.add_resource(Testing,'/')

if __name__ == '__main__':
  
    app.run(debug = True, threaded=True)