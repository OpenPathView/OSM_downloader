import pygame.image
import pygame
import threading
import queue
import sys, os
import socket
from urllib.request import urlopen
from urllib.error import URLError
from . import tile

CACHE_PATH  = "./cache/{z}/{x}/{y}.png"
SOURCE_URL = "http://c.tile.openstreetmap.org/{z}/{x}/{y}.png"
ZOOM_MIN = 0
ZOOM_MAX = 19
UPDATE_DISPLAY_EVEN = pygame.USEREVENT
MAX_DL_LEN = 32

class Tiles(threading.Thread):
    """
    define a set of tiles which together are a complete map
    """

    def __init__(self):
        """
        init all
        """
        threading.Thread.__init__(self)
        self.daemon=True
        self.__tiles = dict()       #access to __tiles is private becaus of the use of mutex
        for z in range(ZOOM_MIN,ZOOM_MAX+1):
            self.__tiles[z]=dict()
        self.__tilesLock = threading.Lock()
        self.__toDownload = set()   #use a set to prevent useless multiple entry
        self.__toDownloadCondition = threading.Condition()
        self.start()    #start download thread

    def run(self):
        """
        methode called on a separated thread
        download asked tiles
        """
        while True:
            self.__toDownloadCondition.acquire()
            if not self.__toDownload:       #check if there realy is something to download
                self.__toDownloadCondition.wait()   #wait for something to append            
            x,y,z = self.__toDownload.pop() #get a tile we want to download
            self.__toDownloadCondition.release()

            if not self.__tiles[z].get((x,y)):  #check if we don't already have the tile
                self.__dowloadTileXY(x,y,z)


    def __dowloadTileXY(self,x,y,zoom):
        """
        download the given tile (in a thread)
        """
        nbrTiles = 2**zoom
        x%=nbrTiles
        y%=nbrTiles

        imgPath = CACHE_PATH.format(x=x,y=y,z=zoom)
        imgFolder = os.path.dirname(imgPath)
        if not os.path.isdir(imgFolder):
            os.makedirs(imgFolder)
        try:
            response = urlopen(SOURCE_URL.format(x=x,y=y,z=zoom),timeout=0.5)   #load online file
            img = response.read()
        except (URLError, socket.timeout) as e:
            print(e,file=sys.stderr)
            self.addTileRequest(x,y,zoom)
        else:                                           #save loaded image in cache
            with open(imgPath,"wb") as imgFD:   #save image
                imgFD.write(img)
            self.loadTileFromFile(x,y,zoom,imgPath)
        
        try:
            evt = pygame.event.Event(UPDATE_DISPLAY_EVEN)
            pygame.event.post(evt)
        except (pygame.error) as e:
            print(e,file=sys.stderr)            

    def loadTileFromFile(self,x,y,zoom,imgPath):
        """
        load a Tile from a file
        @return:   
            1 if succes
            0 if fail
        """
        with self.__tilesLock:
            try:
                pic = pygame.image.load(imgPath).convert()
            except(pygame.error) as e:
                print(e,file=sys.stderr)
                print(imgPath,file=sys.stderr)
                return 0
            self.__tiles[zoom][x,y]=tile.Tile(x,y,zoom,pic)
            return 1


    def addTileRequest(self,x,y,zoom):
        """
        add a tile request in the __toDownload set
        """
        with self.__toDownloadCondition:         #if we fail to download the tile, we want to try
            if len(self.__toDownload)<=MAX_DL_LEN:
                self.__toDownload.add((x,y,zoom))
                self.__toDownloadCondition.notify()


    def loadTileXY(self,x,y,zoom):
        """
        load the tile at x,y coordinate with given zoom
        @return:   
            1 if succes
            0 if fail
        """
        nbrTiles = 2**zoom
        x%=nbrTiles
        y%=nbrTiles

        imgPath = CACHE_PATH.format(x=x,y=y,z=zoom)
        imgDir = os.path.dirname(imgPath)

        if not os.path.exists(imgDir): #check directory structure
            os.makedirs(imgDir)

        if not os.path.exists(imgPath):    #if we haven't already downloaded the image
            self.addTileRequest(x,y,zoom)
            return 0
        else:
            return self.loadTileFromFile(x,y,zoom,imgPath)

    def unloadTileXY(self,x,y,zoom,force=False):
        """
        unload unused tile
        """
        with self.__tilesLock:
            del(self.__mapTiles[zoom][x,y])

    def loadTileLatLon(self,lat,lon,zoom):
        """
        load the tile at lat,lon coordinate with given zoom
        @return:   
            1 if succes
            0 if fail
        """
        x,y = tools.deg2num(lat, lon, zoom)
        return self.loadTileXY(x,y,zoom)

    def blit(self,z,x,y,dest,xPos,yPos):
        """
        blit the selected tile on dest
        """
        nbrTiles = 2**z
        x%=nbrTiles
        y%=nbrTiles
        with self.__tilesLock:
            if self.__tiles[z].get((x,y)):
                self.__tiles[z].get((x,y)).blit(dest,xPos,yPos)
                return 1
        if self.loadTileXY(x,y,z):
            self.__tiles[z].get((x,y)).blit(dest,xPos,yPos)
            return 1
        return 0