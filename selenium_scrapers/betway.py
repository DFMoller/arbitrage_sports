from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import sys, time, pprint
sys.path.append('C:/Users/dfmol/Programming/arbitrage_betting/selenium_scrapers/inc')
# from betway_functions import get_tournament_urls

tournaments_base_url = 'https://sports.betway.de/en/sports/ctg/tennis'
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
    anchor_tags = tournament_box.find_elements(By.CLASS_NAME, 'showAllButton')
    links = {}
    for tag in anchor_tags:
        link = tag.get_attribute('href')
        split_link = link.rsplit("//", 1)
        tournament_name = split_link[1]
        link = "/tennis/".join(split_link)
        # print(link)
        links[link] = {'tournament_name': tournament_name}
    return links

def get_location_links_per_tournament(driver, tournament_name):
    return_dict = {}
    while True:
        try:
            box = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div[1]/div/div[2]/div[4]/div/div[2]/div/div[1]/div/div')
            break
        except NoSuchElementException as err:
            print('Waiting...')
            time.sleep(1)
    links = box.find_elements(By.CLASS_NAME, 'showAllButton')
    for link in links:
        href = link.get_attribute('href').replace('///', f'/tennis/{tournament_name}/')
        # print(f'\t{href}')
        return_dict[href] = {}
    return return_dict

def create_complete_build(temp_build):
    build = {}
    for tournament_url in temp_build:
        tournament_name = temp_build[tournament_url]['tournament_name']
        # print("\n" + tournament_url)
        driver.get(tournament_url) # fetch a page for every individual tournament
        # build[tournament_url] = get_location_links_per_tournament(driver, tournament_name)
        package = get_location_links_per_tournament(driver, tournament_name)
        for ins in package:
            if 'doubles' in ins or 'outright' in ins: # filter out unwanted events
                continue
            else:
                build[ins] = {
                    'tour_name': tournament_name,
                    'matches': []
                }
    return build
            


def main():
    temp_build = get_tournament_links(tournaments_base_url) # returns a dictionary
    complete_build = create_complete_build(temp_build) # returns a refined dictionary

    print("\n")
    pprint.pprint(complete_build)

    driver.quit()

if __name__ == "__main__":
    main()