from flask import Flask
from flask import request
from flask import render_template
import tumblrAPItest
import savingCode

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'

@app.route('/')
def my_form():
    return render_template("first-page.html")
     

@app.route('/', methods=['POST'])
image_elem_list=[] # uhhh this is bad practice i think but it's universal
# so like. shush

def findImages():
    """
    Take in image id via submit element, lead to another template
    which shows the images retrieved.
        Parameters:
        Returns:

    """
    image_elem_list=[]

    image_id = request.form['image_id']
    image_URL = tumblrAPItest.getImages(image_id)
    
    image_elem_list.append(image_URL)
    return render_template('save_image.html', image_elem_list=image_elem_list)
    # print all of the images from the post in a for loop here actually
    # via return, and render another template that leads to entering tags

def save_image():
    """
    Save the single image and the tags input by the user in a text file.
    Also saves the image's post information in a text file.
    (Change to mySQL or something later, text file temp solution.)
        Parameters:
            None
        Returns:
            Nothing
    """
    image_tags = request.form[tags]
    save_info = savingCode.writeDatabase()

    return 
def view_images():
    """
    View searched images that are tagged.

    """
    pass

if __name__ == '__main__':
    app.run()