import speech_recognition
import pyttsx3

class Speaker:
    def __init__(self):
        self.__engine = pyttsx3.init()

    def say(self, text):
        self.__engine.say(text)
        self.__engine.runAndWait()

class Microphone:
    def __init__(self, wakeword=None):
        self.__recognizer = speech_recognition.Recognizer()
        self.__mic = speech_recognition.Microphone()
        self.__recognizer.energy_threshold = 3000
        self.__recognizer.dynamic_energy_threshold = True
        self.wakeword = wakeword

    def listen(self, timeout=10):
        result = None
        try:
            with self.__mic as source:
                self.__recognizer.adjust_for_ambient_noise(source)
                audio = self.__recognizer.listen(source, timeout=timeout)
                transcribed_text = self.__recognizer.recognize_whisper(audio).lower()
                if self.wakeword is None or self.wakeword.lower() in transcribed_text:
                    result = transcribed_text
        except Exception as MicrophoneFailedException:
            print(MicrophoneFailedException)
        return result
