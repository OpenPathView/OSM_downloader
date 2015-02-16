from pyleaflet import Pyleaflet
import pygame
import os

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

surface=pygame.display.set_mode((1024,780), pygame.DOUBLEBUF|pygame.RESIZABLE)
pyleaflet = Pyleaflet(surface)
pyleaflet.updateDisplay()

pygame.event.set_allowed(None)
pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.USEREVENT, pygame.VIDEORESIZE])

while 1:

    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        exit()
    elif event.type == pygame.MOUSEMOTION:
        if event.buttons[0]:
            dx,dy = event.rel
            pyleaflet.addX(-dx)
            pyleaflet.addY(-dy)
            pyleaflet.updateDisplay()
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button==4:
            pyleaflet.zoomIn()
        elif event.button==5:
            pyleaflet.zoomOut()
    elif event.type == pygame.USEREVENT:
        pyleaflet.updateDisplay()
    elif event.type == pygame.VIDEORESIZE:
        surface=pygame.display.set_mode(event.size, pygame.DOUBLEBUF|pygame.RESIZABLE)
        pyleaflet.surface = surface
        pyleaflet.updateDisplay()
