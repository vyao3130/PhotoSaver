from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import sys
from bs4 import BeautifulSoup
import os
import json
import requests

def write_json_file(file_name : str, file_object):
    """
    Write to json file
    """
    json_file_object = json.dumps(file_object)
    with open(file_name, "w") as f:
        f.write(json_file_object)


def scroll_down(driver):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(5)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height

def save_bigText(bigText, file_name):
    """
        Parses the big text returned by the image_box 
        bigText (string) : big mass of text from any source
    """
    # getting all this text can take a while so we'll also save it into a temp text file
    with open(file_name, "w",  encoding="utf-8") as f:
        f.write(bigText)

def parse_blogarchive_html(file_name: str) -> list:
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

def get_archive_html(link: str):
    """
    Gets the entire html source code of a tumblr blog's archive and saves it to an html file.
    
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
    else:
        print(f"The link {link} can't be parsed for file use.")
        sys.exit(1)

def get_post_html(link: str):
        """
        Differs from the archive because the archive needs to scroll down :l
        Parses an embedded link and saves the inner parts to a text file for further processing.
        Returns None if class for post not found
        """
        driver = webdriver.Chrome()
        driver.get(link)
        scroll_down(driver)
        time.sleep(1) # sometimes the webdriver is still too fast lol
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div[2]/div/div[2]/iframe")))
        iframe = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div[2]/iframe")
        driver.switch_to.frame(iframe)
        element1 = driver.find_element(By.CLASS_NAME, 'xN3lM')
        # check if post body there
        if not element1:
            return None
        #make post name
        html_link_name = link.split("/")
        for split_link in html_link_name:
            if split_link.isnumeric():
                html_link_name2 = split_link
                break
        # save post html
        with open(os.path.join('posts', html_link_name2), 'w', encoding='utf-8') as f:
            f.write(element1.get_attribute('innerHTML'))
        return html_link_name2
        
        

def process_link(link: str):
    """
    Processes the link to a tumblr post- saves the image link, source, and original post link into a dictionary.
    Param: link (str)
    Return: post_dict (dict{"img_link":str, "source":str, "post_link":str})
    """
    post_html_file = get_post_html(link+"/embed")
    if not post_html_file:
        print("The link {link} was not properly processed.")
        return None
    with open(os.path.join("posts", post_html_file), 'r', encoding='utf-8') as f:
        soup_html = BeautifulSoup(f, "html.parser")
        img_list = []
        post_img_list = soup_html.find_all(attrs={"class":"RoN4R tPU70 xhGbM"})
        post_img_list.extend(soup_html.find_all(attrs={"class":"RoN4R xhGbM"})) # for some reason the embed also has this even though it's the same??
        print(f"list of images: {post_img_list}")
        # no images found in a different way
        if not post_img_list:
            print("No images were found for link {link}")
            return None
        
        for img in post_img_list:
            ac_img_link = str(img).split(" ")[-2]
            print(ac_img_link)
            # ac_img_link1 = ac_img_link.split(" ")[0]
            img_list.append(ac_img_link)
        
        # no images found
        if not img_list:
            print("No images were found for link {link}")
            return None
    
        return {"img_link": img_list, "post_link":link}

def save_image(link, file_name, folder_name):
    """
        Saves link image to file.
        Param: link (str) direct link to file
        file_name (str) file name
        folder_name (str) folder name
        Return: None
    """
    img_data = requests.get(link).content
    image_type = link[-4:] # should be .png or .jpg
    if not (image_type == ".jpg" or image_type == ".png"):
        print(f"Incorrect image type of {image_type} from link {link}.")
        return None
    with open(os.path.join(folder_name, file_name+image_type), 'wb') as handler:
        handler.write(img_data)
        print(f"Image sucessfully saved at {folder_name}/{file_name}{image_type}")

def save_images(img_dict_list: list[dict]):
    """
        Saves all the images in the image dict.
        Naming convention is based off of post_number+image+number
        If the image can't be saved, save into a different json file with the according post number as well.
        Returns a modified img_dict_list that contains the same things as image dict, with the addition of the path to the
            actual images saved.
    """
    mod_img_dict_list = []
    for img_dict in img_dict_list:
        image_links = img_dict.get("img_link")
        post_link = img_dict.get("post_link")
        html_link_name = link.split("/")
        for split_link in html_link_name:
            if split_link.isnumeric():
                html_link_name2 = split_link
                break
        for img in image_links:
            save_image(img, )
    
def main():
    # blog_link = "https://star-nomads.tumblr.com/archive"
    # saved_file = get_archive_html(blog_link)

    post_links = parse_blogarchive_html(r'C:\Users\Vivian\Documents\PhotoSaver\star-nomads')
    # save post_links
    write_json_file("post_links.json", post_links)

    with open("post_links.json", "r") as f:
        post_links = json.load(f)

    post_dicts = []
    not_working_posts=[]

    for post in post_links:
        print(f"working on {post}")
        post_info = process_link(post)
        if not post_info:
            print(f"The post {post} was not processed properly.")
            not_working_posts.append(post)
        else:
            print(f"Got this {post_info}")
            post_dicts.append(post_info)
    
    write_json_file("not_working_posts.json", not_working_posts)
    write_json_file("json_files.json", post_dicts)

    # save the images connected with each post
    with open("json_files.json",'r') as f:
        post_dictionary = json.load(f)
    
    for post_dict in post_dictionary:
        image_links = post_dict.get("img_link")
        

    # print(process_link("https://star-nomads.tumblr.com/post/732880681226715136"))
    # print(process_link('https://star-nomads.tumblr.com/post/726373271092789248/when-two-musicians-sing-into-the-same-microphone'))
    # bigText_archive = image_box.get_attribute("innerHTML")
    # save_image("https://64.media.tumblr.com/8777b29b0dde41a4dea5b9c70266759e/1ca9390b25a83b5b-89/s1280x1920/64bd60bcb80ca76cf7058a641bab865aa7c75aa7.jpg", "blarrgh", "images_star_nomads")

    # links2posts = parse_bigText("bigText.html")
    # for link in links2posts:
    #     process_link(link)
    # parse text


if __name__ == "__main__":
    main()