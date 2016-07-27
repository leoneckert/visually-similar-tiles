import os
import argparse
from imgurpython import ImgurClient
from PIL import Image
import Tiles as t
import requests
import ConfigParser

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-c", "--columns", default=2, type=int, help="Path to the image")
ap.add_argument("-r", "--rows", default=2, type=int, help="Path to the image")
args = vars(ap.parse_args())

config = ConfigParser.ConfigParser()
try:
    config.read('settings.cfg')
    print "[+] Read settings"
except:
    print "[-] Could not read settings"
client_id = config.get('imgur','client_id')
client_secret = config.get('imgur','client_secret')


if __name__ == '__main__':

    # image = cv2.imread(args["image"])
    image = Image.open(args["image"])
    print type(image)
    print image
    columns = args["columns"]
    rows = args["rows"] 

    tiles = t.Tiles(image, columns, rows)
    
    # tiles.open_all()
    # cv2.waitKey(0)

    



    
    client = ImgurClient(client_id, client_secret)

    tiles.save_temp()
    tiles.upload_imgur(client)
    

    tiles.process()


    # tiles.delete_imgur(client)


    tiles.remove_temp()




# client_id = 'YOUR CLIENT ID'
# client_secret = 'YOUR CLIENT SECRET'

# client = ImgurClient(client_id, client_secret)

# get_image(image_id)
# upload_from_path(path, config=None, anon=True)
# upload_from_url(url, config=None, anon=True)
# delete_image(image_id)
# favorite_image(image_id)



    # configDomain = config.get('google','domain')
    # configEmail = config.get('google','email')
    # configPass = config.get('google','psswrd')