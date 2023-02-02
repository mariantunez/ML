import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from csv_generator import create_csv

CSV_PATH = '../CSVFiles/FligthsData2.csv'
CHROME_DRIVER_PATH = 'chromedriver.exe'

# Set Chrome driver
driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=webdriver.ChromeOptions())
driver.implicitly_wait(10)


def open_path(DAY):
    '''Opens webpage acording to the DAY of March 2023 to scrape and closes possible popups windows using the Chrome Driver.
     The search is set to only United Airlines and American airlines with Flights with no stops between Houston to Seattle'''

    FLIGHTS_PATH = 'https://www.kayak.com/flights/IAH-SEA/2023-03-' + str(DAY) + '?sort=price_a&fs=airlines=AS,UA;stops=0'
    
    driver.get(FLIGHTS_PATH)
    driver.implicitly_wait(20)

    # Close popup windows that may appears when the page initially loads
    try:
        XP_CORNER_POPUP = '//*[@class="bBPb-close"]'
        driver.find_element(By.XPATH, XP_CORNER_POPUP).click()

        driver.implicitly_wait(10)

        XP_FULLSCREEN_POPUP = '//*[@class="dDYU-close dDYU-mod-variant-right-corner-outside dDYU-mod-size-default"]'
        driver.find_element(By.XPATH, XP_FULLSCREEN_POPUP).click()
    except Exception:
        pass

    driver.implicitly_wait(10)


def scrape_flight_by_day(DAY):
    '''Scrapes the DATE, PRICES, AIRLINES, TIME & MERIDIEM of flights on a particular day by a xpath. 
        Returns collected data as a pandas Data Frame '''

    open_path(DAY)

    print('Starting Scrape for March ' + str(DAY)) 
    
    # Define XPath of each element to scrape
    XP_DATE = '//*[@class="sR_k-value"]'
    XP_PRICES = '//*[@class="price option-text"]/span'
    XP_AIRLINE = '//*[@class="section times"]/div[2]'
    XP_DEPART_TIME = '//*[@class="depart-time base-time"]'
    XP_MERIDIEM = '//*[@class="time-meridiem meridiem"]'

    # Retreive data by their xpath
    prices = get_by_xpath(XP_PRICES)
    airlines = get_by_xpath(XP_AIRLINE)
    time = get_by_xpath(XP_DEPART_TIME)
    meridiem = get_by_xpath(XP_MERIDIEM)[::2]
    week_day = get_by_xpath(XP_DATE)[0].split()[0]


    prices = list(filter(None, prices))
    prices = [price.replace('$', '') for price in prices]

    dates = [DAY]*len(airlines)
    days = [week_day]*len(airlines)

    # Organice in Dataframe
    FLIGHTS_DATA = {'Airline':airlines,
         'Weekday':days,
         'Date':dates, 
         'Departure Time':time, 
         'Departure Meridiem':meridiem, 
         'Price':prices
         }
        

    flights = pd.DataFrame(data=FLIGHTS_DATA)
    
    print(flights)

    return flights


def get_by_xpath(XPATH): 
    '''Uses chrome driver to find data by a given Xpath'''
    data = [value.text for value in driver.find_elements(By.XPATH, XPATH)]
    driver.implicitly_wait(5)
    return data


def collect_data(DAY):
    '''Initializes the scrape of a particular day until a dataframe is return.
        Writes final Dataframe to a csv file'''
    data = []
    flight = pd.DataFrame(data)

    while(flight.empty):
        flight = scrape_flight_by_day(DAY)

    flight.to_csv(CSV_PATH, header=False, index=False, mode='a')

    driver.implicitly_wait(5)


def start_scraper():
    '''Creates csv file and collects data for each day of the month'''
    create_csv(CSV_PATH)

    for day in range(1, 32):
        day = '{:02}'.format(day)
        collect_data(day)


start_scraper()
driver.quit()
