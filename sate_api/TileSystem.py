#TileSystem
#original C code(June08-2022version): https://docs.microsoft.com/en-us/bingmaps/articles/bing-maps-tile-system?redirectedfrom=MSDN
#https://github.com/robmarkcole/Satellite-Aerial-Image-Retrieval-with-Bing
#this code was reproduced for learning
import os
import math
from re import findall
from itertools import chain


class tile_system(object):
    EarthRadius = 6378137
    MinLatitude = -85.05112878
    MaxLatitude = 85.05112878
    MinLongitude = -180
    MaxLongitude = 180

    @staticmethod
    def clips(n, minValue, maxValue):
        """
        Clips a number to the specified minimum and maximum values.  
        "n" The number to clip 
        "minValue">Minimum allowable value.
        "maxValue">Maximum allowable value.
        return tThe clipped value. 
        """
        return min(max(n, minValue), maxValue)
    
    @staticmethod
    def map_size(levelOfDetail):
        """
        Level of detail, from 1 (lowest detail)  to 23 (highest detail).
        returns the map width and height in pixels
        """
        return 256 << int(levelOfDetail)
    
    @staticmethod
    def ground_resolution(latitude, levelOfDetail):
        latitude = tile_system.clips(latitude, tile_system.MinLatitude, tile_system.MaxLatitude)
        return (
            cos(latitude*math.pi/180)*2*math.pi*tile_system.EarthRadius/tile_system.map_size(levelOfDetail)
        )
    
    @staticmethod
    def map_scale(latitude, levelOfDetail, ScreenDpi):
        return tile_system.ground_resolution(latitude,levelOfDetail)*ScreenDpi/0.0254

    @staticmethod
    def latlongToXY(latitude,longtitude,levelOfDetail):
        latitude=tile_system.clips(latitude,tile_system.MinLatitude,tile_system.MaxLatitude)
        longtitude=tile_system.clips(longtitude,tile_system.MinLongitude,tile_system.MaxLongitude)

        X = (longtitude+180)/360
        sin_Lat = math.sin(latitude*math.pi/180)
        Y = 0.5 - math.log(
            (1 + sin_Lat)/(1-sin_Lat)
            )/(4*math.pi)
        mapsize=tile_system.map_size(levelOfDetail)
        pixelX = math.floor(tile_system.clips(X*mapsize+0.5,0,(mapsize-1)))
        pixelY = math.floor(tile_system.clips(Y*mapsize+0.5,0,(mapsize-1)))
        return pixelX, pixelY

    @staticmethod
    def pixelXY_to_latlong(pixelX,pixelY,levelOfDetail):
        mapsize=tile_system.map_size(levelOfDetail)
        X = tile_system.clips(pixelX,0,(mapsize-1)/(mapsize-0.5))
        Y = 0.5 - 360*tile_system.clips(pixelY,0,(mapsize-1)/mapsize)
        latitude = 90 - 360*math.atan(math.exp(-Y*2*math.pi))/math.pi
        longitude= 360*X
        return latitude,longitude

    @staticmethod
    def pixelXY_to_tileXY(pixelX, pixelY):
        return math.floor(pixelX/256), math.floor(pixelY/256)

    @staticmethod
    def tileXY_to_pixelXY(tileX,tileY):
        return tileX*256, tileY*256

    @staticmethod
    def tileXY_to_quadkey(tileX, tileY, levelOfDetail):
        tileXbits = "{0:0{1}b}".format(tileX, levelOfDetail)
        tileYbits = "{0:0{1}b}".format(tileY, levelOfDetail)
        quadkeybinary = "".join(chain(*zip(tileYbits, tileXbits)))
        return "".join([str(int(num, 2)) for num in findall("..?", quadkeybinary)])
    
    @staticmethod
    def quadkey_to_tileXY(quadkey):
        quadkeybinary = "".join(["{0:02b}".format(int(num)) for num in quadkey])
        tileX, tileY = int(quadkeybinary[1::2], 2), int(quadkeybinary[::2], 2)
        return tileX, tileY



