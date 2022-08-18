"""
Scripts to download bing aerial image
Credit to Linlin Chen(https://github.com/llgeek/Satellite-Aerial-Image-Retrieval) for the base code
"""

import os
from urllib import request
from PIL import Image
import time
from tqdm import tqdm

from sate_api.TileSystem import tile_system
from sate_api.BoundingBox import boundingbox 

TILESIZE = 256  # in Bing tile system, one tile image is in size 256 * 256 pixels

class AerialImageRetrieval(object):
    def __init__(self, lat, lon, radius, maxlevel,maxsize,road_label,path):
        self.lat = lat
        self.lon = lon
        self.radius = radius
        self.maxlevel = maxlevel
        self.maxsize = maxsize
        self.label=road_label
        self.upper_left = boundingbox(self.lat, self.lon, self.radius)[0]
        self.lower_right = boundingbox(self.lat, self.lon, self.radius)[1]

        self.tgtfolder = path

        if self.maxsize:
            self.IMAGEMAXSIZE = 8192 * 8192 * 8  # max width/height in pixels for the retrived image
        else:
            self.IMAGEMAXSIZE = 8192 * 8192 * 100
        
        if self.label:
            self.BASEURL = 'http://h0.ortho.tiles.virtualearth.net/tiles/h{0}.jpeg?g=131'
        else:
            self.BASEURL = 'http://ecn.t3.tiles.virtualearth.net/tiles/a{0}.jpeg?g=6358' #no label
        try:
            os.makedirs(self.tgtfolder)
        except FileExistsError:
            pass
        except OSError:
            raise

    def download_image(self, quadkey):
        with request.urlopen(self.BASEURL.format(quadkey)) as file:
            return Image.open(file)

    def is_valid_image(self, image):

        if not os.path.exists("sate_api/null.png"):
            nullimg = self.download_image(
                "11111111111111111111"
            )  # an invalid quadkey which will download a null jpeg from Bing tile system
            nullimg.save("sate_api/null.png")
        return not (image == Image.open("sate_api/null.png"))

    def max_resolution_imagery_retrieval(self):

        for levl in range(self.maxlevel, 0, -1):
            pixelX1, pixelY1 = tile_system.latlongToXY(self.upper_left[0], self.upper_left[1], levl)
            pixelX2, pixelY2 = tile_system.latlongToXY(self.lower_right[0], self.lower_right[1], levl)

            pixelX1, pixelX2 = min(pixelX1, pixelX2), max(pixelX1, pixelX2)
            pixelY1, pixelY2 = min(pixelY1, pixelY2), max(pixelY1, pixelY2)

            if abs(pixelX1 - pixelX2) * abs(pixelY1 - pixelY2) > self.IMAGEMAXSIZE:
                #print("Image at level {} exceeds the maximum image size 8192*8192*8, will SKIP".format(levl))
                continue

            tileX1, tileY1 = tile_system.pixelXY_to_tileXY(pixelX1, pixelY1)
            tileX2, tileY2 = tile_system.pixelXY_to_tileXY(pixelX2, pixelY2)

            # Stitch the tile images together
            result = Image.new(
                "RGB",
                ((tileX2 - tileX1 + 1) * TILESIZE, (tileY2 - tileY1 + 1) * TILESIZE),
            )
            retrieve_sucess = False
            for tileY in tqdm(range(tileY1, tileY2 + 1)):
                (
                    retrieve_sucess,
                    horizontal_image,
                ) = self.horizontal_retrieval_and_stitch_image(
                    tileX1, tileX2, tileY, levl
                )
                if not retrieve_sucess:
                    break
                result.paste(horizontal_image, (0, (tileY - tileY1) * TILESIZE))

            if not retrieve_sucess:
                continue

            # Crop the image based on the given bounding box
            leftup_cornerX, leftup_cornerY = tile_system.tileXY_to_pixelXY(
                tileX1, tileY1
            )
            retrieve_image = result.crop(
                (
                    pixelX1 - leftup_cornerX,
                    pixelY1 - leftup_cornerY,
                    pixelX2 - leftup_cornerX,
                    pixelY2 - leftup_cornerY,
                )
            )
            print(
                "Find the aerial image at level {}, saved as aerialimg{}-{}_lv{}_{}.jpeg in folder {}".format(
                    levl,self.lat,self.lon,levl,time.strftime("%m%d-%H%M"),self.tgtfolder
                )
            )
            filename = os.path.join(self.tgtfolder, "aerialimg{}-{}_lv{}_{}.jpeg".format(self.lat,self.lon,levl,time.strftime("%m%d-%H%M")))
            retrieve_image.save(filename)
            return True
        return False

    def horizontal_retrieval_and_stitch_image(
        self, tileX_start, tileX_end, tileY, level):
        imagelist = []
        for tileX in range(tileX_start, tileX_end + 1):
            quadkey = tile_system.tileXY_to_quadkey(tileX, tileY, level)
            image = self.download_image(quadkey)
            if self.is_valid_image(image):
                imagelist.append(image)
            else:
                pass
                #print("No tile image at level {0} for tile coordinate ({1}, {2})".format(level, tileX, tileY))
                return False, None
        result = Image.new("RGB", (len(imagelist) * TILESIZE, TILESIZE))
        for i, image in enumerate(imagelist):
            result.paste(image, (i * TILESIZE, 0))
        return True, result
    