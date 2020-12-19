import pytumblr
from bs4 import BeautifulSoup
import json


# Authenticate via API Key
client = pytumblr.TumblrRestClient('MuGUwzyl2L0zahpFu7WJVNgeTFmypWG1AsrIB0GmxEj1HTawiy')

    ## The following function takes all the post ids for a blog and places it into a list. Knows how to stop
    ## by taking the number of posts and stopping after going post#mod20. (Eg: Total Posts: 3107, maximum offset: 3100)
    ## When getting total posts, only displays total number through blog info. Take this number then pass it to 
    ## tumblr get posts with photo as the type filter, which then will display total posts with photos. 
    ## when taking posts via the Tumblr API 
    ## By the way, go by offsets of 20
    ## Also, check if the post can be viewed in legacy. Posts that cannot be viewed should be handled by the other code.
def getTumblrPostIds(blogname):
    ##
    ##
    post_ids=[]

    blog_Info=client.blog_info(blogname)
    maxPosts=blog_Info["blog"]["total_posts"]
    blog_Obj=client.posts(blogname, type='photo', offset=maxPosts) 
    max_photos=blog_Obj["total_posts"]+1 #+1 because range stops right before reaching the actual #
    
    for x in range(0, max_photos, 20): #increment by 20 bc max # posts to get via API is 20
        post_batch=client.posts(blogname, type='photo', offset=x)
        ids=post_batch["posts"]
        for id in ids:
                getImages(id["id_string"])


def getImages(post_id):
    ## The following takes in a singular post id for a blog.
    # Make the request
    html_doc=client.posts('star-nomads.tumblr.com', id=post_id) 
    
    try:
        print(html_doc["posts"][0]["caption"])
        print(html_doc["posts"][0]["summary"])
        
        photo_list=html_doc["posts"][0]["photos"]
        for val in photo_list:
            print(val["original_size"]["url"])
            print(val["caption"])
        

    except: #post doesn't have images in correct format
        print("No caption") #this needs to be handled later via 

    post_source=[]
    post_captions=[]
    post_photos=[]

    ## The following function takes in the text and prints it into a temporary text file. Then all the captions are placed into an array,
    ## and the corresponding original photos' urls are placed into another array (The very first element of the captions array is the caption of the post)
    # Write the string into a temporary text file
    # with open('temp.txt', "r") as f:
    #     foundPhotos=False
    #     lc=0 #line count
    #     for line in f:

    #         if(not(line.find('"source_url":')==-1)): ##find the source url of the post
    #             u=line.strip()
    #             u=u[15:-5] #strip the source_url part to essentials
    #             post_source.append(u)
            
    #         if(not(line.find("caption")==-1)): #found the string "caption" and print the next 3 lines
    #             u=line.strip()
    #             u=u[12:-2] #strip the caption part to essentials
    #             post_captions.append(u)
    #             foundPhotos=True


    #         if(foundPhotos and lc<=3):#print the line after finding the photos object and find the original post
    #             if(not(line.find("url")==-1)): #found the url
    #                 u=line.strip()
    #                 u=u[8:-2]   
    #                 post_photos.append(u)

    #             lc+=1 #iterate
    #             if(lc==3):
    #                 lc=0
    #                 foundPhotos=False
    # print(post_captions)
    # print(post_photos)
    # print(post_source)

## when in the gui and inputting tags display the tag name and number of photos within that tag.


## On occasion, some posts will not work because they are unable to be opened via legacy or something. So I already
## have a function in savingCode.py which will solve this problem by just directly parsing through all the images manually
## which will be a pain but like. Yknow. Better than nothing. Depending on the theme it'll probably go through all of the other images
## So it'll be good to be able to see the images and select (click?) which ones you want to save.
## Also, the captions are gonna be displayed in a list too, so it can be chosen. Whatever. Ugh

# def checkJSON():
#     html_doc=client.posts('star-nomads.tumblr.com', id="637860088164564992")
#     test=json.dumps(html_doc, indent=4)
#     with open("temp.txt","w") as f:
#         f.write(test)

getTumblrPostIds("star-nomads.tumblr.com")
# checkJSON()
getImages(637860088164564992)