import os, shutil, time
import tkinter
import tkinter.filedialog as tkfiledialog
from urllib.request import urlopen
from urllib.error import URLError


tkRoot = tkinter.Tk()
tkRoot.withdraw()

import pygame

from pyleaflet import Wrapper
from pyleaflet import event
from pyleaflet.tiles import tiles
from pyleaflet import tools

leafletWrapper = Wrapper()
leafletWrapper.start()
while 1:
    e = leafletWrapper.waitEvent()

    if e.eventId==event.QUIT:
        exit()

    if e.eventId==event.KEYUP:
        if e.key == pygame.K_d:
            pathToSave = tkfiledialog.askdirectory(title="Choose a folder to save tiles")
            if pathToSave:

                newPid = os.fork()
                if newPid==0:
                    #here we are in a child process, we download data then quit
                    if not os.path.exists(pathToSave):
                        os.makedirs(pathToSave)

                    latTop = e.visible["latTop"]
                    lonRight = e.visible["lonRight"]
                    latBottom = e.visible["latBottom"]
                    lonLeft = e.visible["lonLeft"]

                    for zoom in range(tiles.ZOOM_MIN,tiles.ZOOM_MAX+1):
                        x_min, y_min = tools.deg2num(latTop,lonLeft,zoom)
                        x_max, y_max = tools.deg2num(latBottom,lonRight,zoom)
                        
                        for x in range(x_min,x_max+1):
                            for y in range(y_min,y_max+1):
                                time.sleep(0.5)
                                nbrTiles = 2**zoom
                                x%=nbrTiles
                                y%=nbrTiles
                                if not os.path.exists(os.path.join(pathToSave,"{z}/{x}/".format(z=zoom,x=x))):
                                    os.makedirs(os.path.join(pathToSave,"{z}/{x}/".format(z=zoom,x=x)))
                                imgPath = tiles.CACHE_PATH.format(x=x,y=y,z=zoom)
                                imgFolder = os.path.dirname(imgPath)
                                if os.path.isfile(imgPath):
                                    shutil.copy(imgPath,os.path.join(pathToSave,"{z}/{x}/{y}.png".format(z=zoom,x=x,y=y)))
                                else:
                                    try:
                                        response = urlopen(tiles.SOURCE_URL.format(x=x,y=y,z=zoom),timeout=0.5)   #load online file
                                        img = response.read()
                                    except (URLError, socket.timeout) as e:
                                        print(e,file=sys.stderr)
                                        print("Error downloading tile \{x,y,z\}=\{{x},{y},{z}\}".format(x=x,y=y,z=zoom))
                                    else:                                           #save loaded image in cache
                                        with open(imgPath,"wb") as imgFD:   #save image
                                            imgFD.write(img)
                    print("Download done \o/")
                    os._exit(0)
                    
            else:
                print("Download cancelled")
            
            