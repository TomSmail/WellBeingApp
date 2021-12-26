from instabot import Bot
from os import remove
from passwordEncoding import remoteDecryption, getDetailsFromFile
import pandas as pd
from csv import DictWriter
import time
import text2emotion as emotion




def setupCheckCookies():

    # Removes erroneous JSON file
    try:
        remove("config/tomsmailspythonbot_uuid_and_cookie.json")
    except:
        print("Cookie does not exist, continuing with prorgramn.")

    # Login to Instagram and create instance
    bot = Bot()
    bot.login(username= getDetailsFromFile()[0], password = remoteDecryption()) 
    return bot    



def getPostLikes(bot):

    # Retrieve posts from Instgram
    media = bot.get_your_medias(as_dict=False)
    print (media)
    posts = []

    # Create dictionary of likes, comments etc
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

    # Open csv file and convert to DataFrame
    df = pd.read_csv("Code/postFile.csv")
    print(df)
    newposts = []
    listOfID = df.ID.to_list()

    # Identify new posts
    for i in range(len(posts)):
        if posts[i]["ID"] not in listOfID: 
            newposts.append(posts[i])
    print("newpost", newposts)

    # Add new posts to csv
    with open("Code/postFile.csv", 'a', newline='') as write:
        fieldNames = ["ID", "TIME", "LIKE_COUNT", "COMMENTS"]
        rowWriter = DictWriter(write, fieldNames)
        for i in range(len(newposts)):
            rowWriter.writerow(newposts[i])
    return newposts



def commentReading():

    # Create list of comments from posts
    df = pd.read_csv("Code/postFile.csv")
    listOfComments = df.COMMENTS.to_list()
    print(listOfComments)
    commentsForReading = []
    totalEmotion = 0
    
    # Add new comments to list
    for row in range(len(df.index)):
        if time.time() - 172800 <= int(df["TIME"][row]): 
            commentsForReading.append(listOfComments[row])
    print(commentsForReading)

    # Extract emotions from comments 
    for comment in range(len(commentsForReading)):
        commentEmotion = emotion.get_emotion(commentsForReading[comment])
        print("emotion", commentEmotion)
        totalEmotion = totalEmotion + commentEmotion["Happy"] + commentEmotion["Surprise"] - commentEmotion["Angry"] - commentEmotion["Fear"] - commentEmotion["Sad"]
    return totalEmotion 



def likesReading():

    # Get all likes from csv
    df = pd.read_csv("Code/postFile.csv")
    allPostLikes = df.LIKE_COUNT.to_list()
    print(allPostLikes)
    
    # Identify new post likes
    newposts = []
    for row in range(len(df.index)):
        if time.time() - 172800 <= int(df["TIME"][row]):
            newposts.append(allPostLikes[row])
    print(newposts)

    # No likes return 0
    likesEmotion = 0
    if sum(newposts) == 0 or sum(allPostLikes) == 0:
        return likesEmotion
    
    # Find how much new likes deviate from old 
    else:
        averageNewLikes = (sum(newposts)/ len(newposts))
        averageAllLikes = (sum(allPostLikes)/ len(allPostLikes))
        likesEmotion = (averageNewLikes - averageAllLikes)

        # Stardises results
        if likesEmotion >= 0.2*averageAllLikes: 
            likesEmotion = 2
        elif likesEmotion >= 0.05*averageAllLikes and likesEmotion <= 0.2*averageAllLikes:
            likesEmotion = 1
        elif likesEmotion <= 0.05*averageAllLikes and likesEmotion >= -(0.05*averageAllLikes): 
            likesEmotion = 0
        elif likesEmotion <= -0.05*averageAllLikes and likesEmotion >= -(0.2*averageAllLikes):
            likesEmotion = -1
        elif likesEmotion <= -(0.2*averageAllLikes):
            likesEmotion = -2
    return likesEmotion



def instagramEmotion():

    # Initialise 
    bot = setupCheckCookies()

    # Get all posts and append
    posts = getPostLikes(bot)
    writeNewPostToCSV(posts)

    # Get outputs
    commentEmotion = commentReading()
    likesEmotion = likesReading()
    return commentEmotion, likesEmotion 


if __name__ == '__main__':
    print("----Running Programn----")
    print(commentReading())