from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.animation import Animation
import audioRecording as ar1
import RecordingData as rd1
import notify2
import settingsTool as st1


class MainWindow(Screen):

    def buttonCall(self):

            # Recording Audio
            time = int(self.slide_number.text)
            print(time)
            ar1.recordAudio(time)

            # Gathering data from Instagram, Spotify etc and interpreting 
            rd1.gatherData(False, False)
            mood = rd1.interpretData()

            # Notifications and Actions based on user's mood
            message = rd1.outputActions(mood)
            notify2.init("Emotion Output")
            notification = notify2.Notification(summary = "Mood Reader", message =  message)
            notification.set_urgency(notify2.URGENCY_NORMAL)
            notification.set_timeout(2000)
            notification.show()

    def getSliderValue(self, *args):
        self.slide_number.text = str(args[1])
    pass

class SecondWindow(Screen):

    def likesSliderValue(self, *args):
        self.likes_number.text = str(args[1])

    def commentsSliderValue(self, *args):
        self.comments_number.text = str(args[1])

    def spotifySliderValue(self, *args):
        self.spotify_number.text = str(args[1])

    def voiceSliderValue(self, *args):
        self.voice_number.text = str(args[1])

    def settingsSave(self):
        st1.writeSetting(likesWeight = float(self.likes_number.text), commentsWeight = float(self.comments_number.text), spotifyWeight = float(self.spotify_number.text), voiceWeight = float(self.voice_number.text))

    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("appKivy.kv")


class voiceApplication(App):

    def build(self):
        return kv
    
    



if __name__ == "__main__":
    voiceApplication().run()