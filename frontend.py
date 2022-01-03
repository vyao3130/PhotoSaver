from flask import Flask
from flask import request
from flask import render_template
import tumblrAPItest
import savingCode

import uuid # library to create unique identifiers for photsos
import urllib.request # library to save image from input url


app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
IMAGES_FOLDER = "Images/"

@app.route('/')
def my_form():
    return render_template("first-page.html")
     

@app.route('/', methods=['POST'])
def find_images():
    """
    Take in post id via submit element, lead to another template
    which shows the images retrieved.

        Parameters:
            None
        Returns:
            An html template that's filled out with images from the image_url_list

    """
    image_url_list=[]

    image_id = request.form['image_id']
    image_URLs = tumblrAPItest.getImages(image_id)
    # the getImages method only works with newer tumblr posts
    # so another method needs to be tried to handle older tumblr posts
    # and also add another post to check that the image post id is valid
    
    for image_url in image_URLs:
        image_url_list.append(image_url)
    
    return render_template('save_images.html', image_url_list=image_url_list)

def save_image():
    """
    Save the single image and the tags input by the user in a text file.
    Also saves the image's post information in a text file.
    (Change to mySQL or something later, text file temp solution.)
        Parameters:
            None
        Returns:
            None
    """
    image_tags = request.form[tags]
    image_url = request.form[image_url]
    image_file_name = str(uuid.uuid4())

    # fuck me running getting the images from the url have to be done thru 
    # actual web scraping (beautiful soup)
    # and the image urls ou find will have to start with 64.media.tumblr.com
    # and all have the same pattern, with a pixel size at the end for the multiple kinds
    savingCode.save_image_from_url(image_url, IMAGES_FOLDER, image_file_name)
    savingCode.write_to_database(image_path, caption, image_tags, image_url)
    
def view_images():
    """
    View searched images that are tagged.

    """
    pass

if __name__ == '__main__':
    app.run()