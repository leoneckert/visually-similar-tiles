from PIL import Image
import os
from bs4 import BeautifulSoup
import urllib2
import io
import random
import math

class Tile:
    """docstring for Tile"""
    def __init__(self, image, xidx, yidx, idx, tile_pixels):
        self.im = image
        self.xidx = xidx
        self.yidx = yidx
        self.idx = idx
        self.name = "tile_" + str(idx)
        self.pixels = tile_pixels
        
        self.path = None
        self.upload_data = None
        self.imgur_id = None
        self.link = None
        self.similar_links = None
        self.similar_image = None

    def show(self):
        self.im.show()

    def download_similar(self, random = False):
        fd = urllib2.urlopen(self.similar_links[0])
        image_file = io.BytesIO(fd.read())
        self.similar_image = Image.open(image_file)

    def show_similar(self):
        self.similar_image.show()



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
    
    def upload_imgur(self, client): 
        # tile.upload_imgur(client)
        try:
            self.upload_data = client.upload_from_path(self.path, config=None, anon=True)
            self.imgur_id = self.upload_data["id"]
            self.link = self.upload_data["link"]
            # {u'datetime': 1469655152, u'bandwidth': 0, u'nsfw': None, u'vote': None, u'id': u'W1KkfXA', u'account_id': 0, u'in_gallery': False, u'title': None, u'section': None, u'width': 960, u'size': 12100, u'type': u'image/jpeg', u'is_ad': False, u'deletehash': u'RXuInXyOGiS98wj', u'description': None, u'views': 0, u'link': u'http://i.imgur.com/W1KkfXA.jpg', u'height': 144, u'name': u'', u'favorite': False, u'account_url': None, u'animated': False}
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
        print self.image_w 
        print columns
        print (self.image_w % columns)

        self.tile_h = self.image_h/rows
        self.tiles = self.init_tiles()

    def init_tiles(self):
        tiles_out = list()
        idx = 0

        for y in range(self.rows):
            for x in range(self.columns):
                # this is a workaround to get rif of a werid one pixel gap 
                # between tiles when changing their pixel values
                h = self.tile_h
                w = self.tile_w
                y_pos = (y*h) - 1
                h += 2
                x_pos = (x*w) - 1
                w += 2

                pix_count = 0
                tile_pixels = list()
                # for xx in range(self.image_w):
                for yy in range(self.image_h):
                    for xx in range(self.image_w):
                        if xx > x_pos and xx < x_pos+w and yy > y_pos and yy < y_pos+h:
                            tile_pixels.append(pix_count)
                        pix_count += 1

                tile = self.image.crop(( x_pos,y_pos, x_pos+w, y_pos+h))
                tiles_out.append( Tile( tile, x, y, idx, tile_pixels))
                idx += 1
        return tiles_out

    def open_all(self):
        for tile in self.tiles:
            tile.show()

    def save_output(self, path="data/temp", name="visually_similar_mosaic"):
        path = os.path.join(path, name+".jpg")
        self.image.save(path)
        print "[+] Saved", name+".jpg", "at", path

    def save_temp(self, path="data/temp"):
        if not os.path.isdir(path):
            os.makedirs(path)
        for tile in self.tiles:
            tile.save_temp(path="data/temp")

    def remove_temp(self, path="data/temp"):
        for tile in self.tiles:
            tile.remove_temp(path="data/temp")

    def upload_imgur(self, client):
        for tile in self.tiles:
            tile.upload_imgur(client)


    def process(self):
        base_url = 'https://yandex.ru/images/search?rpt=imageview&img_url='
        for tile in self.tiles:
            url = base_url + tile.link
            html = urllib2.urlopen(url).read()
            soup = BeautifulSoup(html, 'html.parser')
            
            imgs = soup.find_all('img')
            tile.similar_links = list()
            for img in imgs:
                try:
                    if 'similar__image' in img['class']:
                        similar_img = "https:"+str(img['src'])
                        tile.similar_links.append(similar_img)
                except KeyError:
                    print "no class here"
                    pass
            # print similar_imgs
            # tile.similar_links = similar_imgs
            print tile.similar_links
            tile.download_similar()
            tile.show_similar()

            break

    

    def random_red(self):
        pix_val = list(self.image.getdata())

        for tile in self.tiles:
            print tile.pixels[0]
            print tile.pixels[-1]
            if random.random() < 0.5:
                # tile.red()

                for pix in tile.pixels:
                    pix_val[pix] = (255,0,0)


        self.image.putdata(pix_val)













