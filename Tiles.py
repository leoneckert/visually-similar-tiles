import PIL
import os
from bs4 import BeautifulSoup
import urllib2

class Tile:
    """docstring for Tile"""
    def __init__(self, image, xidx, yidx, idx):
        self.im = image
        self.xidx = xidx
        self.yidx = yidx
        self.idx = idx
        self.name = "tile_" + str(idx)
        
        self.path = None
        self.upload_data = None
        self.imgur_id = None
        self.link = None

    def show(self):
        self.im.show()

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



    # def delete_imgur(self, client):
    #     try:
    #         print client.delete_image(self.imgur_id)
    #         print "[+] DELETED", self.name, "FROM imgur with link", self.link, "and id", self.imgur_id
    #     except:
    #         pass
    #         print "[-] problems deleting", self.name, "FROM imgur with link", self.link, "and id", self.imgur_id
  
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
                y_pos = (y*self.tile_h)
                x_pos = (x*self.tile_w)                  
                tile = self.image.crop(( x_pos,y_pos, x_pos+self.tile_w,   y_pos+self.tile_h  ))
                tiles_out.append( Tile( tile, x, y, idx))
                idx += 1
        return tiles_out

    def open_all(self):
        for tile in self.tiles:
            tile.show()

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

    # def delete_imgur(self, client):
    #     for tile in self.tiles:
    #         tile.delete_imgur(client)

    def process(self):
        base_url = 'https://yandex.ru/images/search?rpt=imageview&img_url='
        for tile in self.tiles:
            url = base_url + tile.link
            html = urllib2.urlopen(url).read()
            soup = BeautifulSoup(html, 'html.parser')
            
            imgs = soup.find_all('img')
            similar_imgs = list()
            for img in imgs:
                try:
                    if 'similar__image' in img['class']:
                        similar_img = "https:"+str(img['src'])
                        similar_imgs.append(similar_img)
                except KeyError:
                    print "no class here"
                    pass
            print similar_imgs
            break









