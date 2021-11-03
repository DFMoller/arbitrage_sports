from bs4 import BeautifulSoup
import requests
import datetime


current_url = "https://www.sunbet.co.za/#filter/football/england/premier_league"
html_text = requests.get(current_url).text
soup = BeautifulSoup(html_text, 'lxml')
# print(soup)
# search_results = soup.find_all('div', class_='e-available m-has-photos')
# page_numbers = soup.find('div', class_='b-pagination-bar').find('div', class_='gm-show-inline-block').findChildren()
# pages = int(page_numbers[-1].text) # finds last item in list
tiles = soup.find_all('li', class_='KambiBC-event-item')
# for tile in tiles:
#     teams = tile.find('div', class_='KambiBC-event-participants').text
#     print(teams)

print(len(tiles))

print(soup)