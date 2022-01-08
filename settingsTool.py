import pandas as pd
import csv

def writeSetting(likesWeight = 1, commentsWeight = 1, spotifyWeight = 1, voiceWeight = 1):
    settings = {"likesWeight" : [likesWeight], "commentsWeight":  [commentsWeight], "spotifyWeight": [spotifyWeight], "voiceWeight": [voiceWeight]}
    df = pd.DataFrame.from_dict(settings)
    print(df)
    df.to_csv("settings.txt", mode = "w" )
    
def readSetting(likesWeight = True, commentsWeight = True, spotifyWeight = True, voiceWeight = True):
    file = open("settings.txt", "r")
    reader = csv.DictReader(file)
    dictionary = list(reader)[0]
    del dictionary[""]

    return dictionary


