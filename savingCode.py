import urllib.request
import os
import pytumblr
from bs4 import BeautifulSoup
# re stands for regular expressions
import re
import requests
# BeautifulSoup is for parsing html as a tree

def createClient():
    client = pytumblr.TumblrRestClient(
        '<consumer_key>',
        '<consumer_secret>',
        '<oauth_token>',
        '<oauth_secret>',
    )

    client.info() # Grabs the current user information

# # Create a function that will scrape a tumblr account for images and download
# # all of them into a folder
# def tumblr_scrapeWholeBlog(input_url):
#     url = input_url
#     # Send a "get" request (I want "this" page) to the URL the user provided, r
#     # is created as an object (which is a Python object)
#     r = requests.get(url)
#     # Format the provided URL into text
#     data = r.text
#     # We're feeding "data" to BeautifulSoup with lxml as a parser
#     soup = BeautifulSoup(data, 'lxml')
#     # Give the title of the Tumblr site as name for the image folder
#     title = soup.title.text
#     # Find where this .py file sits on the device, points to the file, dir name
#     # points at the directory that containt this file - on level above
#     dir_path = os.path.dirname(os.path.abspath(__file__))
#     # Name the new folder with the title variable, taken from Tumblr site
#     # dir_path + what folder I want the new folder to live in
#     download_folder = os.path.join(dir_path, str(title))
#     if os.path.exists(download_folder):
#         pass
#     else:
#         os.mkdir(download_folder)
#     # Track down the images and download them into the folder you just created
#     # Also we will give the images slightly meaningful filenames
#     # Filename will be tumblrtitle_page#_image#
#     imgnum = 0
#     for link in soup.find_all("img"):
#         image = link.get("src")
#         if re.search("78.media.tumblr.com/", image):
#             file_format = image.split("/")[-1].split(".")[-1]
#             img_name = soup.title.text + "_" + str(page_num)+"_"+ str(imgnum)
#             img_path = os.path.join(download_folder, img_name + "." +
#                 file_format)
#             urlretrieve(image, img_path)
#             imgnum += 1

# def tumblr_scrapeWholeBlogImplementation():
#     # Now we need to find the "next" button for this page

#     print("Done downloading all images from " + title)

#     # Print Welcome message, request user input: TUMBLR URL
#     input_url = input("Welcome to Tumblr Image Scrape!\n\n\nThis script is a quick "
#     "and easy way to archive all the images from posts on a Tumblr site of your "
#     "choice.\n\n\nATTENTION: this script does not automatically stop when all "
#     "images from the Tumblr have been downloaded. To stop this script in terminal "
#     "you need to press [control]+[C] on your keyboard.\n\n\nPlease provide the URL "
#     "of a Tumblr from which you wish to download all the images, and then press "
#     "[ENTER]: ")
#     # ensure there is a slash at the end of URL so page advance works
#     if input_url[-1] != "/":
#         input_url = input_url + "/"
#     else:
#         # pass means do nothing
#         pass
#     # ensure there is a http:// at the start of the URL so script works
#     if input_url[0:6] != "http://":
#         input_url = "http://" + input_url
#     else:
#         pass

#     page_num = 1
#     while page_num:
#         print("Downloaded: images from page "+ str(page_num))
#         if page_num == 1:
#             tumblr_scrapeWholeBlog(input_url)
#         else:
#             tumblr_scrapeWholeBlog(input_url + "page/" + str(page_num))
#         page_num += 1


# def getTumblrImage():
#     """Gets the tumblr post via the tumblr api and places all the direct image links in a list"""
#     client = pytumblr.TumblrRestClient(
#     'MuGUwzyl2L0zahpFu7WJVNgeTFmypWG1AsrIB0GmxEj1HTawiy',
#     'ETS50dbxPoUur6MHAR6VhcRYtnvvqN12LZhKIXhldHNhjD61Su',
#     'f8u19Ni7hgbT48IXxeMtKFjsmA8eEcMt5dZm43Ii80615yhdiU',
#     'euqkoqwADf59LoUoi1iK8IpcVs9cMhzluxMGTioiBG14gBUcE5'
#     )
    

def save_image_from_direct_url(urlLinked, path, file_name):
    """Takes the urlLink (with .png or .jpg at the end) and saves it along
     with the file name.   
        Parameters:
            urlLinked (string): Url that contains only the image.
            path (string): Path to save the image to.
            file_name (string): Name of file without extension
        Returns:
            None
     
     """

    image_file_path=path+file_name+urlLinked[-4:]

    urllib.request.urlretrieve(urlLinked, image_file_path) #create the temporary image file in directory


