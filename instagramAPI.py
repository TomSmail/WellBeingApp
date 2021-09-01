from instabot import Bot
from os import remove
import instaloader
from passwordEncoding import remoteDecryption, getDetailsFromFile
import csv
from csv import DictWriter
import datetime
import pandas as pd



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
    print (dictionary["taken_at"])
    posts = []
    choice = input("Do you want the list of like users? y/n :")
    for i in range(4):
        likeUserIDs = bot.get_media_likers(media[i])
        comments = bot.get_media_comments(media[i], only_text = True)
        now = bot.get_your_medias(as_dict=True)
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
    post1 = posts[0]
    print("post1", post1)
    #for post in posts:
    print("post1 ID", post1["ID"])
    listOfID = df.ID.to_list()
    print("df ID", df.ID)
    print("df list ID", listOfID)
    for i in range(len(posts)):
        if posts[i]["ID"] not in listOfID:
            newposts.append(posts[i])
    print("newpost", newposts)
    df.append(newposts)
    df2 = pd.DataFrame(posts)
    print(df2)
    df2.to_csv("postFile.csv")
    #for post in df:
        #if post[1] not in df.ID:

            
    
            
    

 
def main():
    bot = setupCheckCookies()
    posts = getPostLikes(bot)
    CSVTEST(posts)

if __name__ == '__main__':
    print("----Running Programn----")
    main()


    