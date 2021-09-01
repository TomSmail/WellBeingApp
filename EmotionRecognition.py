import soundfile # to read audio file
import numpy as np
import librosa # to extract speech features
import glob
import os
import pickle # to save model after training
from sklearn.model_selection import train_test_split # for splitting training and testing
from sklearn.neural_network import MLPClassifier # multi-layer perceptron model
from sklearn.metrics import accuracy_score # to measure how good we are


def getFeatures(file_name, **kwargs):
    mfcc, chroma, mel, tonnetz, contrast  = kwargs.get("mfcc"), kwargs.get("chroma"), kwargs.get("mel"), kwargs.get("tonnetz"), kwargs.get("contrast")
    with soundfile.SoundFile(file_name) as sound_file:
        