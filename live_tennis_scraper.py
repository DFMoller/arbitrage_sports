from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
import sys, json, threading, time
sys.path.append('C:/Users/dfmol/Programming/arbitrage_betting/selenium_scrapers/live_tennis')
import sunbet_live_tennis, sportingbet_live_tennis
from sunbet_live_tennis import init_live_sunbet, read_live_sunbet
from sportingbet_live_tennis import init_live_sportingbet, read_live_sportingbet


sunbet_url = 'https://www.sunbet.co.za/#filter/tennis'
sportingbet_url = 'https://sports.sportingbet.co.za/en/sports/live/tennis-5'
driver_path = 'C:/Users/dfmol/Programming/arbitrage_betting/selenium_scrapers/live_tennis/chromedriver_win32/chromedriver.exe'


def calculate_arbitrage(playerA_sun, playerB_sun, playerA_sport, playerB_sport):
    try:
        arbitrage1 = 1/float(playerA_sun['odds']) + 1/float(playerB_sport['odds'])
        arbitrage2 = 1/float(playerB_sun['odds']) + 1/float(playerA_sport['odds'])
    except ValueError as err:
        return None
    if arbitrage1 < arbitrage2:
        return arbitrage1
    else:
        return arbitrage2

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
                condition1 = sportingbet_match['players'][0]['lastname'].lower() == sunbet_match['players'][0]['lastname'].lower()
                condition2 = sportingbet_match['players'][0]['lastname'].lower() == sunbet_match['players'][1]['lastname'].lower()
                condition3 = sportingbet_match['players'][1]['lastname'].lower() == sunbet_match['players'][0]['lastname'].lower()
                condition4 = sportingbet_match['players'][1]['lastname'].lower() == sunbet_match['players'][1]['lastname'].lower()
                odds_I = sportingbet_match['players'][0]['odds']
                odds_II = sportingbet_match['players'][1]['odds']
                odds_III = sunbet_match['players'][0]['odds']
                odds_IV = sunbet_match['players'][1]['odds']
                condition5 = odds_I != None and odds_II != None and odds_III != None and odds_IV != None

                if condition1 and condition4 and condition5:
                    playerA_sun = sunbet_match['players'][0]
                    playerB_sun = sunbet_match['players'][1]
                    playerA_sport = sportingbet_match['players'][0]
                    playerB_sport = sportingbet_match['players'][1]
                    print(f"\nGame Matched: {playerA_sun['lastname']} vs {playerB_sun['lastname']}")
                    print(f"\tSunbet Odds: {playerA_sun['odds']} - {playerB_sun['odds']}")
                    print(f"\tSportingbet Odds: {playerA_sport['odds']} - {playerB_sport['odds']}")
                    match = True

                elif condition2 and condition3 and condition5:
                    playerA_sun = sunbet_match['players'][0]
                    playerB_sun = sunbet_match['players'][1]
                    playerA_sport = sportingbet_match['players'][1]
                    playerB_sport = sportingbet_match['players'][0]
                    print(f"\nGame Matched: {playerA_sun['namestring']} vs {playerB_sun['namestring']}")
                    print(f"\tSunbet Odds: {playerA_sun['odds']} - {playerB_sun['odds']}")
                    print(f"\tSportingbet Odds: {playerA_sport['odds']} - {playerB_sport['odds']}")
                    match = True
                
                if match:
                    arbitrage = calculate_arbitrage(playerA_sun, playerB_sun, playerA_sport, playerB_sport)
                    print(f'Calculated Arbitrage: {str(arbitrage)}')
                    out_data.append({
                        "sunbet": {
                            "player_A": playerA_sun,
                            "player_B": playerB_sun,
                            "link": sunbet_match['link'],
                            "arbitrage": arbitrage
                        },
                        "sportingbet": {
                            "player_A": playerA_sport,
                            "player_B": playerB_sport,
                            "link": sportingbet_match['link'],
                            "arbitrage": arbitrage
                        }
                    })
                    num_pairs += 1
        with open("out/matched_live_tennis_games.json", 'w') as json_outfile:
            json.dump(out_data, json_outfile)
                    

    # print(f'\nSunbet Matches: {sunbet_stats["num_matches"]}')
    # print(f'Sportingbet Matches: {sportingbet_stats["num_matches"]}')
    # print(f'Number of matches paired: {num_pairs}')

if __name__ == "__main__":
    driver, box, events = init_browser()
    main(driver, box, events)