import pyaudio
import wave

def recordAudio(time = 300):

    # Initialise the audio recorder
    audio = pyaudio.PyAudio()
    time = time * 21.4285714286 # value to convert real time into "> x" value
    stream = audio.open(format=pyaudio.paInt16, channels = 1, rate = 22050, input = True, frames_per_buffer=1024)
    frames = []

    # Create a list of chunks of sound data
    x = 0
    while x <= time:
        data = stream.read(1024)
        frames.append(data)
        x +=1

    # Terminate the audio recorder session
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the file and join chunks
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