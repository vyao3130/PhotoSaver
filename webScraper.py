from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def get_selenium():                           
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('headless') # won't open Chrome in new window      
    driver = webdriver.Chrome() 
    return (driver)

def loadEntirePage():
    """
        Load entire page w/infinite scrolling
    """
    selenium = get_selenium()                           
    selenium.get("your/url")    
    last_elem = ''
    while True:
        current_last_elem = "#my-div > ul > li:last-child"
        scroll = "document.querySelector(\'" + current_last_elem + "\').scrollIntoView();"
        selenium.execute_script(scroll) # execute the js scroll
        time.sleep(3) # wait for page to load new content
        if (last_elem == current_elem):
            break
        else:
            last_elem = current_elem                       
selenium = get_selenium()
print(type(selenium.get("https://star-nomads.tumblr.com/archive")))