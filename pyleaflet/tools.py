import math
from math import radians, log, tan, cos, pi, atan, sinh, degrees

def deg2num(lat_deg, lon_deg, zoom):
    """
    translate degree coordinate to tile id
    """
    lat_rad = radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - log(tan(lat_rad) + (1 / cos(lat_rad))) / pi) / 2.0 * n)
    return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
    """
    translate tile id to degree coordinate
    """
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = atan(sinh(pi * (1 - 2 * ytile / n)))
    lat_deg = degrees(lat_rad)
    return (lat_deg, lon_deg)

def deg2rel(lat_deg, lon_deg):
    """
    translate degree coordinate to relative position on global map
    """
    lat_rad = radians(lat_deg)
    xrel = (lon_deg + 180.0) / 360.0
    yrel = (1.0 - log(tan(lat_rad) + (1 / cos(lat_rad))) / pi) / 2.0
    return (xrel, yrel)

def rel2deg(xrel, yrel):
    """
    translate relative position on global map to degree coordinate
    """
    lon_deg = xrel * 360.0 - 180.0
    lat_rad = atan(sinh(pi * (1 - 2 * yrel)))
    lat_deg = degrees(lat_rad)
    return (lat_deg, lon_deg)