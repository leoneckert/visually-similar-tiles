import os
import argparse
import cv2
import Tiles as t

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-c", "--columns", default=2, type=int, help="Path to the image")
ap.add_argument("-r", "--rows", default=2, type=int, help="Path to the image")
args = vars(ap.parse_args())

if __name__ == '__main__':


    # load the image and show it
    image = cv2.imread(args["image"])
    # cv2.imshow("Original", image)
    columns = args["columns"]
    rows = args["rows"] 




    tiles = t.Tiles(image, columns, rows)
    tiles.open_all()
    cv2.waitKey(0)





