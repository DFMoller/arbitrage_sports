from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
import sys, time, pprint, datetime
sys.path.append('C:/Users/dfmol/Programming/arbitrage_betting/selenium_scrapers/inc')
# from betway_functions import get_tournament_urls

tournaments_base_url = 'https://sports.betway.de/en/sports/ctg/tennis'
path = 'C:/Users/dfmol/Programming/arbitrage_betting/selenium_scrapers/chromedriver_win32/chromedriver.exe'
dt_format = '%d-%m-%Y %H:%M'
driver = webdriver.Chrome(path)

betway_pages = {
    'tennis/atp'
}
            

def get_first_level_links(url):
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
        links[link] = {'tour_name': tournament_name}
    return links


def get_second_level_links(lookup_table):
    new_lookup = {}
    for tour in lookup_table:
        new_lookup[tour] = []
        tournament_name = lookup_table[tour]['tour_name']
        print(tour)
        print(tournament_name)
        driver.get(tour) # fetch a page for every individual tournament
        while True:
            try:
                box = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div[1]/div/div[2]/div[4]/div/div[2]/div/div[1]/div/div')
                break
            except NoSuchElementException as err:
                print('Waiting...')
                time.sleep(1)
        links = box.find_elements(By.CLASS_NAME, 'showAllButton')
        print(f'Number of showAllButtons: {str(len(links))}')
        for link in links:
            href = link.get_attribute('href').replace('///', f'/tennis/{tournament_name}/')
            if 'doubles' in href or 'outright' in href: # filter out unwanted events
                continue
            else:
                new_lookup[tour].append(href)
                print(f'\t{href}')
    return new_lookup


def get_third_level_links(lookup_table):
    match_row_xpath = '/html/body/div[1]/div/div[3]/div/div[1]/div/div[2]/div[4]/div/div[3]/div[2]/div/div/div[2]/div/div[1]'
    new_lookup = {}
    for tour in lookup_table:
        new_lookup[tour] = {}
        for loc in lookup_table[tour]:
            time.sleep(3)
            new_lookup[tour][loc] = []
            driver.get(loc)
            count = 0
            while True and count < 5:
                time.sleep(1)
                try:
                    # matches = driver.find_elements(By.CLASS_NAME, 'oneLineScoreboard')
                    # print(loc)
                    # print(f'\tNumber of matches: {str(len(matches))}')
                    # break
                    main = driver.find_element(By.CLASS_NAME, 'mainContent')
                    print(f"Main found: {loc}")
                    try:
                        matches = driver.find_elements(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[1]/div/div[2]/div[4]/div/div[3]/div[2]/div/div/div[2]/div/div[*]')
                        print(f'Number of matches = {str(len(matches))}')
                    except NoSuchElementException as err:
                        print("No match")
                    # for x in range(10):
                    #     try:
                    #         driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[1]/div/div[2]/div[4]/div/div[3]/div[2]/div/div/div[2]/div/div[{x}]')
                    #         print(f'Found match number {x}')
                    #     except NoSuchElementException as err:
                    #         print("No more matches to be found")
                    #         break
                    break
                except NoSuchElementException as err:
                    print(f"Waiting... : {loc}")
                    count += 1
            # for match in matches:
            #     try:
            #         match.find_element(By.CLASS_NAME, 'scoreCollection') # if found, then match is live
            #         continue
            #     except NoSuchElementException as err:
            #         # match is not live -> Proceed as normal
            #         match_link = match.find_element(By.CLASS_NAME, 'scoreboardInfoNames').get_attribute('href')
            #         new_lookup[tour][loc].append(match_link)
    return new_lookup

# def scrape_data(build):
#     final = []
#     for url in build:
#         driver.get(url)
#         while True:
#             time.sleep(1)
#             try:
#                 box = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div[1]/div/div[2]/div[4]/div/div[3]/div[2]/div')
#                 break
#             except NoSuchElementException as err:
#                 print("Waiting...")
#         matches = day.find_elements(By.CLASS_NAME, 'oneLineEventItem')
#         for match in matches:
#             try:
#                 match.find_element(By.CLASS_NAME, 'scoreCollection') # if found, then match is live
#                 continue
#             except NoSuchElementException as err:
#                 # match is not live -> Proceed as normal
#                 match_time = match.find_element(By.CLASS_NAME, 'oneLineDateTime').text
                
#                 match_link = match.find_element(By.CLASS_NAME, 'scoreboardInfoNames').get_attribute('href')
#                 player_A_full = match.find_element(By.CLASS_NAME, 'teamNameHomeTextFirstPart').text
#                 player_B_full = match.find_element(By.CLASS_NAME, 'teamNameAwayTextFirstPart ').text
#                 player_A_lastname = player_A_full.split()[-1]
#                 player_B_lastname = player_B_full.split()[-1]
#                 odds = match.find_elements(By.CLASS_NAME, 'baseOutcomeItem')
#                 odds_A = odds[0].text
#                 odds_B = odds[1].text
#                 player_A = {
#                     'namestring': player_A_full,
#                     'lastname': player_A_lastname,
#                     'names': player_A_full.replace(player_A_lastname + ' ', ''),
#                     'odds': odds_A
#                 }
#                 player_B = {
#                     'namestring': player_B_full,
#                     'lastname': player_B_lastname,
#                     'names': player_B_full.replace(player_B_lastname + ' ', ''),
#                     'odds': odds_B
#                 }
#                 node = {
#                     "sport": 'tennis',
#                     "date_time": "dt_str",
#                     "date_time_format": dt_format,
#                     "site": "betway",
#                     "tournament": build[url]['tour_name'],
#                     "link": match_link,
#                     "players": [player_A, player_B]
#                 }
#                 final.append(node)
#     return final
            


def main():
    lookup_table = get_first_level_links(tournaments_base_url) # returns a dictionary
    lookup_table = get_second_level_links(lookup_table) # returns a refined dictionary
    lookup_table = get_third_level_links(lookup_table) # returns a refined dictionary

    print("\n")
    # pprint.pprint(lookup_table)

    # data_structure = scrape_data(complete_build)
    # pprint.pprint(data_structure)

    driver.quit()

if __name__ == "__main__":
    main()