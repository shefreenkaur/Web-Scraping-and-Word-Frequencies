from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time  #to add delays

#set up
service = Service("C:\\Program Files (x86)\\chromedriver.exe")

#chrome options
chrome_options = Options()

#initalizing driver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get("https://www.bclaws.gov.bc.ca/civix/content/lc/statreg/?xsl=/templates/browse.xsl")
    #since the page keeps exiting on its own withing 1 second.
    time.sleep(1000)
finally:
     driver.quit()