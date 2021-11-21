from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
import sys, json, threading, time
sys.path.append('C:/Users/dfmol/Programming/arbitrage_betting/selenium_scrapers/live_soccer')
import sunbet_live_soccer, sportingbet_live_soccer
from sunbet_live_soccer import init_live_sunbet, read_live_sunbet
from sportingbet_live_soccer import init_live_sportingbet, read_live_sportingbet
from difflib import SequenceMatcher


sunbet_url = 'https://www.sunbet.co.za/#filter/football'
sportingbet_url = 'https://sports.sportingbet.co.za/en/sports/live/football-4?fallback=false'
driver_path = 'C:/Users/dfmol/Programming/arbitrage_betting/selenium_scrapers/live_tennis/chromedriver_win32/chromedriver.exe'


def similar(a, b):
    # return SequenceMatcher(None, a, b).ratio()
    a_split = a.split()
    b_split = b.split()

    similarities = 0

    for i in a_split:
        for x in b_split:
            if i == x:
                if i != "fc":
                    similarities += 1
    
    return similarities

def calculate_arbitrage(sunbet_odds, sportingbet_odds):
    arbitrage_list = []
    arbitrage_list.append(1/float(sunbet_odds['oddsA']) + 1/float(sportingbet_odds['odds_draw']) + 1/float(sportingbet_odds['oddsB']))
    arbitrage_list.append(1/float(sunbet_odds['odds_draw']) + 1/float(sportingbet_odds['oddsA']) + 1/float(sportingbet_odds['oddsB']))
    arbitrage_list.append(1/float(sunbet_odds['oddsB']) + 1/float(sportingbet_odds['oddsA']) + 1/float(sportingbet_odds['odds_draw']))
    arbitrage_list.append(1/float(sportingbet_odds['oddsA']) + 1/float(sunbet_odds['odds_draw']) + 1/float(sunbet_odds['oddsB']))
    arbitrage_list.append(1/float(sportingbet_odds['odds_draw']) + 1/float(sunbet_odds['oddsA']) + 1/float(sunbet_odds['oddsB']))
    arbitrage_list.append(1/float(sportingbet_odds['oddsB']) + 1/float(sunbet_odds['oddsA']) + 1/float(sunbet_odds['odds_draw']))
    lowest = 10
    for arb in arbitrage_list:
        if arb < lowest:
            lowest = arb
    return lowest

def init_browser():
    driver = webdriver.Chrome(driver_path)
    driver.execute_script("window.open('about:blank', 'sunbet');")
    driver.switch_to.window("sunbet")
    driver.get(sunbet_url)
    box = init_live_sunbet(driver)
    driver.execute_script("window.open('about:blank', 'sportingbet');")
    driver.switch_to.window("sportingbet")
    driver.get(sportingbet_url)
    events = init_live_sportingbet(driver)
    return driver, box, events

