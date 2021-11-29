import SpotifyAPIMood2 as sam2
import instagramAPI as ia1
import EmotionRecognition as er1
import time
import pandas as pd
import csv

def gatherData(backEndTesting, TrainingModel)): # TrainingModel is a bool. 
    ia1.refreshPosts() # need to refresh the post file to check for new posts as the two insta functions dont do this themselves. 
    if backEndTesting:
        userInput = input("Enter a value 0-10")
        try:
            userInput = float(userInput)
        except:
            gatherData(True)
    else:
        if TrainingModel:
            userInput = # take user input from file from front end. 
        else:
            userInput = "Strip this value when traing ML model"

    newRow = {"TIME": time.time() ,"INSTAGRAM_l": ia1.readLikes(), "INSTAGRAM_c": ia1.commentReading(), "SPOTIFY_v": sam2.spotifyReadFull(), "VOICE_e": er1., "USER_i": userInput }
    headers = ["TIME","INSTAGRAM_l","INSTAGRAM_c","SPOTIFY_v","VOICE_e", "USER_i"]
    file = open('trainingData.csv', 'w')
    writer = csv.DictWriter(file, headers)
    writer.writerow(newRow)
    file.close()

            
def main():
    gatherData()


if __name__ == '__main__':
    print("Running Programn")
    main()


# I want to be able to ask for how a user is feeling then insert this value along with the values from the different APIs into a new row of a CSV file. It should take the time taken for the test to be run as its primary key
# This is in hopes of creating a database that I can train a Machine learning model on

# needs to gather data from all the different csv files and store as a list with a time stamp as the index  then take this list of values and append it to the end of a csv as a new row. 
