from flask import *
import json
import time
import SpotifyAPIMood2 as sam2
import instagramAPI as ia1

app = Flask(__name__)



@app.route('/', methods=['GET'])
def homePage():
    dataSet = {"Page": "Home","Message": "Loaded the Home page", "Timestamp": time.time()}
    jsonDump = json.dumps(dataSet)
    return jsonDump



@app.route('/request/', methods=['GET'])
def requestPage():
    userQuery = str(request.args.get("user"))
    dataSet = {"Page": "Request","Message": f"Request Accepted for{userQuery}", "Timestamp": time.time()}
    jsonDump = json.dumps(dataSet)
    return jsonDump



@app.route('/InstagramRead/', methods=['GET'])
def InstagramReadPage():
    ia1.writeNewPostToCSV
    dataSet = {"Page": "postRead","Message": "This request gathers new instagram posts.", "Timestamp": time.time()}
    jsonDump = json.dumps(dataSet)
    return jsonDump



@app.route('/spotifyRead/', methods=['GET'])
def spotifyReadPage():
    sam2.spotifyReadFull()
    dataSet = {"Page": "spotifyRead","Message": "This request activates the spotify read emotion function", "Timestamp": time.time()}
    jsonDump = json.dumps(dataSet)
    return jsonDump



@app.route('/emotionInput/', methods=['GET'])
def emotionInputPage():
    emotionValue = str(request.args.get("value"))
    return emotionValue


if __name__ == "__main__":
    app.run()