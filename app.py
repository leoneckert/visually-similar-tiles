import os
import argparse
from imgurpython import ImgurClient
from PIL import Image
import Tiles as t
import requests

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-c", "--columns", default=2, type=int, help="Path to the image")
ap.add_argument("-r", "--rows", default=2, type=int, help="Path to the image")
args = vars(ap.parse_args())

if __name__ == '__main__':


    # image = cv2.imread(args["image"])
    image = Image.open(args["image"])
    print type(image)
    print image
    columns = args["columns"]
    rows = args["rows"] 

    tiles = t.Tiles(image, columns, rows)
    
    tiles.open_all()
    cv2.waitKey(0)



get_image(image_id)
upload_from_path(path, config=None, anon=True)
upload_from_url(url, config=None, anon=True)
delete_image(image_id)
favorite_image(image_id)
