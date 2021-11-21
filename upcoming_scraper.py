import sys, json
sys.path.append('C:/Users/dfmol/Programming/arbitrage_betting/selenium_scrapers/upcoming_tennis')
import sunbet_upcoming, sportingbet_upcoming
from sunbet_upcoming import scrape_sunbet
from sportingbet_upcoming import scrape_sportingbet




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


def main():
    scrape_sunbet()
    scrape_sportingbet()
    with open("selenium_scrapers/upcoming_tennis/data/sportingbet-upcoming-data.json", "r") as sportingbet_file:
        sportingbet_data = json.load(sportingbet_file)
        sportingbet_matches = sportingbet_data['matches']
        sportingbet_stats = sportingbet_data['statistics']
    with open("selenium_scrapers/upcoming_tennis/data/sunbet-upcoming-data.json", "r") as sunbet_file:
        sunbet_data = json.load(sunbet_file)
        sunbet_matches = sunbet_data['matches']
        sunbet_stats = sunbet_data['statistics']
    num_pairs = 0
    for sportingbet_match in sportingbet_matches:
        for sunbet_match in sunbet_matches:
            match = False
            condition1 = sportingbet_match['players'][0]['lastname'].lower() == sunbet_match['players'][0]['lastname'].lower()
            condition2 = sportingbet_match['players'][0]['lastname'].lower() == sunbet_match['players'][1]['lastname'].lower()
            condition3 = sportingbet_match['players'][1]['lastname'].lower() == sunbet_match['players'][0]['lastname'].lower()
            condition4 = sportingbet_match['players'][1]['lastname'].lower() == sunbet_match['players'][1]['lastname'].lower()
            # date_contition = sportingbet_match['']
            if condition1 and condition4:
                playerA_sun = sunbet_match['players'][0]
                playerB_sun = sunbet_match['players'][1]
                playerA_sport = sportingbet_match['players'][0]
                playerB_sport = sportingbet_match['players'][1]
                print(f"\nGame Matched: {playerA_sun['namestring']} vs {playerB_sun['namestring']}")
                print(f"\tSunbet Odds: {playerA_sun['odds']} - {playerB_sun['odds']}")
                print(f"\tSportingbet Odds: {playerA_sport['odds']} - {playerB_sport['odds']}")
                match = True

            elif condition2 and condition3:
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
                num_pairs += 1

    print(f'\nSunbet Matches: {sunbet_stats["num_matches"]}')
    print(f'Sportingbet Matches: {sportingbet_stats["num_matches"]}')
    print(f'Number of matches paired: {num_pairs}')
            

if __name__ == "__main__":
    main()