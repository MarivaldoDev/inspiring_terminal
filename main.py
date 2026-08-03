import requests
from pprint import pprint
from random import randint
import asyncio
from tradutor import translate_text

choice = randint(0, 50)

url = "https://zenquotes.io/api/quotes/&keyword=inspiration"

response = requests.get(url)
json = response.json()

sentence = json[choice]["q"]


print(asyncio.run(translate_text(sentence)))