from custom_modules import interface
from custom_modules import chatbot
import threading
import time

WAKEWORD = None
ai = chatbot.ChatBot()
microphone = interface.Microphone(WAKEWORD)
speaker = interface.Speaker()

def main():
    while True:
        query = microphone.listen(3).strip()
        if query is not None and len(query) > 0:
            if query.lower() == "stop":
                break
            print(f"USER: {query}\n")
            result = ai.ask(query)
            print(f"AI: {result}\n")
            speaker.say(result)

if __name__ == '__main__':
    main()