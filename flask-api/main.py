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

@app.route('/<lmt>', methods=['GET'])
def getbylimit(lmt):
    try:
        limit = int(lmt)  # Convert string to integer
        result = [mongo_to_dict(doc) for doc in col.find().limit(limit)]  # Convert each doc
        return jsonify(result)
    except ValueError:
        return jsonify({'error': 'Invalid limit value'}), 400

@app.route('/', methods=['GET'])
def get():
    return "Hello"



if __name__ == "__main__":
    app.run(debug=True)