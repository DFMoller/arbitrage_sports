from bs4 import BeautifulSoup
import requests
import datetime

# It is confirmed that betUS works with webscraping


current_url = "https://www.betus.com.pa/sportsbook/tennis/challenger-alicante/"
html_text = requests.get(current_url).text
soup = BeautifulSoup(html_text, 'lxml')
# print(soup)
# search_results = soup.find_all('div', class_='e-available m-has-photos')
# page_numbers = soup.find('div', class_='b-pagination-bar').find('div', class_='gm-show-inline-block').findChildren()
# pages = int(page_numbers[-1].text) # finds last item in list
tiles = soup.find_all('div', class_='normal')
for tile in tiles:
    time = tile.find('span', class_='time').span.text
    print(time)
# print(soup)