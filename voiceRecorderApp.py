from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.animation import Animation
import audioRecording as ar1
import RecordingData as rd1


class voiceRecorder(App):

    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.8, 0.8)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.window.add_widget(Image(source = "logo.png"))

        self.slider = Slider(value = 35, min = 10, max = 60, step = 5, padding = 32, cursor_size = [30, 30], cursor_image = "dot.png")
        self.window.add_widget(Label(text = "How long would you like to talk for?", font_size = 20, color  = "FFFFFF", font_name = "comic"))
        self.window.add_widget(self.slider)

        self.button = Button(text="Talk!", font_size = 25, color  = "FFFFFF", font_name = "comic", size_hint = (.5,.4), background_color = "00801A", background_normal = "")
        self.button.bind(on_press = self.buttonCall)
        self.window.add_widget(self.button)

        return self.window

    def buttonCall(self, instance):
        self.button.text = "Finished! (" + str(self.slider.value) + " seconds)"
        ar1.recordAudio(self.slider.value)
        rd1.gatherData(False, False)
        rd1.interpretData()

        

if __name__ == "__main__":
    voiceRecorder().run()