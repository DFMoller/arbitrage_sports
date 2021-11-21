from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import sys
sys.path.append('C:/Users/dfmol/Programming/arbitrage_betting/selenium_scrapers/upcoming_tennis/inc')
import sunbet_functions
from sunbet_functions import open_filter_dropdown, select_filter_by_time, find_event_days, expand_day, find_daily_rows, interpret_daily_row, collect_data, save_data
import time, datetime

web = 'https://www.sunbet.co.za/#filter/tennis'
path = 'C:/Users/dfmol/Programming/arbitrage_betting/selenium_scrapers/upcoming_tennis/chromedriver_win32/chromedriver.exe'
dt_format = '%d-%m-%Y %H:%M'

def scrape_sunbet():

    # initiate scraper
    driver = webdriver.Chrome(path)
    driver.get(web)
    open_filter_dropdown(driver)
    select_filter_by_time(driver)
    upcoming_days = find_event_days(driver)
    for day in upcoming_days:
        expand_day(day)
    for day in upcoming_days:
        time.sleep(1)
        loop = True
        while loop:
            loop = False
            time.sleep(1)
            daily_rows = find_daily_rows(day)
            for count, row in enumerate(daily_rows):
                clicked = interpret_daily_row(count, daily_rows)
                if clicked:
                    # element has been clicked
                    loop = True # need to start loop again, because daily_rows have changed
                    break
                else:
                    # element has not been clicked
                    pass
    time.sleep(1)
    print("Collecting Data...")
    match_list, statistics = collect_data(upcoming_days, dt_format)
    save_data({
        'statistics': statistics,
        'matches': match_list
    })
    driver.quit()

if __name__ == "__main__":
    scrape_sunbet()