from pyleaflet import Pyleaflet
import pygame

surface=pygame.display.set_mode((1024,780), pygame.DOUBLEBUF)
pyleaflet = Pyleaflet(surface)
pyleaflet.updateDisplay()


while 1:

    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        exit()
    elif event.type == pygame.MOUSEMOTION:
        # print(event.buttons)
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