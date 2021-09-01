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
    dictionary = bot.get_your_medias(as_dict=True)
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



def writeNewPostToCSV(posts):
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
    print(newposts)
"""dictWriter = DictWriter(fileObject, fieldnames = fieldNames)
if posts[row][0] not in originalFile: #or (posts[0] in file and posts[1] < yesterday):
    dictWriter.writerow(posts[row])
else:
    print("error")"""

def CSVTEST(posts):
    df = pd.read_csv("postFile.csv")
    print(df)
    newposts = []
    listOfID = df.ID.to_list()
    for i in range(len(posts)):
        if posts[i]["TIME"] >= time.time() + 86400 and posts[i]["ID"] not in listOfID: # checks to see if a post is more than a day old and not in the dataframe already
            newposts.append(posts[i])
    print("newpost", newposts)
    df.append(newposts)
    df2 = pd.DataFrame(posts)
    print(df2)
    df2.to_csv("postFile.csv")
    return newposts

def commentReading():
    df = pd.read_csv("postFile.csv")
    listOfComments = df.COMMENTS.to_list()
    print(listOfComments)
    commentsForReading = []
    for row in range(len(df.index)):
        print(df["TIME"][row])
        print(time.time() +172800)
        if time.time() - 172800 <= df["TIME"][row]: # if a post is less that 2 days old add the comments to a list (commentsForReading)
            commentsForReading.append(listOfComments[row])
    print(commentsForReading)
    for comment in range(len(commentsForReading)):
        print(emotion.get_emotion(commentsForReading[comment]))
    #if a post is more than a day old but less that 2 days old then we want to look at its comments


            
    
            
    

 
def main():
    bot = setupCheckCookies()
    posts = getPostLikes(bot)
    CSVTEST(posts)
    commentReading()

if __name__ == '__main__':
    print("----Running Programn----")
    main()


    