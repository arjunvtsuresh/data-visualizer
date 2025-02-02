from flask import Flask
from flask import jsonify
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()
app = Flask(__name__)

uri=os.getenv("CONNECTION_STR")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["BlackCofferDB"]
col = db["CollectDB"]

def mongo_to_dict(mongo_obj):
    mongo_obj['_id'] = str(mongo_obj['_id'])  # Convert ObjectId to string
    return mongo_obj

#get amount of data filter
@app.route('/count/<lmt>', methods=['GET'])
def getbylimit(lmt):
    try:
        limit = int(lmt)  # Convert string to integer
        result = [mongo_to_dict(doc) for doc in col.find().limit(limit)]  # Convert each doc
        return jsonify(result)
    except ValueError:
        return jsonify({'error': 'Invalid limit value'}), 400


# country filter
@app.route('/country/<country>', methods=['GET'])
def getbycountry(country):
    try:
        result = [mongo_to_dict(doc) for doc in col.find({"country":f"{country}"})]
        return jsonify(result)
    except ValueError:
        return jsonify({'error': 'Invalid country value'}), 400

#sector filter
@app.route('/sector/<path:sector>', methods=['GET'])
def getbysector(sector):
    try:
        result = [mongo_to_dict(doc) for doc in col.find({"sector":f"{sector}"})]
        return jsonify(result)
    except ValueError:
        return jsonify({'error': 'Invalid sector value'}), 400

#pestle fitler
@app.route('/pestle/<path:pestle>', methods=['GET'])
def getbypestle(pestle):
    try:
        result = [mongo_to_dict(doc) for doc in col.find({"pestle":f"{pestle}"})]
        return jsonify(result)
    except ValueError:
        return jsonify({'error': 'Invalid pestle value'}), 400
    


@app.route('/', methods=['GET'])
def get():
    return "Welcome to flask Project"



if __name__ == "__main__":
    app.run(debug=True)