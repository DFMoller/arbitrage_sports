from bs4 import BeautifulSoup
import requests
import datetime


current_url = "https://sports.sportingbet.com/en/sports"
html_text = requests.get(current_url).text
soup = BeautifulSoup(html_text, 'lxml')
print(soup)
# search_results = soup.find_all('div', class_='e-available m-has-photos')
# page_numbers = soup.find('div', class_='b-pagination-bar').find('div', class_='gm-show-inline-block').findChildren()
# pages = int(page_numbers[-1].text) # finds last item in list