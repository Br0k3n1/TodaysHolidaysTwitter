from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import sys

# !!DONT TOUCH GOOGLE CHROME IT WILL PROBABLY MESS IT UP!!

monthDict={1:'january', 2:'february', 3:'march', 4:'april', 5:'may', 6:'june', 7:'july', 8:'august', 9:'september', 10:'october', 11:'november', 12:'december'}

# Loop through all months
for monthNumber in range(1, 13):
    # Get Month and URL
    month = monthDict[monthNumber]
    url = f'https://nationaltoday.com/{month}-holidays/'

    # Setup Driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_window_position(10000, 0, windowHandle='current')
    driver.get(url)
    
    # Remove Popup from screen
    while True:
        isPopup = driver.find_elements_by_xpath('//*[@id="om-n1ckfw2xewacbaibb9nm-optin"]/div/div/div/div')
        if len(isPopup) > 0:
            sleep(1)
            driver.find_element_by_xpath('//*[@id="om-n1ckfw2xewacbaibb9nm-optin"]/div/button').click()
            break
            

    # Get the table with all the holidays
    HolidayTable = driver.find_elements_by_xpath('//*[@id="main"]/div[4]/table/tbody/tr')
    
    # Open/Create text file
    with open(os.path.join(sys.path[0], f"Holidays\{month}.txt"), "w") as f:
        # Loop through rows in holiday table
        for tr in range(0, len(HolidayTable)):
            # Get Row
            row = driver.find_element_by_xpath(f'//*[@id="main"]/div[4]/table/tbody/tr[{tr + 1}]')
            
            # If row is header remove day
            if row.get_attribute("class").split()[0] == "row-header":
                print(driver.find_element_by_xpath(f'//*[@id="main"]/div[4]/table/tbody/tr[{tr + 1}]/td/div/span[1]').text)
                f.write(driver.find_element_by_xpath(f'//*[@id="main"]/div[4]/table/tbody/tr[{tr + 1}]/td/div/span[1]').text + "\n")
            
            # If row is holiday remove catagory and tags
            elif row.get_attribute("class").split()[0] == "row-data":
                print(driver.find_element_by_xpath(f'//*[@id="main"]/div[4]/table/tbody/tr[{tr + 1}]/td[2]').text)
                f.write(driver.find_element_by_xpath(f'//*[@id="main"]/div[4]/table/tbody/tr[{tr + 1}]/td[2]').text + "\n")

    driver.quit()