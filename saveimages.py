from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def scroll_down(self):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = self.driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = self.driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height


def main():
    driver = webdriver.Chrome()
    driver.get("https://star-nomads.tumblr.com/archive")
    text_box = driver.find_element(by=By.CLASS_NAME, value="TlRfv")
    print(text_box)


if __name__ == "__main__":
    main()