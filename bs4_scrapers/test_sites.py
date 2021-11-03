import requests
from bs4 import BeautifulSoup
from headers import get_random_headers
# from collections import OrderedDict

url = "https://sports.tipico.de/en"
headers = get_random_headers()
# print(headers)
html_text = requests.get(url, headers=headers).text
soup = BeautifulSoup(html_text, 'lxml')
with open('bs4_scrapers/test_sites.html', "w", encoding="utf-8") as html_file:
    html_file.write(str(soup))
    # html_file.write(str(soup.encode("utf-8")))

# tiles = soup.find_all("div", class_="grid-event-wrapper")
# print(len(tiles))