def write_to_database(image_path, caption, input_tags, imageURL):
    """
    Take the string input and append it into the tagsListAllImages textfile in the format where [image_location, image_caption, tag1,tag2] 
    where [tag1,tag2] is a post and [tag1, tag2] is another post.

        Keyword Arguments:
            imagePath -- str, where the image for the tag is located 
            caption -- str, where the caption of the image is located
            imageUrl -- url of image
            inputtags -- input tags, currently formatted as a String
            the tags list will then be printed into a text file to be saved and viewed for later.  
        Returns:
            None    
    """

    f= open("imageDatabase.txt","a+")
    f.write("[" + "Image path: " + image_path + ", Caption: " + caption + ", tags: " + input_tags + ", Image URL: " + imageURL + "]" + "\n")
    f.close
    # return something to display to the user to confirm what they want

def get_images_direct(tumblr_url):
    """
    Get direct links to tumblr images. Takes in the url of the tumblr post containing the image,
    then returns a list of links containing the largest images in the post only.

    Parameters:
        tumblr_url (string): Url to tumblr image post
    
    Returns:
        direct_image_urls(List[string]): List of direct links to the images from the tumblr image post
        OR 
        Empty List: No images were found
    """
    
    direct_image_urls = []
    # Send a GET request (I want "this" page) to the URL the user provided, 
    # r is created as an object (which is a Python object)
    request_object = requests.get(url)

    raw_data = request_object.text
    # We're feeding "data" to BeautifulSoup with lxml as a parser
    html_soup = BeautifulSoup(data, 'lxml')

    for link in soup.find_all("img"):
        image_link = link.get("src") #this finds the image photoset
        if re.search("78.media.tumblr.com/", image_link) or re.search("64.media.tumblr.com/", image_link):
            # cut out all images that aren't above a certain size
            # because everyone's themes are different 

            # then cut out possible similar images retrieved because of the various sizes
            # depending on the theme of course


    return direct_image_urls

def main():
    """Actual implementation from running this file:"""

    # Print Welcome message, request user input: TUMBLR URL
    input_url = input("Welcome to Tumblr Image Scrape!\nThis script is a quick "
    "and easy way to archive all the images from a post on a Tumblr site of your "
    "choice.\nATTENTION: this script does not automatically stop when all "
    "images from the Tumblr have been downloaded. To stop this script in terminal "
    "you need to press [control]+[C] on your keyboard.\nPlease provide the URL "
    "of a Tumblr from which you wish to download all the images, and then press "
    "[ENTER]: ")

    foundCaption = False
    url = input_url
    # Send a "get" request (I want "this" page) to the URL the user provided

    # r is created as an object (which is a Python object)
    r = requests.get(url)
    # Format the provided URL into text
    data = r.text
    # We're feeding "data" to BeautifulSoup with lxml as a parser
    soup = BeautifulSoup(data, 'lxml')
    # Give the title of the Tumblr site as name for the image folder
    tumblrName = soup.title.text
    tags = "no Tags"
    foldername=input("Enter anticipated folder name: ")
    filename=input("Enter the name of all the files: ")
    fileNumber=0

    for link in soup.find_all("img"):
        image = link.get("src") #this finds the image photoset

        if re.search("78.media.tumblr.com/", image) or re.search("64.media.tumblr.com/", image): #look for the images in the hmtl soup
            print("We're currently on this image here: " + image)
            wantImage = input("Do you want this image? (y to confirm)," + "\n"
            + "(Type quit to exit): ")
            if(wantImage == "y"):
                l=input("y to change current folder " + foldername + ": ")
                if( l == "y"):
                    directory_contents = os.listdir(".")
                    print("Current folders: ")
                    print(directory_contents)
                    foldername=input("Enter folder name: ")
                
                t=input("y to change the filename." + filename)
                if(t == "y"):
                    filename=input("Enter the new name of the file: ")
                    fileNumber=0
            
                if not(foundCaption):
                    for captions in soup.find_all("meta"):
                        print(captions.get("content"))
                        wantCaption = input("Y to confirm caption: ")
                        if(wantCaption == "y"):
                            image_caption=captions.get("content")
                            foundCaption=True
                            break
                        elif(wantCaption == "quit"):
                            break

                newTags=input("Current tags: " + tags + "\n"
                "Y to change current tags: ")
                if (newTags=="y"):
                    tags=input("Type in all of the tags that apply, seperate via commas: ")
                else:
                    pass
                
                fileNumber+=1
                e(image, filename + str(fileNumber), foldername)
                pathImg="D:/PhotoSaver/"+foldername+filename+image[-4:]
                writeDatabase(pathImg, image_caption, tags, input_url)
            elif (wantImage == "quit"):
                break
            else:
                print("Alright, we'll move on.")

    
    # #tags=input("Enter the tags. Commas seperate tags: ") #Okay this has to be in there for sorting. Print each tag that applies I guess.

