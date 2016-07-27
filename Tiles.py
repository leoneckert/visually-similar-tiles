import PIL

class Tile:
    """docstring for Tile"""
    def __init__(self, image, xidx, yidx, idx):
        self.im = image
        self.xidx = xidx
        self.yidx = yidx
        self.idx = idx
        self.name = "tile_" + str(idx)

    def show(self):
        self.im.show()
        
  
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
