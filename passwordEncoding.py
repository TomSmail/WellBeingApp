from instabot import Bot
import random
from cryptography.fernet import Fernet



def getUsernameAndPassword():
    clientInfo  = {"username": "", "password": ""}
    clientInfo["username"] = input("Please input your username: ")
    clientInfo["password"] = input("Please input your password: ")
    return clientInfo



def checkUserExists(clientInfo):
    try:
        bot = Bot()
        bot.login(username= clientInfo["username"], password = clientInfo["password"])
    except: 
        print("This username and password do not match, please try again")
        getUsernameAndPassword()



def passwordEncryption(clientInfo):
    key = Fernet.generate_key()
    keyfile = open("Code/passwordKey.key", "wb")
    keyfile.write(key)
    keyfile.close()
    encodedPassword = clientInfo["password"].encode()
    tool = Fernet(key)
    encryptedPassword = tool.encrypt(encodedPassword)
    return encryptedPassword



def passwordDecryption(encryptedPassword):
    keyfile = open("Code/passwordKey.key", "rb")
    key = keyfile.read()
    keyfile.close()
    tool = Fernet(key)
    decryptedPassword = tool.decrypt(encryptedPassword)
    originalPassword = decryptedPassword.decode()
    return originalPassword



def writeDetailsToFile(clientInfo, encryptedPassword):
    userFile = open("Code/userFile.txt", "w")
    userFile.write(clientInfo["username"])
    userFile.close()
    passwordFile = open("Code/passwordFile.key", "wb")
    passwordFile.write(encryptedPassword)
    passwordFile.close()



def getDetailsFromFile():
    userFile = open("Code/userFile.txt", "r")
    username = userFile.read()
    userFile.close()
    passwordFile = open("Code/passwordFile.key", "rb")
    encryptedPassword = passwordFile.read()
    passwordFile.close()
    return username, encryptedPassword



def remoteDecryption():
    encryptedPassword = getDetailsFromFile()[1]
    originalPassword = passwordDecryption(encryptedPassword)
    return originalPassword



def main():
    clientInfo = getUsernameAndPassword()
    checkUserExists(clientInfo)
    encryptedPassword = passwordEncryption(clientInfo)
    writeDetailsToFile(clientInfo, encryptedPassword)
    passwordDecryption(encryptedPassword)



if __name__ == '__main__':
    print("Running Programn")
    main()
    





