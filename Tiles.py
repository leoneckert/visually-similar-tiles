import cv2

class Tile:
    """docstring for Tile"""
    def __init__(self, image, xidx, yidx, idx):
        self.im = image
        self.xidx = xidx
        self.yidx = yidx
        self.idx = idx
        self.name = "tile_" + str(idx)

    def show(self):
        cv2.imshow(self.name, self.im)
        
  
class Tiles(object):
    """docstring for Tiles"""
    def __init__(self, image, columns, rows):
        self.columns = columns
        self.rows = rows
        self.image = image
        self.image_w = image.shape[1]
        self.image_h = image.shape[0]
        self.tile_w = self.image_w/columns
        self.tile_h = self.image_h/rows
        self.tiles = self.init_tiles()

    def init_tiles(self):
        tiles_out = list()
        idx = 0
        for y in range(self.rows):
            for x in range(self.columns):
                temp_img = self.image.copy()    
                y_pos = (y*self.tile_h)
                x_pos = (x*self.tile_w)
                im = temp_img[y_pos:y_pos+self.tile_h, x_pos:x_pos+self.tile_w]
                tiles_out.append( Tile( im, x, y, idx))
                idx += 1
        return tiles_out

    def open_all(self):
        for tile in self.tiles:
            tile.show()
