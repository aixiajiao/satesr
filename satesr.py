import sys
from sate_api.bing_aerial import AerialImageRetrieval
from realesrgan.super_resolution import REenhance as RE



def satesr(
    lat: float = 86,
    lon: float = 181,
    radius: float = None,
    maxlevel: int = 20,
    path: str='demo/aerial_imgs',
    label: bool=False,
    enhance: bool=False,
    mode: int=1,
    scale: float = 4,
    tile: int = 0):
    
    input=path
    output = path + "_enhanced"
    
    if lat < 85.05112878 and lat > -85.05112878 and lon < 180 and lon > -180:
        try: 
            AerialImageRetrieval(lat=lat,lon=lon,radius=radius,maxlevel=maxlevel,maxsize=True,road_label=label,path=input).max_resolution_imagery_retrieval()
        except:
            raise 
    else:
        print('No valid coordinates, SR only')
    if enhance == True:
        try:
            RE(input,output,mode,scale,'enhanced',tile,10,0,'auto')
        except:
            raise







    

