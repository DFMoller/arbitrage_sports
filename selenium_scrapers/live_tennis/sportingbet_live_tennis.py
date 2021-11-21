from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
import sys, time, pprint, datetime, pprint, json

dt_format = '%d-%m-%Y %H:%M'


def save_data(final_data):
    with open('selenium_scrapers/live_tennis/data/sportingbet-live-data.json', 'w') as json_file:
        json.dump(final_data, json_file)


def read_live_sportingbet(events):
    match_list = []
    for event in events:
        if 'grid-event' in event.get_attribute('class'):
            # this element is a match
            try:
                live_icon = event.find_element(By.CLASS_NAME, 'live-icon') # if found, this match is live
            except NoSuchElementException as err:
                # match is not live
                continue
            try:
                link = event.find_element(By.CLASS_NAME, 'grid-info-wrapper').get_attribute('href')
                names = event.find_elements(By.CLASS_NAME, 'participant')
                player_countries = event.find_elements(By.CLASS_NAME, 'participant-country')
                player_A_fullname = names[0].text.replace(player_countries[0].text, "")
                player_A_firstname = player_A_fullname.split()[0]
                player_A_lastname = player_A_fullname.split()[1]
                player_B_fullname = names[1].text.replace(player_countries[1].text, "")
                player_B_firstname = player_B_fullname.split()[0]
                player_B_lastname = player_B_fullname.split()[1]
                # print(f'\n{names[0].text}')
                # print(names[1].text)
            except IndexError as err:
                print(f"\nIndexError caused by: {link}")
                continue
            odds_container = event.find_element(By.CLASS_NAME, 'grid-group-container')
            odds_categories = odds_container.find_elements(By.CLASS_NAME, 'grid-option-group')
            odds = odds_categories[0].find_elements(By.CLASS_NAME, 'grid-option')
            if len(odds) > 0:
                odds_A = odds[0].find_element(By.CLASS_NAME, 'option-value').text
                odds_B = odds[1].find_element(By.CLASS_NAME, 'option-value').text
                player_A = {
                    "namestring": player_A_fullname,
                    "lastname": player_A_lastname,
                    "names": player_A_firstname,
                    "odds": odds_A
                }
                player_B = {
                    "namestring": player_B_fullname,
                    "lastname": player_B_lastname,
                    "names": player_B_firstname,
                    "odds": odds_B
                }
                node = {
                    'sport': 'tennis',
                    'date_time': "live",
                    'date_time_format': None,
                    'site': 'sportingbet',
                    'link': link,
                    'players': [player_A, player_B]
                }
                match_list.append(node)
    return match_list


def init_live_sportingbet(driver):
    while True:
        time.sleep(1)
        try:
            driver.find_element(By.CLASS_NAME, 'theme-sorting').click()
            while True:
                time.sleep(1)
                try:
                    droplist = driver.find_elements(By.CLASS_NAME, 'sort-selector-option')
                    droplist[1].click()
                    print("Filtering by time...")
                    break
                except NoSuchElementException as err:
                    print("Waiting...")
            break
        except NoSuchElementException as err:
            print("Waiting...")
    while True:
        time.sleep(1)
        try:
            box = driver.find_element(By.XPATH, '/html/body/vn-app/vn-dynamic-layout-single-slot[4]/vn-main/main/div/ms-main/ng-scrollbar/div/div/div/div/ms-main-column/div/ms-live/ms-live-event-list/div/ms-grid/ms-event-group')
            break
        except NoSuchElementException as err:
            print("Waiting...")
    events = box.find_elements(By.XPATH, '*')
    return events


if __name__ == "__main__":
    events = init_live_sportingbet()
    matches = {
        'matches': read_live_sportingbet(events)
    }
    save_data(matches)

