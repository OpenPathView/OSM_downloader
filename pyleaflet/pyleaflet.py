from . import tools, tiles
from urllib.request import urlopen
from urllib.error import URLError
import os
import math
from math import floor, ceil, log, tan, cos, radians, pi
import pygame

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

    def __init__(self, surface=None,lat=48.390834,lon=-4.485556,zoomRange=[0,19]):
        """
        init map
        @param
            surface : a pygame surface on wich we will draw, if not given, a new window will be created
            lat : latitude of the map center
            lon : longitude of the map center
            zoomRange : a liste of two element : [min,max] zoom level of map
        """

        if surface:
            self.surface = surface
        else:
            self.surface=pygame.display.set_mode((1024,780), pygame.DOUBLEBUF)

        self._zoom = 2
        self.__zoomRange = zoomRange
        self.__totalMapWidth  = (2**self._zoom)*TILE_WIDTH
        self.__totalMapHeight  = (2**self._zoom)*TILE_HEIGHT
        
        relOffsetX, relOffsetY =  tools.deg2rel(lat,lon)

        self.__xPixOffset = relOffsetX * self.__totalMapWidth
        self.__yPixOffset = relOffsetY * self.__totalMapHeight
        self.__mapTiles = tiles.Tiles()

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
                #self.__mapTiles.loadTileXY(x,y,self._zoom)
                xPos = x*TILE_WIDTH+surfWidth/2-self.__xPixOffset
                yPos = y*TILE_HEIGHT+surfHeight/2-self.__yPixOffset
                if not self.__mapTiles.blit(self._zoom,x,y,self.surface,xPos,yPos):
                    self.surface.fill((0,0,0),(xPos,yPos,TILE_WIDTH,TILE_HEIGHT)) #fill a white rect
        pygame.display.flip()


        #TODO delete old useless tile

    def unloadTile(self):
        """
        unload unused tile
        """
        # TODO : everything to unload tiles
        pass

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