from .converter import convert_temperature
from googlesearch import search
import wikipediaapi as wiki_api
import requests

class SearchEngine:
    def __init__(self, converter=None, weather_api_key='a41fe6548df14647984ca9e3c0bbc4bf'):
        self.__weather_api_key = weather_api_key
        self.__wikipedia = wiki_api.Wikipedia('en')

    def weather(self, city, unit='celcius'):
        url = "http://api.openweathermap.org/data/2.5/weather?appid={}&q={}".format(self.__weather_api_key, city)
        response = requests.get(url).json()
        if response["cod"] != "404":
            data = response["main"]
            temp = convert_temperature(data["temp"], 'k', unit)
            low = convert_temperature(data["temp_min"], 'k', unit)
            high = convert_temperature(data["temp_max"], 'k', unit)
            humidity = data["humidity"]
            desc = response["weather"][0]["description"]
            weather = "It is currently {0} degrees {3} in {4}. Today's forecast predicts a high of {1} degrees {3} and a low of {2} degrees {3}.You can expect {5} with a humidity of {6}%".format(temp, high, low, unit, city, desc, humidity)
            return weather
        else:
            return 'Unable to get weather for {}'.format(city.capitalize())

    def song_data(self, song_name=None, max_limit=3):
        if song_name is not None:
            try:
                search_url = 'https://search.azlyrics.com/search.php?q={}'.format('+'.join(song_name.split(' '))).lower()
                unscraped_text = requests.get(search_url).text
                raw_text = unscraped_text[unscraped_text.index('<div class=\"panel-heading\"><b>Song results:</b><br><small>'):]
                search_results = []
                for ind in range(1, max_limit+1):
                    if str(ind) in raw_text:
                        url_start = '{}. <a href="'.format(str(ind))
                        url_end = '" target="_blank">' 
                        lyrics_url = raw_text[raw_text.index(url_start)+len(url_start):raw_text.index(url_end)]
                        filtered_text = raw_text[raw_text.index(url_end)+len(url_end):]
                        song_name = filtered_text[filtered_text.index('<b>')+3:filtered_text.index('</b></a>')]
                        artist_name = filtered_text[filtered_text.index('by <b>')+6:filtered_text.index('by <b>')+6+filtered_text[filtered_text.index('by <b>')+6:].index('</b>')]
                        raw_text = raw_text[raw_text.index('</td></tr>')+10:]
                        search_results.append({
                            "name": song_name,
                            "artist": artist_name.split(', ')[0],
                            "url": lyrics_url
                            })
                    else:
                        break
            except Exception as LyricGetterException:
                print(LyricGetterException)
            if len(search_results) > 0:
                song_data = search_results[0]
                unscraped_text = requests.get(song_data["url"]).text
                raw_start_text = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
                raw_end_text = '</div>'
                lyrics_raw = unscraped_text[unscraped_text.index(raw_start_text)+len(raw_start_text):unscraped_text.index(raw_start_text)+len(raw_start_text)+unscraped_text[unscraped_text.index(raw_start_text)+len(raw_start_text):].index(raw_end_text)]
                lyrics_data = [text.strip('\n').strip('\r').replace('&quot;', '"') for text in lyrics_raw.split('<br>')]
                song_data["lyrics"] = lyrics_data
            else:
                song_data = None
                print("No Results Found!")
        return song_data

    def wiki_search(self, query):
        page = self.__wikipedia.page(query.lower().strip())
        if page.exists():
            return page.summary.split('\n')[0]
        else:
            return None

    def google_search(self, query, limit=3):
        results = list(search(query, tld="co.in", num=limit, stop=1, pause=2))
        if len(results) > 0:
            return "This might help: {}".format(results[0])
        else:
            return None

    def combined_search(self, query):
        result = None
        parts = query.lower().split()
        align = "left"
        formatting = "string"
        if "weather" in parts:
            if "in" in parts:
                loc = parts[parts.index("in")+1]
            else:
                loc = "bangalore"
            result = self.weather(loc)
        elif "lyrics" in parts:
            try:
                song_name = " ".join(parts[parts.index("of")+1:])
                raw_res = self.song_data(song_name)
                if raw_res is not None:
                    result = raw_res["lyrics"]
                    formatting = "list"
                    align = "center"
            except IndexError:
                pass
        elif "is" in parts:
            try:
                query = " ".join(parts[parts.index("is")+1:])
            except IndexError:
                pass
        if result is None:
            result = self.wiki_search(query)
            if result is None:
                result = self.google_search(query, 1)
        return result, formatting, align