from .pyleaflet import Pyleaflet
from . import tiles, action, event
import pygame
import os
import threading, multiprocessing, queue

class TooManyAction(Exception):
    """
    Exception raised when you try to add action in action queue while the queue is full
    """

    def __init__(self, desc):
        self.desc = desc

    def __str__(self):
        return self.desc

class Wrapper (multiprocessing.Process): 
    """
    a class containing a subprocess
    """
    def __init__(self,*args,**kwarg):
        """
        init the multiprocessing layer
        @params
            every parameters we want to pass to Process
        """
        
        self.__actionQueue = multiprocessing.Queue(128) #queue to send action to the subprocess
        self.__eventQueue =  multiprocessing.Queue(128) #queue to receive event from the subprocess

        multiprocessing.Process.__init__(self,*args,**kwarg)
        self.daemon = True

    def poolEvent(self):
        """
        return an single event, if no event are in queue, return a NOEVENT event
        """
        try:
            retrievedEvent = self.__eventQueue.get_nowait()
            return retrievedEvent
        except (queue.Empty) as e:
            return event.Event()    #NOEVENT event

    def waitEvent(self,timeout=None):
        """
        wait for an event, if timeout is given, return NOEVENT event after timeout if no event appear
        @params
            timeout : time to wait for an event before a NOEVENT event is returned
        """
        try:
            retrievedEvent = self.__eventQueue.get(timeout=timeout)
            return retrievedEvent
        except (queue.Empty) as e:
            return event.Event()    #NOEVENT event

    def putAction(self,action,timeout=None):
        """
        send an action request to the PyLeaflet process
        the action queue has a max size of 128 actions, trying to add action when queue is full will raise a TooManyAction exception
        unknown action won't do anything
        @params
            action : the action to be sent
            timeout : an optional timeout, in case the queue is full, wait for timeout before raising a TooManyAction exception
        """
        assert type(action) is action.Action
        try:
            self.__actionQueue.put(action,timeout=timeout)
        except (queue.Full) as e:
            raise TooManyAction("Action queue full")


    def run(self):
        """
        a process displaying the PyLeaflet, configurable via pipe
        """

        self.surface=pygame.display.set_mode((1024,780), pygame.DOUBLEBUF|pygame.RESIZABLE) #init map display
        pyleaflet = Pyleaflet(self.surface)
        pyleaflet.updateDisplay()

        pygame.event.set_allowed(None)                                                      #select wich event are allowed
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN,
            tiles.UPDATE_DISPLAY_EVENT, pygame.VIDEORESIZE,
            pygame.KEYDOWN, pygame.KEYUP])
        self.communicationThread = threading.Thread(target=self.__comThread,daemon=True)    #start the communication thread
        self.communicationThread.start()

        while 1:
            pgEvent = pygame.event.wait()         #wait for an event, it can be classical pygame event or custom map control event
            if pgEvent.type == pygame.QUIT:
                self.__addEvent(event.Event(event.QUIT))
                exit()
            elif pgEvent.type == pygame.MOUSEMOTION:  #move the map
                dx,dy = pgEvent.rel
                for e in pygame.event.get(pygame.MOUSEMOTION):  #we sum all mouse mouvement to prevent excessive display update
                    if e.buttons[0]:
                        tdx,tdy = pgEvent.rel
                        dx += tdx
                        dy += tdy
                if pgEvent.buttons[0]:
                    pyleaflet.addX(-dx)
                    pyleaflet.addY(-dy)
                    pyleaflet.updateDisplay()
                self.__addEvent(event.Event(event.MOUSEMOTION, pos=pgEvent.pos, button=pgEvent.buttons, rel=[dx,dy], center=pyleaflet.getCenterCoordinate(),visible=pyleaflet.getDisplayedCoordinate()))
            elif pgEvent.type == pygame.MOUSEBUTTONUP:    #zoom
                self.__addEvent(event.Event(event.MOUSEBUTTONUP, pos=pgEvent.pos, button=pgEvent.button, center=pyleaflet.getCenterCoordinate(),visible=pyleaflet.getDisplayedCoordinate()))
                if pgEvent.button==4:
                    pyleaflet.zoomIn()
                elif pgEvent.button==5:
                    pyleaflet.zoomOut()
            elif pgEvent.type == pygame.MOUSEBUTTONDOWN:
                self.__addEvent(event.Event(event.MOUSEBUTTONDOWN, pos=pgEvent.pos, button=pgEvent.button, center=pyleaflet.getCenterCoordinate(),visible=pyleaflet.getDisplayedCoordinate()))
            elif pgEvent.type == pygame.KEYDOWN:
                self.__addEvent(event.Event(event.KEYDOWN, unicode = pgEvent.unicode, key=pgEvent.key, mod=pgEvent.mod, center=pyleaflet.getCenterCoordinate(),visible=pyleaflet.getDisplayedCoordinate()))
            elif pgEvent.type == pygame.KEYUP:
                self.__addEvent(event.Event(event.KEYUP, key=pgEvent.key, mod=pgEvent.mod, center=pyleaflet.getCenterCoordinate(),visible=pyleaflet.getDisplayedCoordinate()))
            elif pgEvent.type == tiles.UPDATE_DISPLAY_EVENT:    #something append which might want the display to be updated
                pyleaflet.updateDisplay()
            elif pgEvent.type == pygame.VIDEORESIZE:            #user resized the window
                surface=pygame.display.set_mode(pgEvent.size, pygame.DOUBLEBUF|pygame.RESIZABLE)
                pyleaflet.surface = surface
                pyleaflet.updateDisplay()

    def __addEvent(self,event):
        """
        add an event in the event queue
        return True if the event is added, False in case of error
        """
        try:
            self.__eventQueue.put(event)
            return True
        except (queue.Full) as e:
            print(e,file=sys.stderr)
            return False

    def __comThread(self):
        """
        a mathode run in a separated thread to receive inter-process communication
        """
        while True:
            action = self.__actionQueue.get()
            pass

    # TODO : Add some communication protocole
    #        Add some action protocole (add marker, add path, move to some point)
    #        Add some event protocole (key pressed, mouse clique, etc)