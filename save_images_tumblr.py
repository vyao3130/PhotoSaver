# saves the images
import pytumblr
import os

tumblr_key = os.getenv('TUMBLR_KEY')

# Authenticate via API Key
client = pytumblr.TumblrRestClient(tumblr_key)

# Make the request
# print(client.posts('starbitscoffee.tumblr.com'))

# don't forget to make requests for posts as a string
def get_all_posts(tumblr_name: str) -> list:
    """
    Gets all the posts from a specific tumblr. 
    tumblr_name: tumblr post name
    Returns:
        list of tumblr post links
    """
    # get all posts
    number_of_posts = (client.blog_info(tumblr_name).get('blog')).get('posts')
    print(number_of_posts)
    for i in range(0, -(number_of_posts//-20)):
        tumblr_posts = client.posts(offset=i*20)


get_all_posts('starbitscoffee.tumblr.com')
