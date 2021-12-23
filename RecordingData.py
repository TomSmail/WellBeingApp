import SpotifyAPIMood2 as sam2
import instagramAPI2 as ia2
import EmotionRecognition2 as er2
import time
import pandas as pd
import csv
import signal
import time
import requests
from bs4 import BeautifulSoup
import random


# This is to allow for a timeout exception to be thrown
class Timeout(Exception):  
    pass

def handler(sig, frame):
    raise Timeout



def gatherData(backEndTesting, TrainingModel): 

    # Initialises signal function to throw an error if "try" takes too long
    signal.signal(signal.SIGALRM, handler) 
    signal.alarm(30)  
    try:

        # Runs Instagram data gathering
        # Throws 429 sometimes causing this function to barf
        comments, likes  = ia2.instagramEmotion()
        
    except Timeout:
        likes = 0
        comments = 0

    # This code is semi-outdated as I am no longer predicting total mood using ML
    if backEndTesting:
        userInput = int(input("Enter a value 0-10"))
        while type(userInput) != int:
            userInput = input("Enter a value 0-10")
    else:
        if TrainingModel:
            userInput = int(input("Enter a value 0-10"))
            while type(userInput) != int:
                userInput = input("Enter a value 0-10")
        else:
            userInput = 0

    # Creates a new row in csv file and adds all the important data to it
    # This inclues: Instagram (likes and comments), Spotify and Emotion Recognition
    newRow = {"TIME": time.time() ,"INSTAGRAM_l": likes, "INSTAGRAM_c": comments, "SPOTIFY_v": sam2.spotifyReadFull(), "VOICE_e": er2.predictValue("audio2.wav")[0], "USER_i": userInput } 
    headers = ["TIME","INSTAGRAM_l","INSTAGRAM_c","SPOTIFY_v","VOICE_e", "USER_i"]
    file = open('trainingData.csv', 'a') 
    writer = csv.DictWriter(file, headers)
    writer.writerow(newRow)
    file.close()



def interpretData(likesWeight = 1, commentsWeight = 1, spotifyWeight = 1, voiceWeight = 1): 

    # Opens csv and interprets the latest data from each column
    file = open('trainingData.csv', 'r') 
    reader = csv.reader(file)
    rows = []
    for row in reader:
        rows.append(row)
    
    # Each data source has a different weight to change how it effects the mood
    mood = float(rows[-1][1]*likesWeight) + float(rows[-1][2]*commentsWeight) + float(rows[-1][3]*spotifyWeight) + float(rows[-1][4]*voiceWeight)
    print(mood)
    return mood


def outputActions(mood):

    # Each mood level trigers a different output.
    if mood >= 1:

        # Best mood - nothing needs to be done
        message = "Keep up the positivity!"
        return message

    elif mood >= -1 and mood < 1:

        # Creates a happy playlist and notifies user
        sam2.HappyPlayslistFull()
        message = "We have made you a playlist! Listen to it whilst doing something you enjoy"
        return message 

    elif mood <  -1:

        # Creates a happy playlist
        # Takes positive quote from website, sends it to user in notification
        sam2.HappyPlayslistFull()
        page = requests.get("https://www.keepinspiring.me/positive-quotes-and-sayings/")
        soup = BeautifulSoup(page.content, 'html.parser')
        i = random.randint(0, len(soup.find_all(class_ = "wp-block-quote is-style-large")))
        quote = soup.find_all(class_ = "wp-block-quote is-style-large")[i].get_text()
        quoteList = (quote.split("."))
        quoteList.insert(1, "-")
        quote = " ".join(quoteList)
        print("quote:", quote)
        message = quote
        return message
        


def main():
    interpretData()


def training():
    if input("Back End Testing? y/n") == "y":
        backEndTest = True
    else:
        backEndTest = False
    if input("Training Model? y/n") == "y":
        trainingModel = True
    else: 
        trainingModel = False
    gatherData(backEndTest, trainingModel)


if __name__ == '__main__':
    print("Running Programn")
    main()


# I want to be able to ask for how a user is feeling then insert this value along with the values from the different APIs into a new row of a CSV file. It should take the time taken for the test to be run as its primary key
# This is in hopes of creating a database that I can train a Machine learning model on

# needs to gather data from all the different csv files and store as a list with a time stamp as the index  then take this list of values and append it to the end of a csv as a new row. 
