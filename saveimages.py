from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys
from bs4 import BeautifulSoup


def scroll_down(driver):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height

def save_bigText(bigText, file_name):
    """
        Parses the big text returned by the image_box 
        bigText (string) : big mass of html text from /archive tumblr
    """
    # getting all this text can take a while so we'll also save it into a temp text file
    with open(file_name, "w",  encoding="utf-8") as f:
        f.write(bigText)

def parse_bigText(file_name):
    """
        Parse the big mass of html taken from the tumblr archive into
        usable chunks.
        The chunks have the format of list[]
        return: list of tumblr posts as links list[str]
    """
    post_dictionary=[]
    with open(file_name, "r", encoding="utf-8") as f:
        soup_archive = BeautifulSoup(f, "html.parser")
        post_list = soup_archive.find_all(attrs={"class":"oKaff QmZ0e"})
 
        for post in post_list:
            htmlized_link = BeautifulSoup(str(post), "html.parser")
            cleaned_posts = htmlized_link.find_all("a","oKaff QmZ0e")
            split_post = str(cleaned_posts).split(" ")
            post_dictionary.append(split_post[3][6:-1])
        print(type(post_dictionary))
        print(post_dictionary)
        return post_dictionary

def get_archive_html(link):
    """
    Gets the entire html source code of a dynamic webpage and saves it to an html file.
    todo: put link somewhere and name html file after link in some way
    """
    # link = "https://star-nomads.tumblr.com/archive"
    driver = webdriver.Chrome()
    driver.get(link)
    scroll_down(driver)
    bigText_archive = driver.page_source
    if "archive" in link:
        html_link_name = link.split(".")
        html_link_name2 = html_link_name[0][8:]
        save_bigText(bigText_archive, file_name=html_link_name2)
        return html_link_name2
    elif "post" in link:
        html_link_name = link.split("post/")
        html_link_name2 = html_link_name[1]
        save_bigText(bigText_archive, file_name=html_link_name2)
        return html_link_name2
    else:
        print(f"The link {link} can't be parsed for file use.")
        sys.exit(1)

def process_link(link):
    """
    Processes the link to a tumblr post- saves the image link, source, and original post link into a dictionary.
    Param: link (str)
    Return: dict{"img_link":str, "source":str, "post_link":str}
    """
    post_html_file = get_archive_html(link)
    with open(post_html_file, 'r', encoding='utf-8') as f:
        soup_html = BeautifulSoup(f, "html.parser")
        img_list = soup_html.find_all(attrs={"class":"post_media_photo_anchor"})
        for img in img_list:
            ac_img_link = str(img).split("data-big-photo=")[1]
            # print(ac_img_link)
            ac_img_link1 = ac_img_link.split(" ")[0]
        print(ac_img_link1)
def main():
    # get_archive_html()
    # make driver
    # image_box = driver.find_element(by=By.CLASS_NAME, value="TlRfv")
    # image_box = driver.page_source
    # print(image_box.get_attribute("innerHTML"))
    process_link("https://star-nomads.tumblr.com/post/732790132063731712")
    # bigText_archive = image_box.get_attribute("innerHTML")

    # links2posts = parse_bigText("bigText.html")
    # for link in links2posts:
    #     process_link(link)
    # parse text


if __name__ == "__main__":
    main()