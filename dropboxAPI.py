import dropbox
import EmotionRecognition as er
db = dropbox.Dropbox('-9EY8VU6xfEAAAAAAAAAAd-AyKKqeEYy4jY7PV426PMBzFQeR9_f1RPbw5ju_O28')
appSecret = "rnt2zq33akm0iiy"
appKey = "gl99chamr35370o"

def pullVoiceRecording():
    for file in db.files_list_folder('').entries:
        if "voiceRecording" in file.name:
            er.encodeResults(file)
            print("results have been encoded")
            db.files_delete(file)

        else:
            print("Voice Recording Not Found!")

def updateSettingsFolder():
    for file in db.files_list_folder("").entries:
        if "SettingsFile" in file.name:
            dbx.files_download_to_file("SettingsFile", file, rev)
