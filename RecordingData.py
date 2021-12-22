import SpotifyAPIMood2 as sam2
import instagramAPI as ia1
import EmotionRecognition2 as er2
import time
import pandas as pd
import csv
import signal
import time
import requests
from bs4 import BeautifulSoup
import random



class Timeout(Exception):  
    pass

def handler(sig, frame):
    raise Timeout



def gatherData(backEndTesting, TrainingModel): # TrainingModel is a bool. 
    signal.signal(signal.SIGALRM, handler) 
    signal.alarm(30)  #if instagram has issue then after 30 seconds move on and ignore it
    try:
        ia1.refreshPosts() # need to refresh the post file to check for new posts as the two insta functions dont do this themselves. 
        likes = ia1.readLikes()
        comments = ia1.commentReading()
    except Timeout:
        likes = 0
        comments = 0

    if backEndTesting:
        userInput = int(input("Enter a value 0-10"))
        while type(userInput) != int:
            userInput = input("Enter a value 0-10")
    else:
        if TrainingModel:
            userInput = 0 #open dropbox file and extract userInput
        else:
            userInput = 0

    newRow = {"TIME": time.time() ,"INSTAGRAM_l": likes, "INSTAGRAM_c": comments, "SPOTIFY_v": sam2.spotifyReadFull(), "VOICE_e": er2.predictValue("audio2.wav")[0], "USER_i": userInput } 
    headers = ["TIME","INSTAGRAM_l","INSTAGRAM_c","SPOTIFY_v","VOICE_e", "USER_i"]
    file = open('trainingData.csv', 'a') 
    writer = csv.DictWriter(file, headers)
    writer.writerow(newRow)
    file.close()



def interpretData(likesWeight = 1, commentsWeight = 1, spotifyWeight = 1, voiceWeight = 1): 
    file = open('trainingData.csv', 'r') 
    reader = csv.reader(file)
    rows = []
    for row in reader:
        rows.append(row)
    mood = float(rows[-1][1]*likesWeight) + float(rows[-1][2]*commentsWeight) + float(rows[-1][3]*spotifyWeight) + float(rows[-1][4]*voiceWeight)
    print(mood)
    return mood


def outputActions(mood):
    if mood >= 1:
        message = "Keep up the positivity!"
        return message

    elif mood >= -1 and mood < 1:
        sam2.HappyPlayslistFull()
        message = "We have made you a playlist! Listen to it whilst doing something you enjoy"
        return message 

    elif mood <  -1:
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
