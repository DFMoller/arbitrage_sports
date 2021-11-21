from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
import sys, time, pprint, datetime, pprint, json


dt_format = '%d-%m-%Y %H:%M'


def interpret_daily_row(count, rows):
    element_class = rows[count].get_attribute("class")
    if count+1 < len(rows) and "KambiBC-betoffer-labels" in element_class: # if not the last item and item is clickable
        if "KambiBC-list-view__event-list" not in rows[count+1].get_attribute("class"): # if next item is not a ul
            rows[count].click()
            return True
        else:
            return False
    elif count+1 == len(rows) and "KambiBC-betoffer-labels" in element_class: # if last item is not expanded
        rows[count].click()
        return True
    elif "KambiBC-list-view__event-list" in element_class: # Item is a ul
        return False
    elif "KambiBC-betoffer-labels" not in element_class and "KambiBC-list-view__event-list" not in element_class:
        print("Row not recognized!!!")
        return False
    else:
        print("Unknown error...")
        return False


def save_data(final_data):
    with open('selenium_scrapers/live_tennis/data/sunbet-live-data.json', 'w') as json_file:
        json.dump(final_data, json_file)


def read_live_sunbet(box):
    match_list = []
    rows_box = box.find_element(By.CLASS_NAME, 'KambiBC-collapsible-content')
    live_matches = rows_box.find_elements(By.CLASS_NAME, 'KambiBC-event-item--live')
    for match in live_matches:
        link = match.find_element(By.CLASS_NAME, 'KambiBC-event-item__link').get_attribute('href')
        try:
            odds_box = match.find_element(By.CLASS_NAME, 'KambiBC-bet-offer__outcomes')
        except NoSuchElementException as err:
            # print(f'Match has no odds: {link}')
            continue
        names = match.find_elements(By.CLASS_NAME, 'KambiBC-event-participants__name')
        odds = match.find_elements(By.CLASS_NAME, 'OutcomeButton__Odds-sc-lxwzc0-5')
        if len(odds) == 2:
            oddsA = odds[0].text
            oddsB = odds[1].text
        else:
            oddsA = None
            oddsB = None
        player_A_lastname = names[0].text.split(', ')[0]
        try:
            player_A_firstname = names[0].text.split(', ')[1]
        except IndexError as err:
            player_A_firstname = ''
        player_B_lastname = names[1].text.split(', ')[0]
        try:
            player_B_firstname = names[1].text.split(', ')[1]
        except IndexError as err:
            player_B_firstname = ''
        # print(f'\nplayer a lastname: {player_A_lastname}')
        # print(f'player b lastname: {player_B_lastname}')
        playerA = {
            'lastname': player_A_lastname,
            'firstname': player_A_firstname,
            'odds': oddsA
        }
        playerB = {
            'lastname': player_B_lastname,
            'firstname': player_B_firstname,
            'odds': oddsB
        }
        node = {
            'players': [playerA, playerB],
            'link': link
        }
        match_list.append(node)
    return match_list


def init_live_sunbet(driver):
    while True:
        time.sleep(1)
        try:
            box = driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div[2]/div/div[3]/div[2]/div/div/div/div/div/div[4]/div/div[1]')
            break
        except:
            print("Waiting for page to load...")
    header = box.find_element(By.CLASS_NAME, 'CollapsibleContainer__HeaderWrapper-sc-14bpk80-1')
    while True:
        time.sleep(1)
        try:
            rows_box = box.find_element(By.CLASS_NAME, 'KambiBC-collapsible-content')
            break
        except NoSuchElementException as err:
            # rows not yet expanded
            print("Expanding live category")
            header.click()
    loop = True
    while loop:
        loop = False
        rows = rows_box.find_elements(By.XPATH, '*')
        time.sleep(1)
        for count, row in enumerate(rows):
            clicked = interpret_daily_row(count, rows)
            if clicked:
                # element has been clicked
                loop = True # need to start loop again, because daily_rows have changed
                break
            else:
                # element has not been clicked
                pass
    return box


if __name__ == "__main__":
    box = init_live_sunbet()
    final_data = {
        'matches': read_live_sunbet(box)
    }
    save_data(final_data)
            