import pytumblr
from bs4 import BeautifulSoup
import json


# Authenticate via API Key
client = pytumblr.TumblrRestClient('MuGUwzyl2L0zahpFu7WJVNgeTFmypWG1AsrIB0GmxEj1HTawiy')

##
##
##
## This fucntion removes the caption or url portion of the strings input
def strip_input(i):
    i = i[8:-2]
    return i

def str_input(i):
    i=i[12:-2]
    return i
## The following function takes all the post ids for a blog and places it into a list. Knows how to stop
## by taking the number of posts and stopping after going post#mod20. (Eg: Total Posts: 3107, maximum offset: 3100)
## When getting total posts, only displays total number through blog info. Take this number then pass it to 
## tumblr get posts with photo as the type filter, which then will display total posts with photos. 
## when taking posts via the Tumblr API 
## By the way, go by offsets of 20
## Also, check if the post can be viewed in legacy. Posts that cannot be viewed should be handled by the other code.


## The following takes in a singular post id for a blog.
# Make the request
html_doc=client.posts('star-nomads.tumblr.com', id="636343217862868992")
test=json.dumps(html_doc, indent=4)

## The following function takes in the text and prints it into a temporary text file. Then all the captions are placed into an array,
## and the corresponding original photos' urls are placed into another array (The very first element of the captions array is the caption of the post)
# Write the string into a temporary text file
with open("uhhh.txt","w") as f:
    f.write(test)
    f.write("SDKF")

post_source=[]
post_captions=[]
post_photos=[]

with open('uhhh.txt', "r") as f:
    foundPhotos=False
    lc=0 #line count
    for line in f:

        if(not(line.find('"source_url":')==-1)): ##find the source url of the post
            u=line.strip()
            u=u[15:-5] #strip the source_url part to essentials
            post_source.append(u)
        
        if(not(line.find("caption")==-1)): #found the string "caption" and print the next 3 lines
            post_captions.append(str_input(line.strip()))
            foundPhotos=True


        if(foundPhotos and lc<=3):#print the line
            # print(line)
            if(not(line.find("url")==-1)): #found the url
                post_photos.append(strip_input(line.strip()))

            lc+=1 #iterate
            if(lc==3):
                lc=0
                foundPhotos=False


## when in the gui and inputting tags display the tag name and number of 
print(post_captions)
print(post_photos)
print(post_source)

## On occasion, some posts will not work because they are unable to be opened via legacy or something. So I already
## have a function in savingCode.py which will solve this problem by just directly parsing through all the images manually
## which will be a pain but like. Yknow. Better than nothing. Depending on the theme it'll probably go through all of the other images
## So it'll be good to be able to see the images and select (click?) which ones you want to save.
## Also, the captions are gonna be displayed in a list too, so it can be chosen. Whatever. Ugh