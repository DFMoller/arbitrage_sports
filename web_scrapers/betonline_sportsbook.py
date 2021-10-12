from bs4 import BeautifulSoup
import requests
import datetime


current_url = "https://sports.intertops.eu/en/Bets/Tennis/26"
html_text = requests.get(current_url).text
soup = BeautifulSoup(html_text, 'lxml')
# print(soup)
# search_results = soup.find_all('div', class_='e-available m-has-photos')
# page_numbers = soup.find('div', class_='b-pagination-bar').find('div', class_='gm-show-inline-block').findChildren()
# pages = int(page_numbers[-1].text) # finds last item in list
tiles = soup.find('ul', class_='tab nextbets active').find_all("li")
for tile in tiles:
    # time = tile.find('span', class_='time').span.text
    title_anchor = tile.find('a', class_='cl-e cl-ttl')
    title = title_anchor.text.strip()
    link = "https://sports.intertops.eu" + title_anchor.get('href')
    print(title, link)
# print(soup)