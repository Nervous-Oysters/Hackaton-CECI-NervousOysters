#import speech_recognition as sr
#from pynput import mouse, keyboard
from vosk import Model, KaldiRecognizer
import pyaudio

#keyboard_controller = keyboard.Controller()
#mouse_controller = mouse.Controller()

model = Model('vosk-model-small-fr-0.22')
recognize = KaldiRecognizer(model, 16000)
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

while True:
    data=stream.read(4096)
    #if len(data) == 0:
     #   break

    if recognize.AcceptWaveform(data):
        print(recognize.Result())