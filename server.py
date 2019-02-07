# import modules
from flask import Flask, jsonify
import requests
from pymongo import MongoClient


app = Flask(__name__)
mongo_uri = "mongodb://<mLab_username>:<mLab_password>@ds145299.mlab.com:45299/mydbinstance"
client = MongoClient(mongo_uri)
db = client.mydbinstance
yelp_collection = db.yelp

@app.route('/')
def index():
    return "Hello"

@app.route('/LA')
def LA():
    try:
        query = {}
        la_result = [item['restaurants']['Los Angeles'] for item in list(yelp_collection.find(query))]
    except:
        la_result = "failed"
    finally:
        return jsonify({'Restaurants':la_result})

@app.route('/SF')
def SF():
    try:
        query = {}
        sf_result = [item['restaurants']['San Francisco'] for item in list(yelp_collection.find(query))]
    except:
        sf_result = "failed"
    finally:
        return jsonify({'Restaurants':sf_result})

@app.route('/NY')
def NY():
    try:
        query = {}
        ny_result = [item['restaurants']['New York'] for item in list(yelp_collection.find(query))]
    except:
        ny_result = "failed"
    finally:
        return jsonify({'Restaurants':ny_result})

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
