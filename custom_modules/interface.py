import speech_recognition
import threading
import pyttsx3
import pygame

class Display:
    def __init__(self, window_size=(800, 600), fps=60):
        pygame.init()
        pygame.font.init()
        self.__window_size = window_size
        self.__fps = 60
        self.__screen = pygame.display.set_mode(window_size)
        self.__clock = pygame.time.Clock()
        self.running = False
        self.__display_thread = None
        self.__text = []
        self.__font = pygame.font.SysFont('Helvetica', 25)
        self.__max_line_length = 64

    def add_text(self, text, color=(255, 255, 255), align="left"):
        while len(text) > 0:
            ind = 128 if len(text) < self.__max_line_length else self.__max_line_length - text[:self.__max_line_length][::-1].index(' ')
            text_piece = text[:ind]
            text = text[ind:]
            self.__text.append((text_piece, color, align))
        
    def start(self):
        self.running = True
        self.__run()

    def __run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.__screen.fill((0, 0, 0))
            for y, (text, color, align) in enumerate(self.__text[::-1][:20], 1):
                font_object = self.__font.render(text, False, color)
                pos = list(font_object.get_rect(center=(self.__window_size[0]/2, self.__window_size[1]-30-(y*30))))[:2]
                if align == "left":
                    pos[0] = 30 
                self.__screen.blit(font_object, pos)
            pygame.display.flip()
            self.__clock.tick(self.__fps)
        pygame.font.quit()
        pygame.quit()

class Speaker:
    def __init__(self):
        self.__engine = pyttsx3.init()
        self.__engine.setProperty('voice', self.__engine.getProperty('voices')[1].id)

    def say(self, text):
        self.__engine.say(text)
        self.__engine.runAndWait()

class Microphone:
    def __init__(self, wakeword=None):
        self.__recognizer = speech_recognition.Recognizer()
        self.__mic = speech_recognition.Microphone()
        self.__recognizer.energy_threshold = 700
        self.__recognizer.dynamic_energy_threshold = True
        self.wakeword = wakeword

    def listen(self, timeout=10):
        result = None
        try:
            with self.__mic as source:
                self.__recognizer.adjust_for_ambient_noise(source)
                audio = self.__recognizer.listen(source, timeout=timeout)
            transcribed_text = self.__recognizer.recognize_google(audio).lower()
            if self.wakeword is None or self.wakeword.lower() in transcribed_text:
                result = transcribed_text
        except Exception as MicrophoneFailedException:
            print(MicrophoneFailedException)
        return result
