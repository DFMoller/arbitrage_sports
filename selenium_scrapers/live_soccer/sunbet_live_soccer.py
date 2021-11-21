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
    with open('selenium_scrapers/live_soccer/data/sunbet-live-soccer-matches.json', 'w') as json_file:
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
        if len(odds) == 3:
            oddsA = odds[0].text
            oddsDraw = odds[1].text
            oddsB = odds[2].text
        else:
            oddsA = None
            oddsDraw = None
            oddsB = None
        team_A_name = names[0].text
        team_B_name = names[1].text
        node = {
            'teamA_name': team_A_name,
            'teamB_name': team_B_name,
            'link': link,
            'odds': {
                'oddsA': oddsA,
                'odds_draw': oddsDraw,
                'oddsB': oddsB
            }
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
    driver_path = 'C:/Users/dfmol/Programming/arbitrage_betting/selenium_scrapers/live_tennis/chromedriver_win32/chromedriver.exe'
    sunbet_url = 'https://www.sunbet.co.za/#filter/football'
    driver = webdriver.Chrome(driver_path)
    driver.get(sunbet_url)
    time.sleep(1)
    box = init_live_sunbet(driver)
    final_data = {
        'matches': read_live_sunbet(box)
    }
    save_data(final_data)
    driver.quit()
            