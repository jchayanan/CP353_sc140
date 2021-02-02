from flask import Flask, request, render_template
from urllib.parse import quote
from urllib.request import urlopen
import json
import requests
app = Flask(__name__)

OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&APPID={1}"
OPEN_WEATHER_KEY = '95e98d182d8f7bf6089915c05cce6d97'
OPEN_WEATHER_ICON = "http://openweathermap.org/img/wn/{0}@2x.png"

NEWS_API_URL = 'https://newsapi.org/v2/everything?q={0}&apiKey={1}'

NEWS_API_KEY = '6e2243e2abf5413785e2f93ef4a38707'

@app.route("/")
def home():
    city = request.args.get('city')
    if not city:
        city = 'bangkok'
    weather = get_weather(city, OPEN_WEATHER_KEY)
    news = 'covid'
    news = get_news(news, NEWS_API_KEY)
    return render_template("home.html", weather=weather, news=news)

def get_weather(city,API_KEY):
    try:
        query = quote(city)
        url = OPEN_WEATHER_URL.format(query, API_KEY)
        data = urlopen(url).read()
        parsed = json.loads(data)
        weather = None
        
        if parsed.get('weather'):
            description = parsed['weather'][0]['description']
            temperature = parsed['main']['temp']
            city = parsed['name']
            country = parsed['sys']['country']
            pressure = parsed['main']['pressure']
            humidity = parsed['main']['humidity']
            wind = parsed['wind']['speed']
            icon = parsed['weather'][0]['icon']
            weather = {'description': description,
                    'temperature': temperature,
                    'city': city,
                    'country': country,
                    'pressure': pressure,
                    'humidity': humidity,
                    'wind': wind,
                    'icon': icon
                    }
    except:
        weather = {'description': "city not found"}
    return weather

def get_news(news,API_KEY):
    try:
        query = quote(news)
        url = NEWS_API_URL.format(query, API_KEY)
        data = urlopen(url).read()
        parsed = json.loads(data)
        news = None

        if parsed.get('articles'):
            countNews = len(parsed['articles'])

            titleList = []
            descriptionList = []
            urlList = []
            urlToImageList = []

            for i in range(countNews):
                title = parsed['articles'][i]['title']
                titleList.append(title)

                description = parsed['articles'][i]['description']
                descriptionList.append(description)

                url = parsed['articles'][i]['url']
                urlList.append(url)

                urlToImage = parsed['articles'][i]['urlToImage']
                urlToImageList.append(urlToImage)

            news = {'countNews': countNews,
                    'titleList': titleList,
                    'descriptionList': descriptionList,
                    'urlList': urlList,
                    'urlToImageList': urlToImageList,
                    }
        return news
    except:
        news = None
        return news

@app.route("/news")
def news():
    news = request.args.get('news')
    if not news:
        news = 'covid'
    
    news = get_news(news, NEWS_API_KEY)
    return render_template('news.html', news=news)

@app.route("/about")
def about():
    city = request.args.get('city')
    if not city:
        city = 'bangkok'
    weather = get_weather(city, OPEN_WEATHER_KEY)
    return render_template('about.html', weather=weather)

@app.route("/test")
def func():
    return render_template('test.html')



if __name__ == "__main__":
    app.run(debug=True)