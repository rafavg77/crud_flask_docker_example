from crypt import methods
from dataclasses import dataclass
import logging
import re
from textwrap import indent
from urllib import response
from flask import Flask, request, json, Response
from pymongo import MongoClient

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoAPI:

    def __init__(self,data):
        self.client = MongoClient("mongodb://mymongo_1:27017/")

        database = data["database"]
        collection = data["collection"]
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def read(self):
        documents = self.collection.find()
        output = [{item : data[item] for item in data if item != '_id' } for data in documents]
        return output
    
    def write(self,data):
        logging.info('Writing Data')
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted','Document_ID':str(response.inserted_id)}
        return output

    def update(self):
        logging.info('Updating Data')
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data):
        logging.info('Deleting Data')
        filt = data['Filter']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output

"""
    def update(self):
        filt = self.data['data']
        updated_data = {'$set': self.data['DataToBeUpdated']}
        response = self.collection.insert_one(filt,updated_data)
        output = {'Status' : 'Successfully Updated' if response.modified_count > 0 else "Nothing was Updated."}
        return output
    
    def delete(self,data):
        filt = data['Document']
        response = self.collection.delete_one(filt)
        output = {'Status' : 'Successfully Deleted' if response.deleted_count > 0 else "Document not found. "}
        return output
"""
@app.route('/')
def base():
    return Response(response=json.dumps({"Status" : "UP"}),status=200,mimetype='application/json')

@app.route('/mongodb', methods=['GET'])
def mongo_reag():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),status=400, mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.read()
    print(response)
    return Response(response=json.dumps(response),status=200,mimetype='application/json')

@app.route('/mongodb', methods=['POST'])
def mongo_write():
    data = request.json
    if data is None or data == {} or 'Document' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.write(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/mongodb', methods=['PUT'])
def mongo_update():
    data = request.json
    logging.info(data)
    if data is None or data == {} or 'DataToBeUpdated' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.update()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/mongodb', methods=['DELETE'])
def mongo_delete():
    data = request.json
    if data is None or data == {} or 'Filter' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.delete(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')

    #data = {
    #        "database" : "crud",
    #        "collection" : "people"
    #}
    #mongo_obj = MongoAPI(data)
    #print(json.dumps(mongo_obj.read(), indent=4))