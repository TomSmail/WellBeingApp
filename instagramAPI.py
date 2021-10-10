from re import T
from instabot import Bot
from os import remove
import instaloader
from passwordEncoding import remoteDecryption, getDetailsFromFile
import csv
from csv import DictWriter
import datetime
import pandas as pd
import time
import text2emotion as emotion



def setupCheckCookies():
    try:
        remove("config/tomsmailspythonbot_uuid_and_cookie.json")
    except:
        print("Cookie does not exist, continuing with prorgramn.")
    bot = Bot()
    bot.login(username= getDetailsFromFile()[0], password = remoteDecryption()) # This gets the username and password from a file from another script
    return bot    



def getPostLikes(bot):
    media = bot.get_your_medias(as_dict=False)
    print (media)
    posts = []
    choice = input("Do you want the list of like users? y/n :")
    for i in range(len(media)):
        likeUserIDs = bot.get_media_likers(media[i])
        comments = bot.get_media_comments(media[i], only_text = True)
        now = bot.get_your_medias(as_dict=True)[i]["taken_at"]
        print("This is the number of likes", likeUserIDs)
        if choice == "y":
            for j in range(len(likeUserIDs)):
                print("These people liked your post:", bot.get_username_from_user_id(likeUserIDs[j]))
        print("Post number", i + 1, "has", len(likeUserIDs), "likes.")
        posts.append({"ID": media[i], "TIME": now, "LIKE_COUNT": len(likeUserIDs),"COMMENTS": comments})#["Post", i] = len(likeUserIDs)
    print(posts)
    return posts



"""def writeNewPostToCSV(posts): # THIS FUNCTION IS NOT CURRENTLY IN USE
    file = open('postFile.csv', 'w')
    originalFile = open('postFile.csv', "r")
    reader = csv.reader(originalFile)
    writer = csv.writer(file)
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    fieldNames = ["ID", "TIME", "LIKE_COUNT", "COMMENTS"]
    newposts = []
    with open ('postFile.csv', "r") as fileObject:
        f = fileObject.read()
        for post in posts:
            if post["ID"] not in f:
                newposts.append(post)
    print(newposts)"""
"""dictWriter = DictWriter(fileObject, fieldnames = fieldNames)
if posts[row][0] not in originalFile: #or (posts[0] in file and posts[1] < yesterday):
    dictWriter.writerow(posts[row])
else:
    print("error")"""

def writeNewPostToCSV(posts):
    df = pd.read_csv("postFile.csv")
    print(df)
    newposts = []
    listOfID = df.ID.to_list()
    for i in range(len(posts)):
        if posts[i]["TIME"] >= time.time() - 86400 and posts[i]["ID"] not in listOfID: # checks to see if a post is more than a day old and not in the dataframe already
            newposts.append(posts[i])
    print("newpost", newposts)
    df.append(newposts)
    df.to_csv("postFile.csv")
    return newposts



def commentReading():
    df = pd.read_csv("postFile.csv")
    listOfComments = df.COMMENTS.to_list()
    print(listOfComments)
    commentsForReading = []
    totalEmotion = 0
    for row in range(len(df.index)):
        print(df["TIME"][row])
        print(time.time() +172800)
        if time.time() - 172800 <= df["TIME"][row]: # if a post is less that 2 days old add the comments to a list (commentsForReading)
            commentsForReading.append(listOfComments[row])
    print(commentsForReading)
    for comment in range(len(commentsForReading)):
        commentEmotion = emotion.get_emotion(commentsForReading[comment])
        print("emotion", commentEmotion)
        totalEmotion = totalEmotion + commentEmotion["Happy"] + commentEmotion["Surprise"] - commentEmotion["Angry"] - commentEmotion["Fear"] - commentEmotion["Sad"]
    print(totalEmotion)
    return totalEmotion #if a post is more than a day old but less that 2 days old then we want to look at its comments



def likesReading():
    df1 = pd.read_csv("postFile.csv")
    df2 = pd.read_csv("newPostFile.csv")
    listOfLikes = df1.LIKES.to_list()
    averageLikes = (sum(listOfLikes)/ len(listOfLikes))
    likesEmotion = 0
    for i in range(len(df1)):
        if df1[i]["TIME"] <= time.time() - 86400: # checks to see if a post is more than a day old and not in the dataframe already
            likes = df1[i]["LIKE_COUNT"]
            likesEmotion = likesEmotion + (likes - averageLikes)
    return likesEmotion


def refreshPosts():
    bot = setupCheckCookies()
    posts = getPostLikes(bot)
    writeNewPostToCSV(posts)



def main():
    bot = setupCheckCookies()
    posts = getPostLikes(bot)
    writeNewPostToCSV(posts)

if __name__ == '__main__':
    print("----Running Programn----")
    main()


    