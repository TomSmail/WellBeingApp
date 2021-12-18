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
    for i in range(len(media)):
        likeUserIDs = bot.get_media_likers(media[i])
        comments = bot.get_media_comments(media[i], only_text = True)
        now = bot.get_your_medias(as_dict=True)[i]["taken_at"]
        print("This is the number of likes", likeUserIDs)
        print("Post number", i + 1, "has", len(likeUserIDs), "likes.")
        posts.append({"ID": media[i], "TIME": now, "LIKE_COUNT": len(likeUserIDs),"COMMENTS": comments})#["Post", i] = len(likeUserIDs)
    print(posts)
    return posts



def writeNewPostToCSV(posts):
    df = pd.read_csv("Code/postFile.csv")
    print(df)
    newposts = []
    listOfID = df.ID.to_list()
    for i in range(len(posts)):
        if posts[i]["TIME"] >= time.time() - 86400 and posts[i]["ID"] not in listOfID: # checks to see if a post is more than a day old and not in the dataframe already
            newposts.append(posts[i])
    print("newpost", newposts)
    with open("postFile.csv", 'w', newline='') as write:
        fieldNames = ["ID", "TIME", "LIKE_COUNT", "COMMENTS"]
        rowWriter = DictWriter(write, fieldNames)
        rowWriter.writeheader()
        for i in range(len(newposts)):
            rowWriter.writerow(newposts[i])
    return newposts




def commentReading():
    df = pd.read_csv("Code/postFile.csv")
    listOfComments = df.COMMENTS.to_list()
    print(listOfComments)
    commentsForReading = []
    totalEmotion = 0
    for row in range(len(df.index)):
        if time.time() - 172800 <= df["TIME"][row]: # if a post is less that 2 days old add the comments to a list (commentsForReading)
            commentsForReading.append(listOfComments[row])
        else:
            totalEmotion = 0
    print(commentsForReading)
    for comment in range(len(commentsForReading)):
        commentEmotion = emotion.get_emotion(commentsForReading[comment])
        print("emotion", commentEmotion)
        totalEmotion = totalEmotion + commentEmotion["Happy"] + commentEmotion["Surprise"] - commentEmotion["Angry"] - commentEmotion["Fear"] - commentEmotion["Sad"]
    return totalEmotion #if a post is more than a day old but less that 2 days old then we want to look at its comments



def likesReading(posts):
    df1 = pd.read_csv("Code/postFile.csv")
    allPostLikes = []
    for i, post in enumerate(posts):
        allPostLikes.append(post["LIKE_COUNT"])
    newLikes = df1.LIKE_COUNT.to_list()
    likesEmotion = 0
    if sum(newLikes) == 0 or sum(allPostLikes) == 0:
        return likesEmotion
    else:
        averageNewLikes = (sum(newLikes)/ len(newLikes))
        averageAllLikes = (sum(allPostLikes)/ len(allPostLikes))
        likesEmotion = (averageNewLikes - averageAllLikes)
    return likesEmotion


def refreshPosts():
    bot = setupCheckCookies()
    posts = getPostLikes(bot)
    writeNewPostToCSV(posts)

def readLikes():
    bot = setupCheckCookies()
    posts = getPostLikes(bot)
    return likesReading(posts)
    


def main():
    bot = setupCheckCookies()
    posts = getPostLikes(bot)
    writeNewPostToCSV(posts)
    print(commentReading())
    print(likesReading(posts))


if __name__ == '__main__':
    print("----Running Programn----")
    main()


    