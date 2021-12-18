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
    with soundfile.SoundFile(fileName) as file:

        data = file.read(dtype="float32")
        sampleRate = file.samplerate # This is the number of samples of audio a second 
        stft = np.abs(librosa.stft(data)) # this calcualtes the short-time fourier transform - which is used to determine the frequency and content of sections of a sound wave. 
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampleRate, n_mfcc=40)) # Mel-frequency cepstral coefficients (MFCCs)
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sampleRate)) # finds the different pitches
        mel = np.mean(librosa.feature.melspectrogram(data, sr=sampleRate)) # creates a spectorgram of all of the mel values from the spectrum
        contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sampleRate)) # finds average spectral contrast 
        flatness = np.mean(librosa.feature.spectral_flatness(y=data)) # find the average flatness of the entire spectrum
    return ({ "mfccs": mfccs, "chroma": chroma, "mel": mel, "contrast": contrast, "flatness": flatness, "emotion": "none"})



def writeData(test_size=0.1): #this function is taken from the place i got the voice files
    filenameEmotions = {"01": "neutral","02": "calm","03": "happy","04": "sad","05": "angry","06": "scared","07": "disgusted","08": "shocked"}
    emotionsWanted = {"angry","calm","sad","neutral","happy"}
    rows = []
    Fields = [ "mfccs", "chroma", "mel", "contrast", "flatness", "emotion"]
    for file in glob.glob("./data/Actor_*/*.wav"):
            basename = os.path.basename(file) # get the base name of the audio file        
            emotion = filenameEmotions[basename.split("-")[2]] # get the emotion label, the last value in the file name corresponds to a dictionary value in filenameEmotions
            if emotion in emotionsWanted: # only certain emotions are needed so we cut off others          
                features = getFeatures(file) # extract speech features          
                features["emotion"] = emotion
                rows.append(features)
            else:
                continue
    print(rows)
    with open("voiceTrainingData.csv", "w", encoding='UTF8', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=Fields)
        writer.writeheader()
        writer.writerows(rows)



def buildModel():
    data = pd.read_csv("voiceTrainingData.csv")
    y = data.emotion
    data.drop(['emotion'], axis=1, inplace=True)
    for i in range(len(y)): # ordinal encoding
        if y[i] == "sad": # <- Insert Poor Joke
            y[i] = -2
        elif y[i] == "angry": 
            y[i] = -1
        elif y[i] == "neutral": 
            y[i] = 0
        elif y[i] == "calm": 
            y[i] = 1
        elif y[i] == "happy": 
            y[i] = 2
    X_train, X_valid, y_train, y_valid = train_test_split(data, y, train_size=0.8, test_size=0.2,random_state=0)
    Model1 = XGBRegressor(random_state = 420)
    Model1.fit(X_train, y_train)
    print(X_valid)
    prediction = Model1.predict(X_valid)
    print("Mean Absolute Error:", mean_absolute_error(prediction, y_valid))
    pickle.dump(Model1, open("Code/result/VoiceEmotion.model", "wb"))
    

def predictValue(fileName):
    Model1 = pickle.load(open("Code/result/VoiceEmotion.model", 'rb'))
    features = getFeatures(fileName)
    del features["emotion"]
    features = pd.DataFrame(features, [0]) # Gets data in same format as "pd.read_csv"
    print(features)
    prediction = Model1.predict(features)
    print(prediction)
    return(prediction)



        


if __name__ == '__main__':
    print("Running Programn")
    predictValue("audio.wav")
    
