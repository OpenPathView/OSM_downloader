from .pyleaflet import Pyleaflet
from . import tiles
import pygame
import os
import threading, multiprocessing


class Wrapper (multiprocessing.Process): 
    """
    a class containing a subprocess
    """
    def __init__(self,*args,**kwarg):
        """
        init stuff
        """
        multiprocessing.Process.__init__(self,*args,**kwarg)
        self.daemon = True


    def run(self):
        """
        a process displaying the PyLeaflet, configurable via pipe
        """

        self.surface=pygame.display.set_mode((1024,780), pygame.DOUBLEBUF|pygame.RESIZABLE) #init map display
        pyleaflet = Pyleaflet(self.surface)
        pyleaflet.updateDisplay()

        pygame.event.set_allowed(None)                                                      #select wich event are allowed
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, tiles.UPDATE_DISPLAY_EVENT, pygame.VIDEORESIZE])

        self.communicationThread = threading.Thread(target=self.__comThread,daemon=True)    #start the communication thread
        self.communicationThread.start()

        while 1:
            event = pygame.event.wait()         #wait for an event, it can be classical pygame event or custom map control event
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEMOTION:  #move the map
                if event.buttons[0]:
                    dx,dy = event.rel
                    for e in pygame.event.get(pygame.MOUSEMOTION):  #we sum all mouse mouvement to prevent excessive display update
                        if e.buttons[0]:
                            tdx,tdy = event.rel
                            dx += tdx
                            dy += tdy
                    pyleaflet.addX(-dx)
                    pyleaflet.addY(-dy)
                    pyleaflet.updateDisplay()
            elif event.type == pygame.MOUSEBUTTONUP:    #zoom
                if event.button==4:
                    pyleaflet.zoomIn()
                elif event.button==5:
                    pyleaflet.zoomOut()
            elif event.type == tiles.UPDATE_DISPLAY_EVENT:    #something append which might want the display to be updated
                pyleaflet.updateDisplay()
            elif event.type == pygame.VIDEORESIZE:            #user resized the window
                surface=pygame.display.set_mode(event.size, pygame.DOUBLEBUF|pygame.RESIZABLE)
                pyleaflet.surface = surface
                pyleaflet.updateDisplay()

    def __comThread(self):
        """
        a mathode run in a separated thread to receive inter-process communication
        """
        pass