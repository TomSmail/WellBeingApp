from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import os
import sys 
#import RecordingData as rd1



app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
CORS(app)


allowed = [".mp3", ".wav", ".flac", ".m4a", ".MP3"]

@app.route('/', methods= ['GET', 'POST'])
def get_message():

    # Returns index file
    print("Rendering index.html from templates file")
    return render_template("index.html")



@app.route('/run_script', methods=['POST'])
def run_script():

    print("Got request for /run_script")
    print(request.files)
    file = request.files['static_file']
    if os.path.splitext(file.filename)[1] in allowed:
        file.save(os.path.join("/home/tomsmail/Documents/0SCHOOL/A-Level/Comp Sci/NEA/Code/audioUpload", file.filename))
        #rd1.backEndWorkflow(file)

    else:  
        resp = {"success": False, "response": "Illegal File"}
        return jsonify(resp), 312
    
    resp = {"success": True, "response": "File has been saved!"}
    return jsonify(resp), 200



if __name__ == "__main__":
 app.run(host='0.0.0.0', debug=True)