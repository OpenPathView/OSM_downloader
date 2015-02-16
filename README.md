# PyLeaflet

## What is it ?

PyLeaflet is a PyGame based Python version of Leaflet, an OSM map reader. PyLeaflet is a desktop application which aim to be used by other desktop application for map stuff

## What can it do ?

For now, not much, but when it will be finished, it  should allow users to :
  * Download part of a map for offline use
  * Move the map to given coordinate
  * Add series of coordinate to draw a path
  * Lot of other fun thing I don't have in mind yet

## How to install it ?

For now, the ony dependenci is PyGame, so here is how to install it :

For Ubuntu
```bash
sudo apt-get install mercurial python3-dev python3-numpy \
    libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev \
    libsdl1.2-dev  libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev

hg clone https://bitbucket.org/pygame/pygame

cd pygame
python3 setup.py build
sudo python3 setup.py install    
```

For Windows:
Download the installer on [PyGame WebSite](http://pygame.org/download.shtml) (be carefull to take the installer for python3)


## How to use it ?
