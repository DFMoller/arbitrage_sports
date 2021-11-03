from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import time, datetime, csv, json


def open_filter_dropdown(driver):
    while(1):
        try:
            sorting_options = driver.find_element(By.CLASS_NAME, "KambiBC-mod-event-group-filtering-options-container")
            sort_button = sorting_options.find_element(By.CLASS_NAME, "KambiBC-mod-event-sort-selection")
            sort_button.click()
            time.sleep(0.5)
            break

        except ElementClickInterceptedException as err:
            print("ElementClickInterceptedException -> Page not ready")
            print("Retrying in 1 second...")
            time.sleep(1)
        
        except NoSuchElementException as err:
            print("NoSuchElementException -> Page not ready")
            print("Retrying in 1 second...")
            time.sleep(1)

def select_filter_by_time(driver):
    sorting_dropdown = driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div[2]/div/ul')
    sorting_dropdown.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div[2]/div/ul/li[2]').click()

def find_event_days(driver):
    box = driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div[2]/div/div[3]/div[2]/div/div/div/div/div/div[4]/div')
    rows = box.find_elements(By.CLASS_NAME, 'KambiBC-mod-event-group-container')
    print("Number of rows:", str(len(rows)))

    # remove live events
    upcoming_days = []
    for count, row in enumerate(rows):
        try:
            live_icon = row.find_element(By.CLASS_NAME, 'LiveIcon__Label-sc-4apq0x-2')
            print(f'Row {count+1} is live')
        except NoSuchElementException:
            upcoming_days.append(row)
            print(f'Row {count+1} is not live')
    
    return upcoming_days

def expand_day(day):
    try:
        expansion = day.find_element(By.CLASS_NAME, 'CollapsibleContainer__CollapsibleContent-sc-14bpk80-3')
        # if found, it is already expanded
        print("Day expanded!")
    except NoSuchElementException as err:
        # element not found, means not yet expanded
        print("Day not expanded! About to click!")
        day.click()

def find_daily_rows(day):
    expansion = day.find_element(By.CLASS_NAME, 'KambiBC-mod-event-group-event-container')
    child_rows = expansion.find_elements(By.XPATH, './*')
    return child_rows

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


def collect_data(upcoming_days):
    return_list = []
    for day in upcoming_days:
        daily_rows = find_daily_rows(day)
        date_str = day.find_element(By.CLASS_NAME, 'CollapsibleContainer__LabelDetails-sc-14bpk80-8').text + "2021"
        dt_obj = datetime.datetime.strptime(date_str, '%d %B %Y')
        tournament = ''
        for count, row in enumerate(daily_rows):
            element_class = row.get_attribute("class")
            if "KambiBC-betoffer-labels" in element_class:
                tournament = row.find_element(By.CLASS_NAME, 'CollapsibleContainer__Title-sc-14bpk80-7').text
            elif "KambiBC-list-view__event-list" in element_class: # This element is a ul containing data
                matches = row.find_elements(By.CLASS_NAME, 'KambiBC-event-item--sport-TENNIS')
                for match in matches:
                    link = match.find_element(By.CLASS_NAME, 'KambiBC-event-item__link').get_attribute('href')
                    names = match.find_elements(By.CLASS_NAME, 'KambiBC-event-participants__name')
                    # print(f'{names[0].text} vs {names[1].text}')
                    player_a_lastname = names[0].text.split(', ')[0]
                    player_b_lastname = names[1].text.split(', ')[0]
                    outcome_boxes = match.find_elements(By.CLASS_NAME, 'KambiBC-betty-outcome')
                    player_a_odds = outcome_boxes[0].find_element(By.CLASS_NAME, 'OutcomeButton__Odds-sc-lxwzc0-5').text
                    player_b_odds = outcome_boxes[1].find_element(By.CLASS_NAME, 'OutcomeButton__Odds-sc-lxwzc0-5').text
                    player_a = {
                        'namestring': names[0].text,
                        'lastname': player_a_lastname,
                        'names': names[0].text.replace(f'{player_a_lastname}, ', ''),
                        'odds': player_a_odds
                    }
                    player_b = {
                        'namestring': names[1].text,
                        'lastname': player_b_lastname,
                        'names': names[1].text.replace(f'{player_b_lastname}, ', ''),
                        'odds': player_b_odds
                    }
                    node = {
                        'sport': 'tennis',
                        'date': date_str,
                        'players': [player_a, player_b],
                        'site': 'sunbet',
                        'tournament': tournament,
                        'link': link
                    }
                    return_list.append(node)
    return return_list

def save_data(match_list):
    # with open('results.csv', 'w') as csv_file:
    #     writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     writer.writerow(['Player A', 'Odds A', 'Player B', 'Odds B'])
    with open('results.json', 'w') as json_file:
        json.dump(match_list, json_file)