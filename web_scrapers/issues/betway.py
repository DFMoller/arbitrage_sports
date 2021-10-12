from bs4 import BeautifulSoup
import requests
import datetime


current_url = "https://betway.com/en/sports"
html_text = requests.get(current_url).text
soup = BeautifulSoup(html_text, 'lxml')
print(soup)