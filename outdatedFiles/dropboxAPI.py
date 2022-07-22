import dropbox
import EmotionRecognition as er
db = dropbox.Dropbox('SECRET')
appSecret = ""
appKey = ""

def pullVoiceRecording():
    for file in db.files_list_folder('').entries:
        if "voiceRecording" in file.name:
            er.encodeResults(file)
            print("results have been encoded")
            #need to be able to append encoded results onto a file in table
            db.files_delete(file)

        else:
            print("Voice Recording Not Found!")

def updateSettingsFolder():
    for file in db.files_list_folder("").entries:
        if "SettingsFile" in file.name:
            dbx.files_download_to_file("SettingsFile", file, rev)
