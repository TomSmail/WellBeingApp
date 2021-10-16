import soundfile # to read audio file
import numpy as np
import librosa # to extract speech features
import glob
import os
import pickle # to save model after training
from sklearn.model_selection import train_test_split # for splitting training and testing
from sklearn.metrics import mean_squared_error # to measure how good the model is
from sklearn.preprocessing import OrdinalEncoder # mask data that is missing
from xgboost import XGBRegressor # machine learning model
from sklearn.preprocessing import LabelEncoder # makes the y values integers so they can be interpreted by XGBoost



def getFeatures(file_name):
    with soundfile.SoundFile(file_name) as file:
        data = file.read(dtype="float32")
        sampleRate = file.samplerate # This is the number of samples of audio a second 
        stft = np.abs(librosa.stft(data)) # this calcualtes the short-time fourier transform - which is used to determine the frequency and content of sections of a sound wave. 
        result = np.array([]) # results is returned as an array of features which are float values
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampleRate, n_mfcc=40).T, axis=0) # Mel-frequency cepstral coefficients (MFCCs)
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sampleRate).T,axis=0) # finds the different pitches
        mel = np.mean(librosa.feature.melspectrogram(data, sr=sampleRate).T,axis=0) # creates a spectorgram of all of the mel values from the spectrum
        contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sampleRate).T,axis=0) # finds average spectral contrast 
        flatness = np.mean(librosa.feature.spectral_flatness(y=data)) # find the average flatness of the entire spectrum
        result = np.hstack((result, mfccs, chroma, mel, contrast, flatness)) # this flips the data so that the features are displayed in different columns, it flips the rows and colums - Transpose. 
    return result



def load_data(test_size=0.1): #this function is taken from the place i got the voice files
    filenameEmotions = {"01": "neutral","02": "calm","03": "happy","04": "sad","05": "angry","06": "scared","07": "disgusted","08": "shocked"}
    emotionsWanted = {"angry","calm","sad","neutral","happy"}
    XData = []
    yData = []
    for file in glob.glob("../data/Actor_*/*.wav"):       
        basename = os.path.basename(file) # get the base name of the audio file        
        emotion = filenameEmotions[basename.split("-")[2]] # get the emotion label, the last value in the file name corresponds to a dictionary value in filenameEmotions
        if emotion in emotionsWanted: # only certain emotions are needed so we cut off others          
            features = getFeatures(file) # extract speech features          
            XData.append(features) # add the speech features to the data
            yData.append(emotion) # will make up target data in machine learning model
        else:
            continue        
    label_encoder = LabelEncoder()
    label_encoder = label_encoder.fit(yData)
    label_encoded_y = label_encoder.transform(yData)
    splitData = train_test_split(np.array(XData), label_encoded_y, test_size=test_size, random_state=7)
    return splitData  # split the data to training and testing and return it



def XGBoostModelTrain(splitData): # still need to optimise this as it is currently un - optimised. 
    X_train, X_valid, y_train, y_valid = splitData 
    model = XGBRegressor(random_state = 1, n_estimators=500, learning_rate=0.05) # can fidle with this later to see what gets the best outcome
    model.fit(X_train, y_train, early_stopping_rounds=5, eval_set=[(X_valid, y_valid)],verbose=False) # this fits the training data to the model, with the evaluation data being the x and y valid data (testing data)
    preds_valid = model.predict(X_valid) # this passes the valid data to see if it matches with the y data. 
    print("mean squared error:", mean_squared_error(y_valid, preds_valid, squared=False))
    pickle.dump(model, open("result/VoiceEmotion.model", "wb")) # writes model to a file so it can be used later. 



def encodeResults(file_name):
    features = getFeatures(file_name) # extract speech features
    print(features)
    splitFeatures =[features[i:i + 1] for i in range(len(features))]
    modelPrediction(np.array(splitFeatures))



def modelPrediction(voiceData):
    model = pickle.load(open("result/VoiceEmotion.model", 'rb'))
    print(model)
    print(f"This is the prediction for the recording: {model.predict(voiceData)}, taken from voiceData.")





def main():
    encodeResults("03-01-01-01-01-01-01.wav")
    """splitData = load_data(test_size=0.25)
    XGBoostModelTrain(splitData)"""



if __name__ == '__main__':
    print("Running Programn")
    main()
