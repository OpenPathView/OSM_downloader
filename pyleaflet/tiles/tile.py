class Tile():
    """
    define a tile, with image and coordinate
    """

    def __init__(self,x,y,z,img):
        """
        init all
        @params:
            x: x coordinate, as tile
            y: y coordinate, as tile
            z: zoom
            img: tile picture, as a pygame surface
        """
        self.x = x
        self.y = y
        self.z = z
        
        self.pic = img

    def blit(self,dest,xPos,yPos):
        """
        blit the tile picture on destination
        @params:
            dest: pygame surface to use as destination
            xPos: x position on dest
            yPos: y position on dest
        """
        dest.blit(self.pic, (int(xPos),int(yPos)))
        