def main(driver, box, events):

    while True:

        print("\n###########  NEW LOOP  ##############")

        driver.switch_to.window("sunbet")
        time.sleep(1)
        sunbet_matches = read_live_sunbet(box)

        driver.switch_to.window("sportingbet")
        time.sleep(1)
        sportingbet_matches = read_live_sportingbet(events)

        out_data = []
        
        num_pairs = 0
        for sportingbet_match in sportingbet_matches:
            for sunbet_match in sunbet_matches:
                match = False

                # condition1 = similar(sportingbet_match['teamA_name'].lower(), sunbet_match['teamA_name'].lower()) > 0.1
                # condition2 = similar(sportingbet_match['teamA_name'].lower(), sunbet_match['teamB_name'].lower()) > 0.1
                # condition3 = similar(sportingbet_match['teamB_name'].lower(), sunbet_match['teamB_name'].lower()) > 0.1
                # condition4 = similar(sportingbet_match['teamB_name'].lower(), sunbet_match['teamA_name'].lower()) > 0.1

                condition1 = similar(sportingbet_match['teamA_name'].lower(), sunbet_match['teamA_name'].lower()) > 0
                condition2 = similar(sportingbet_match['teamA_name'].lower(), sunbet_match['teamB_name'].lower()) > 0
                condition3 = similar(sportingbet_match['teamB_name'].lower(), sunbet_match['teamA_name'].lower()) > 0
                condition4 = similar(sportingbet_match['teamB_name'].lower(), sunbet_match['teamB_name'].lower()) > 0

                odds_I = sportingbet_match['odds']['oddsA']
                odds_II = sportingbet_match['odds']['odds_draw']
                odds_III = sportingbet_match['odds']['oddsB']
                odds_IV = sunbet_match['odds']['oddsA']
                odds_V = sunbet_match['odds']['odds_draw']
                odds_VI = sunbet_match['odds']['oddsB']
                condition5 = odds_I != None and odds_II != None and odds_III != None and odds_IV != None and odds_V != None and odds_VI != None

                if condition1 and condition4 and condition5:
                    teamA_name_sunbet = sunbet_match['teamA_name']
                    teamB_name_sunbet = sunbet_match['teamB_name']
                    teamA_name_sportingbet = sportingbet_match['teamA_name']
                    teamB_name_sportingbet = sportingbet_match['teamB_name']
                    sunbet_odds = {
                        'oddsA': sunbet_match['odds']['oddsA'],
                        'odds_draw': sunbet_match['odds']['odds_draw'],
                        'oddsB': sunbet_match['odds']['oddsB']
                    }
                    sportingbet_odds = {
                        'oddsA': sportingbet_match['odds']['oddsA'],
                        'odds_draw': sportingbet_match['odds']['odds_draw'],
                        'oddsB': sportingbet_match['odds']['oddsB']
                    }
                    print(f"\nGame Matched: {teamA_name_sunbet} vs {teamB_name_sunbet}")
                    print(f"\tSunbet Odds: {sunbet_odds['oddsA']} - {sunbet_odds['odds_draw']} - {sunbet_odds['oddsB']}")
                    print(f"\tSportingbet Odds: {sportingbet_odds['oddsA']} - {sportingbet_odds['odds_draw']} - {sportingbet_odds['oddsB']}")
                    match = True

                # These conditions are true if sunbet and sportingbet list teams in different orders
                elif condition2 and condition3 and condition5:
                    teamA_name_sunbet = sunbet_match['teamA_name']
                    teamB_name_sunbet = sunbet_match['teamB_name']
                    teamA_name_sportingbet = sportingbet_match['teamB_name']
                    teamB_name_sportingbet = sportingbet_match['teamA_name']
                    sunbet_odds = {
                        'oddsA': sunbet_match['odds']['oddsA'],
                        'odds_draw': sunbet_match['odds']['odds_draw'],
                        'oddsB': sunbet_match['odds']['oddsB']
                    }
                    # Notice that the odds get swapped for these conditions
                    sportingbet_odds = {
                        'oddsA': sportingbet_match['odds']['oddsB'],
                        'odds_draw': sportingbet_match['odds']['odds_draw'],
                        'oddsB': sportingbet_match['odds']['oddsA']
                    }
                    print(f"\nGame Matched: {teamA_name_sunbet} vs {teamB_name_sunbet}")
                    print(f"\tSunbet Odds: {sunbet_odds['oddsA']} - {sunbet_odds['odds_draw']} - {sunbet_odds['oddsB']}")
                    print(f"\tSportingbet Odds: {sportingbet_odds['oddsA']} - {sportingbet_odds['odds_draw']} - {sportingbet_odds['oddsB']}")
                    match = True
                
                if match:
                    arbitrage = calculate_arbitrage(sunbet_odds, sportingbet_odds)
                    print(f'Calculated Arbitrage: {str(arbitrage)}')
                    out_data.append({
                        "sunbet": {
                            "teamA": teamA_name_sunbet,
                            "teamB": teamB_name_sunbet,
                            "link": sunbet_match['link'],
                            "arbitrage": arbitrage,
                            "odds": sunbet_odds
                        },
                        "sportingbet": {
                            "teamA": teamA_name_sportingbet,
                            "teamB": teamB_name_sportingbet,
                            "link": sportingbet_match['link'],
                            "arbitrage": arbitrage,
                            "odds": sportingbet_odds
                        }
                    })
                    num_pairs += 1
        with open("out/matched_live_soccer_games.json", 'w') as json_outfile:
            json.dump(out_data, json_outfile)

if __name__ == "__main__":
    while True:
        try:
            driver, box, events = init_browser()
            main(driver, box, events)
        except StaleElementReferenceException as err:
            print(f'{err} -> Starting over in 1 second...')
            time.sleep(1)