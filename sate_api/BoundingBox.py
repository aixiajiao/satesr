'''
credit to Jan Philip Matuschek (http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates)

'''
import math
def boundingbox(lat, lon, arc=100):    
    r = 6378.137 # radius of earth in km: (), same with Bing API
    arckm = arc/1000
    # convert coordinates to Radians
    lat_rad = lat * math.pi / 180
    lon_rad = lon * math.pi / 180
    # angular distance in radians on a great circle
    dist_rad = arckm / r
        
    SE_lat = lat_rad - dist_rad
    NW_lat = lat_rad + dist_rad
    
    delta_lon = math.asin(math.sin(dist_rad) / math.cos(lat_rad))
    SE_lon = lon_rad + delta_lon
    NW_lon = lon_rad - delta_lon
    
    

    deg_NW_lat = math.degrees(NW_lat)
    deg_NW_lon = math.degrees(NW_lon)
    deg_SE_lat = math.degrees(SE_lat)
    deg_SE_lon = math.degrees(SE_lon)

    north_west = (deg_NW_lat, deg_NW_lon)
    south_east = (deg_SE_lat, deg_SE_lon)
    bound = [north_west,south_east]
    return bound
   
