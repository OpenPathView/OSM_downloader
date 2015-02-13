from . import tools, tile
from urllib.request import urlopen
from urllib.error import URLError
import pygame.image
import os
from math import floor, ceil

LAT_MAX = 85.0511
LAT_MIN = -85.0511
LAT_RANGE = LAT_MAX-LAT_MIN
LON_MIN = -180
LON_MAX = 180
LON_RANGE = LON_MAX-LON_MIN
TILE_WIDTH = 256
TILE_HEIGHT = 256


class Pyleaflet:
    """
    a pygame viewer to display osm map
    """

    def __init__(self, surface=None, sourceUrl = "http://c.tile.openstreetmap.org/{z}/{x}/{y}.png",cachePath="./cache/{z}/{x}/{y}.png",lat=48.390834,lon=-4.485556,zoomRange=[0,19]):
        """
        init map
        @param
            surface : a pygame surface on wich we will draw, if not given, a new window will be created
            sourceUrl : a formated url to download tile (ex : http://a.tile.openstreetmap.org/{z}/{x}/{y}.png)
            cachePath : a formated path to where we store tile
            lat : latitude of the map center
            lon : longitude of the map center
            zoomRange : a liste of two element : [min,max] zoom level of map
        """

        if surface:
            self.surface = surface
        else:
            self.surface=pygame.display.set_mode((1024,780), pygame.DOUBLEBUF)

        self.cachePath=cachePath
        self._zoom = 2
        self.__zoomRange = zoomRange
        self.__totalMapWidth  = (2**self._zoom)*TILE_WIDTH
        self.__totalMapHeight  = (2**self._zoom)*TILE_HEIGHT
        

        self.sourceUrl=sourceUrl
        relOffsetX=(lon-LON_MIN)/LON_RANGE
        relOffsetY=1-((lat-LAT_MIN)/LAT_RANGE)
        self.__xPixOffset = relOffsetX * self.__totalMapWidth
        self.__yPixOffset = relOffsetY * self.__totalMapHeight
        self.__mapTiles = dict()
        for z in range(zoomRange[0],zoomRange[1]+1):
            self.__mapTiles[z]=dict()

    # TODO : add event loop to move/zoom/click/etc

    def updateDisplay(self):
        """
        update display
        """
        surfWidth, surfHeight = self.surface.get_size()

        x_min_pix = self.__xPixOffset-surfWidth
        x_max_pix = self.__xPixOffset+surfWidth
        y_min_pix = self.__yPixOffset-surfHeight
        y_max_pix = self.__yPixOffset+surfHeight

        x_min_disp = floor(x_min_pix/TILE_WIDTH)
        x_max_disp = ceil(x_max_pix/TILE_WIDTH)
        y_min_disp = floor(y_min_pix/TILE_HEIGHT)
        y_max_disp = ceil(y_max_pix/TILE_HEIGHT)

        for x in range(x_min_disp,x_max_disp):
            for y in range(y_min_disp,y_max_disp):
                self.loadTileXY(x,y)
                xPos = x*TILE_WIDTH+surfWidth/2-self.__xPixOffset
                yPos = y*TILE_HEIGHT+surfHeight/2-self.__yPixOffset
                if self.__mapTiles[self._zoom].get((x,y)):
                    self.__mapTiles[self._zoom][x,y].blit(self.surface,xPos,yPos)
                else:
                    self.surface.fill((0,0,0),(xPos,yPos,TILE_WIDTH,TILE_HEIGHT))
                    #fill a white rect
            pygame.display.flip()


        #TODO delete old useless tile

    def loadTileXY(self,x,y,z=None,force=False):
        """
        load the tile at x,y coordinate with zoom z
        """
        x%=(2**self._zoom)
        y%=(2**self._zoom)        
        z = z if z else self._zoom
        if self.__mapTiles[z].get((x,y)):   #check if we already have the tile
            if not force:                   #we may want to force the update
                return

        imgPath = self.cachePath.format(x=x,y=y,z=z)
        imgDir = os.path.dirname(imgPath)

        if not os.path.exists(imgDir): #check directory structure
            os.makedirs(imgDir)

        if not os.path.exists(imgPath):    #if we haven't already downloaded the image
            print("Download z={z},x={x},y={y}".format(z=z,x=x,y=y))
            try:
                response = urlopen(self.sourceUrl.format(x=x,y=y,z=z))   #load online file
                img = response.read()
            except (URLError) as e:
                print(e)
                img = None
            else:                                           #save loaded image in cache
                with open(imgPath,"wb") as imgFD:
                    imgFD.write(img)
        if os.path.exists(imgPath):
            pic = pygame.image.load(imgPath)
            self.__mapTiles[z][x,y]=tile.Tile(x,y,z,pic)

    def unloadTileXY(self,x,y,z=None,force=False):
        """
        unload unused tile
        """
        zoom = z if z else self._zoom
        del(self.__mapTiles[z][x,y])

    def loadTileLatLon(self,lat,lon,z=None):
        """
        load the tile at lat,lon coordinate with zoom z
        """
        zoom = z if z else self._zoom
        x,y = tools.deg2num(lat, lon, zoom)
        return self.loadTileXY(x,y,zoom)

    #TODO : add code to convert pixel offset and zoom to lat and lon
    # @property
    # def lat(self):
    #     return self._lat
    # @lat.setter
    # def lat(self, value):
    #     self._lat = value
    #     self.updateDisplay()

    # @property
    # def lon(self):
    #     return self._lon
    # @lon.setter
    # def lon(self, value):
    #     self._lon = value
    #     self.updateDisplay()

    def addX(self,dx):
        """
        move the map of dx
        """
        self.__xPixOffset+=dx

    def addY(self,dy):
        """
        move the map of dy
        """
        self.__yPixOffset+=dy

    def zoomIn(self):
        """
        zoom in
        """
        if self._zoom+1<=max(self.__zoomRange):
            self.zoom=self.zoom+1

    def zoomOut(self):
        """
        zoom out
        """
        if self._zoom-1>=min(self.__zoomRange):
            self.zoom=self.zoom-1

    @property
    def zoom(self):
        return self._zoom
    @zoom.setter
    def zoom(self, value):
        self._zoom = value
        # (2**zoom)x(2**zoom) tiles
        
        relOffsetX=self.__xPixOffset/self.__totalMapWidth
        relOffsetY=self.__yPixOffset/self.__totalMapHeight

        self.__totalMapWidth  = (2**self._zoom)*TILE_WIDTH
        self.__totalMapHeight  = (2**self._zoom)*TILE_HEIGHT
        
        self.__xPixOffset = relOffsetX * self.__totalMapWidth
        self.__yPixOffset = relOffsetY * self.__totalMapHeight

        self.updateDisplay()