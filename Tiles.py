from PIL import Image
import os
from bs4 import BeautifulSoup
import urllib2
import io
import random
import math
from imgurpython.helpers.error import ImgurClientError

import re

class Tile:
    """docstring for Tile"""
    def __init__(self, image, idx, tile_pixels):
        self.im = image
        self.idx = idx
        self.name = "tile_" + str(idx)
        self.new_pixels = list(self.im.getdata())

        self.pixels = tile_pixels
        
        self.path = None
        self.upload_data = None
        self.imgur_id = None
        self.link = None
        self.similar_links = None
        self.similar_image = None
        

    def save_temp(self, path="data/temp"):
        self.path = os.path.join(path, self.name+".jpg")
        self.im.save(self.path)
        print "[+] Saved", self.name, "at", self.path
    
    def remove_temp(self, path="data/temp"):
        if self.path is not None:
            os.remove(self.path)
            print "[+] Removed", self.name, "from", self.path
        else:
            print "[-] tried to remove", self.name, "but couldn't find a path."


    def download_similar(self, random = False):
        for i in range(len(self.similar_links)):
            try:
                fd = urllib2.urlopen(self.similar_links[0])
                image_file = io.BytesIO(fd.read())
                self.similar_image = Image.open(image_file)
                w = self.similar_image.size[0]
                h = self.similar_image.size[1]

                

                # print "size :", self.similar_image.size[0], self.similar_image.size[1]
                factor = 1.01
                while self.similar_image.size[0] < self.im.size[0] or self.similar_image.size[1] < self.im.size[1]:
                    size = int(w*factor), int(h*factor)
                    self.similar_image = self.similar_image.resize(size, Image.ANTIALIAS)
                    factor += 0.01
                # print "size :", self.similar_image.size[0], self.similar_image.size[1] 
                


                path = os.path.join("data/temp", self.name+"_vs.jpg")
                self.similar_image.save(path) 

                w = self.similar_image.size[0]
                h = self.similar_image.size[1]
                x_pos = (w/2) - (self.im.size[0]/2)
                y_pos = (h/2) - (self.im.size[1]/2)
                crop_region = self.similar_image.crop((  x_pos ,  y_pos , x_pos+self.im.size[0], y_pos+self.im.size[1]))
                path = os.path.join("data/temp", self.name+"_vs2.jpg")
                crop_region.save(path) 
                self.new_pixels = list(crop_region.getdata())

                break
            except:
                pass


    def show_similar(self):
        self.similar_image.show()

    
    def upload_imgur(self, client): 
        print client
        try:
            self.upload_data = client.upload_from_path(self.path, config=None, anon=True)
            self.imgur_id = self.upload_data["id"]
            self.link = self.upload_data["link"]
            print "[+] UPLOADED", self.name, "TO imgur with link", self.link, "and id", self.imgur_id
        except ImgurClientError as e:
     
            print(e.error_message)
            print(e.status_code)

class Tiles(object):
    """docstring for Tiles"""
    def __init__(self, image, columns, rows):
        self.columns = columns
        self.rows = rows
        self.image = image
        self.image_w = image.size[0]
        self.image_h = image.size[1]
        self.tile_w = self.image_w/columns
        self.tile_h = self.image_h/rows

        self.tiles = self.init_tiles()

    def init_tiles(self):
        tiles_out = list()
        idx = 0

        for y in range(self.rows):
            for x in range(self.columns):
                h = self.tile_h
                w = self.tile_w
                y_pos = (y*h)
                x_pos = (x*w) 


                pix_count = 0
                tile_pixels = list()
                for yy in range(self.image_h):
                    for xx in range(self.image_w):
                        if xx >= x_pos and xx < x_pos+w and yy >= y_pos and yy < y_pos+h:
                            tile_pixels.append(pix_count)
                        pix_count += 1

                tile = self.image.crop((x_pos,y_pos, x_pos+w, y_pos+h))
                tiles_out.append( Tile( tile, idx, tile_pixels))
                idx += 1
        return tiles_out

    def save_output(self, path="data/temp", name="visually_similar_mosaic"):
        path = os.path.join(path, name+".jpg")
        self.image.save(path)
        print "[+] Saved", name+".jpg", "at", path

    

    # BATCH OPERATIONS:

    def save_temp(self, path="data/temp"):
        if not os.path.isdir(path):
            os.makedirs(path)
        for tile in self.tiles:
            tile.save_temp(path)

    def remove_temp(self, path="data/temp"):
        for tile in self.tiles:
            tile.remove_temp(path)

    def upload_imgur(self, client):
        for tile in self.tiles:
            tile.upload_imgur(client)
            # break


    def process(self):
        base_url = 'https://yandex.ru/images/search?rpt=imageview&img_url='
        for tile in self.tiles:
            try:
                url = base_url + tile.link
                html = urllib2.urlopen(url).read()
                soup = BeautifulSoup(html, 'html.parser')
                
                imgs = soup.find_all('img')
                tile.similar_links = list()

                for img in soup.findAll('img', attrs={'class': re.compile(r".*\bsimilar__image\b.*")}):
                # for img in imgs:
                    try:
                        # if 'similar__image' in img['class']:
                        similar_img = "https:"+str(img['src'])
                        tile.similar_links.append(similar_img)
                        print "added link"
                    except KeyError:
                        print "this is an error, why?"
                        pass

                tile.download_similar()
            except:
                pass
            # tile.show_similar()

            # break

    

    def replace_pixels(self):
        pix_val = list(self.image.getdata())

        for tile in self.tiles:

            for i, pix in enumerate(tile.pixels):
                pix_val[pix] = tile.new_pixels[i]


        self.image.putdata(pix_val)













