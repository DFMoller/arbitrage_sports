from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import sys, time
sys.path.append('C:/Users/dfmol/Programming/arbitrage_betting/selenium_scrapers/inc')
# from betway_functions import get_tournament_urls

web = 'https://www.sunbet.co.za/#filter/tennis'
path = 'C:/Users/dfmol/Programming/arbitrage_betting/selenium_scrapers/chromedriver_win32/chromedriver.exe'
dt_format = '%d-%m-%Y %H:%M'
driver = webdriver.Chrome(path)

betway_pages = {
    'tennis/atp'
}

def get_tournament_links(url):
    driver.get(url)
    while True:
        time.sleep(1)
        try:
            tournament_box = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div[1]/div/div[2]/div[4]/div/div[2]/div/div/div')
            break
        except NoSuchElementException as err:
            print("Waiting...")
            pass
    tournament_rows = tournament_box.find_elements(By.CLASS_NAME, 'collapsableHeader')
    links = []
    for row in tournament_rows:
        link = row.find_element(By.CLASS_NAME, 'showAllButton').get_attribute('href')
        split_link = link.rsplit("//", 1)
        link = "/tennis/".join(split_link)
        print(link)
        links.append(link)
    return links

def main():
    links = get_tournament_links("https://sports.betway.de/en/sports/ctg/tennis")
    driver.quit()

if __name__ == "__main__":
    main()