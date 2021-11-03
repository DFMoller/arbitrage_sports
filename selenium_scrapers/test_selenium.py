from selenium import webdriver
import time

web = 'https://sports.tipico.de/en/all/football/spain/la-liga'
# web = 'https://betway.com/en/sports'
path = 'C:/Users/dfmol/Programming/arbitrage_betting/selenium_scrapers/chromedriver_win32/chromedriver.exe'

driver = webdriver.Chrome(path)
driver.get(web)

time.sleep(3) #add implicit wait, if necessary
accept = driver.find_element_by_xpath('//*[@id="_evidon-accept-button"]')
accept.click()

teams = []
x12 = [] #3-way
odds_events = []

# //*[@id="app"]/main/main/section/div/div[1]/div/div
# //*[@id="app"]/main/main/section/div/div[1]/div/div/div
box = driver.find_element_by_xpath('//div[contains(@testid, "Program_SELECTION")]')
rows = box.find_elements_by_class_name('EventRow-styles-event-row')

driver.quit()