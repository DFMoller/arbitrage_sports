from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
import sys, time, pprint, datetime, pprint, json

base_url = 'https://sports.sportingbet.co.za/en/sports/tennis-5/betting?tab=matches'
driver_path = 'C:/Users/dfmol/Programming/arbitrage_betting/selenium_scrapers/upcoming_tennis/chromedriver_win32/chromedriver.exe'
dt_format = '%d-%m-%Y %H:%M'
final_data = []

def save_data(match_list):
    with open('selenium_scrapers/upcoming_tennis/data/sportingbet-upcoming-data.json', 'w') as json_file:
        json.dump(match_list, json_file)


def scrape_sportingbet():
    statistics = {
        'num_matches': 0
    }
    driver = webdriver.Chrome(driver_path)
    driver.get(base_url)
    while True:
        time.sleep(1)
        try:
            box = driver.find_element(By.XPATH, '/html/body/vn-app/vn-dynamic-layout-single-slot[4]/vn-main/main/div/ms-main/ng-scrollbar[2]/div/div/div/div/ms-main-column/div/ms-fixture-list/div/div/div/div/ms-grid')
            break
        except NoSuchElementException as err:
            print("Waiting...")
    count = 0
    while count < 5:
        time.sleep(1)
        try:
            while True:
                time.sleep(3)
                try:
                    driver.find_element(By.CLASS_NAME, 'grid-footer').click()
                    print("More Matches clicked!")
                    break
                except ElementClickInterceptedException as err:
                    print("Trying to click...")
        except NoSuchElementException as err:
            print("Waiting...")
            count += 1
    time.sleep(5)
    events = box.find_elements(By.XPATH, '*')
    for event in events:
        if 'event-group' in event.get_attribute('class'):
            tournament = event.find_element(By.CLASS_NAME, 'title').text
            matches = event.find_elements(By.CLASS_NAME, 'grid-event')
            for match in matches:
                try:
                    live_icon = match.find_element(By.CLASS_NAME, 'live-icon') # if works, means this match is live
                    continue
                except NoSuchElementException as err: # Means this match is not live
                    pass
                link = match.find_element(By.CLASS_NAME, 'grid-info-wrapper').get_attribute('href')
                names = match.find_elements(By.CLASS_NAME, 'participant')
                player_countries = match.find_elements(By.CLASS_NAME, 'participant-country')
                try:
                    player_A_fullname = names[0].text.replace(player_countries[0].text, "")
                except IndexError as err:
                    print(err)
                    continue
                player_A_firstname = player_A_fullname.split()[0]
                player_A_lastname = player_A_fullname.split()[1]
                player_B_fullname = names[1].text.replace(player_countries[1].text, "")
                player_B_firstname = player_B_fullname.split()[0]
                player_B_lastname = player_B_fullname.split()[1]
                td_obj = datetime.date.today()
                tmrw_obj = td_obj + datetime.timedelta(days=1)
                td_str = td_obj.strftime('%d-%m-%Y')
                tmrw_str = tmrw_obj.strftime('%d-%m-%Y')
                starting_time_str = match.find_element(By.CLASS_NAME, 'starting-time').text
                if 'Tomorrow' in starting_time_str:
                    dt_str = f'{tmrw_str} {starting_time_str.replace("Tomorrow / ", "")}'
                    local_dt_format = dt_format
                elif 'Today' in starting_time_str:
                    dt_str = f'{td_str} {starting_time_str.replace("Today / ", "")}'
                    local_dt_format = dt_format
                elif 'Starting now' in starting_time_str:
                    dt_str = "live"
                    local_dt_format = None
                    print(f"Live Match: {player_A_fullname}")
                elif 'Starting' in starting_time_str:
                    timedelta_str = starting_time_str.replace("Starting in ", "").replace(" min", "")
                    starting_time_obj = datetime.datetime.now() + datetime.timedelta(minutes=int(timedelta_str))
                    starting_time_str = starting_time_obj.strftime("%H:%M")
                    dt_str = f'{td_str} {starting_time_str}'
                    local_dt_format = dt_format
                    print(f"Starting soon: {dt_str} -> {link}")
                elif starting_time_str == "":
                    dt_str = ""
                    local_dt_format = None
                    print(f"Empty starting time str: {player_A_fullname}")
                else:
                    try:
                        dt_obj = datetime.datetime.strptime(starting_time_str, '%d/%m/%Y %H:%M') # just to check if the format is correct
                        dt_str = dt_obj.strftime(dt_format)
                        local_dt_format = dt_format
                        # print(f'Date: ')
                    except ValueError as err:
                        print(f'Unknown Date! ValueError when converting string: {err}')
                        dt_str = "unknown"
                        local_dt_format = "unknown"
                master_odds_box = match.find_element(By.CLASS_NAME, 'grid-group-container')
                relevant_odds_container = master_odds_box.find_elements(By.CLASS_NAME, 'grid-option-group')[0]
                odds = relevant_odds_container.find_elements(By.CLASS_NAME, 'option-value')
                odds_A = odds[0].text
                odds_B = odds[1].text
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
                    'date_time': dt_str,
                    'date_time_format': local_dt_format,
                    'site': 'sportingbet',
                    'tournament': tournament,
                    'link': link,
                    'players': [player_A, player_B]
                }
                final_data.append(node)
                statistics['num_matches'] += 1
    save_data({
        'statistics': statistics,
        'matches': final_data
    })
    driver.quit()

if __name__ == "__main__":
    scrape_sportingbet()