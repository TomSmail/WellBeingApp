"""import pyaudio
import wave

audio = pyaudio.PyAudio()

stream = audio.open(format=pyaudio.paInt16, channels = 1, rate = 44100, input = True, frames_per_buffer=1024)
frames = []
try:
    while True:
        data = stream.read(1024)
        frames.append(data)
except KeyboardInterrupt:
    pass 
stream.stop_stream()
stream.close()
audio.terminate()

sound_file = wave.open("audio2.wav", "wb")
sound_file.setnchannels(1)
sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
sound_file.setframerate(44100)
sound_file.writeframes(b"".join(frames))
sound_file.close()"""

import pyaudio
import wave

def recordAudio(time = 300):
    audio = pyaudio.PyAudio()
    time = time * 21.4285714286 # value to convert real time into "> x" value
    stream = audio.open(format=pyaudio.paInt16, channels = 1, rate = 22050, input = True, frames_per_buffer=1024)
    frames = []
    x = 0
    while x <= time:
        data = stream.read(1024)
        frames.append(data)
        x +=1
    stream.stop_stream()
    stream.close()
    audio.terminate()

    sound_file = wave.open("audio2.wav", "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(22050)
    sound_file.writeframes(b"".join(frames))
    sound_file.close()


def main():
    userTime = int(input("Enter the number of seconds you wish to speak for:"))
    recordAudio(userTime)

if __name__ == "__main__":
    main()