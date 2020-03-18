from custom_modules import internet
from custom_modules import converter
from custom_modules import interface
import threading
import time

WAKEWORD = None

display = interface.Display()
microphone = interface.Microphone(WAKEWORD)
speaker = interface.Speaker()
search_engine = internet.SearchEngine()

def add_text(result, align):
    for text in result:
        display.add_text(text, (255, 255, 255), align)
        time.sleep(0.1)

def main():
    time.sleep(1)
    while display.running:
        query = microphone.listen(5)
        if query is not None:
            display.add_text(query, (0, 100, 255))
            result, formatting, align = search_engine.combined_search(query)
            if result is None:
                result, formatting, align = "I couldn't find anything for that", "string"
            if formatting is "string":
                result = [result]
            threading.Thread(target=add_text, args = (result, align,)).start()
            speaker.say(result)
            display.add_text(" ")

if __name__ == '__main__':
    main_thread = threading.Thread(target=main)
    main_thread.start()
    display.start()
    main_thread.join()