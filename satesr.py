import sys
from realesrgan.super_resolution import REenhance as RE
from sate_api.bing_aerial import download_aerial_imgs as DAI


def satesr(
    lat: float = 86,
    lon: float = 181,
    radius: float = None,
    maxlevel: int = 20,
    path: str=None,
    label: bool=False,
    enhance: bool=False,
    mode: int=1,
    scale: float = 4,
    tile: int = 0):
    input=path
    output = path + "_enhanced"
    
    if lat < 85.05112878 and lat > -85.05112878 and lon < 180 and lon > -180:
        try: 
            DAI(lat=lat,lon=lon,radius=radius,maxlevel=maxlevel,maxsize=True,road_label=label,path=input)
        except:
            raise ValueError('Check input values')
    else:
        print('No valid coordinates, SR only')
    if enhance == True:
        try:
            RE(input,output,mode,scale,'enhanved',tile,10,0,'auto')
        except:
            raise

    
    

        






    

