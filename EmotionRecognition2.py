import soundfile
import numpy as np
import librosa
import csv
import glob
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import OrdinalEncoder
from xgboost import XGBRegressor
import pickle




def getFeatures(fileName):

    # Gather data from file
    with soundfile.SoundFile(fileName) as file:
        
        # Average list of features for each feature type
        data = file.read(dtype="float32")
        sampleRate = file.samplerate 
        stft = np.abs(librosa.stft(data)) 
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampleRate, n_mfcc=40)) 
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sampleRate)) 
        mel = np.mean(librosa.feature.melspectrogram(data, sr=sampleRate)) 
        contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sampleRate)) 
        flatness = np.mean(librosa.feature.spectral_flatness(y=data)) 
        
    return ({ "mfccs": mfccs, "chroma": chroma, "mel": mel, "contrast": contrast, "flatness": flatness, "emotion": "none"})



def writeData(test_size=0.1): 

    # This function is partly from where I got the training data
    filenameEmotions = {"01": "neutral","02": "calm","03": "happy","04": "sad","05": "angry","06": "scared","07": "disgusted","08": "shocked"}
    emotionsWanted = {"angry","calm","sad","neutral","happy"}
    rows = []
    Fields = [ "mfccs", "chroma", "mel", "contrast", "flatness", "emotion"]

    # Cycles through traing data running getFeatures() on each file
    for file in glob.glob("./data/Actor_*/*.wav"):
            basename = os.path.basename(file)     
            emotion = filenameEmotions[basename.split("-")[2]]
            if emotion in emotionsWanted:         
                features = getFeatures(file)        
                features["emotion"] = emotion
                rows.append(features)
            else:
                continue
    
    # Writes rows to a csv file with variable width encoding
    with open("voiceTrainingData.csv", "w", encoding='UTF8', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=Fields)
        writer.writeheader()
        writer.writerows(rows)



def buildModel():

    # Encodes y values so can be interpreted by ML algorithm
    data = pd.read_csv("voiceTrainingData.csv")
    y = data.emotion
    data.drop(['emotion'], axis=1, inplace=True)
    for i in range(len(y)): 
        if y[i] == "sad": # <- Insert Bad Joke
            y[i] = -2
        elif y[i] == "angry": 
            y[i] = -1
        elif y[i] == "neutral": 
            y[i] = 0
        elif y[i] == "calm": 
            y[i] = 1
        elif y[i] == "happy": 
            y[i] = 2

    # Takes training data and builds a ML model
    X_train, X_valid, y_train, y_valid = train_test_split(data, y, train_size=0.8, test_size=0.2,random_state=0)
    Model1 = XGBRegressor(random_state = 420)
    Model1.fit(X_train, y_train)

    # Tests ML model and saves it
    prediction = Model1.predict(X_valid)
    print("Mean Absolute Error:", mean_absolute_error(prediction, y_valid))
    pickle.dump(Model1, open("Code/result/VoiceEmotion.model", "wb"))
    

def predictValue(fileName):

    # Loads ML model and runs prediction on it
    Model1 = pickle.load(open("Code/result/VoiceEmotion.model", 'rb'))
    features = getFeatures(fileName)

    # Formating data for prediction
    del features["emotion"]
    features = pd.DataFrame(features, [0]) # Gets data in same format as "pd.read_csv"
    prediction = Model1.predict(features)
    print(prediction)
    
    return(prediction)



if __name__ == '__main__':
    print("Running Programn")
    predictValue("/home/tomsmail/Documents/0SCHOOL/A-Level/Comp Sci/NEA/Code/audioUpload/audio1.wav")
    
