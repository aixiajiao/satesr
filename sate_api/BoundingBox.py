'''
credit to Jan Philip Matuschek (http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates)

'''
import math
def boundingbox(lat, lon, arc=100):    
    r = 6378137 # radius of earth in km: (), same with Bing API

    # convert coordinates to Radians
    lat_rad = lat * math.pi / 180
    lon_rad = lon * math.pi / 180
    # angular distance in radians on a great circle
    dist_rad = arc / r

    N_lat = lat_rad + dist_rad    
    S_lat = lat_rad - dist_rad
    
    
    delta_lon = math.asin(math.sin(dist_rad) / math.cos(lat_rad))

    E_lon = lon_rad + delta_lon
    W_lon = lon_rad - delta_lon
    
    

    deg_N_lat = math.degrees(N_lat)
    deg_W_lon = math.degrees(W_lon)
    deg_S_lat = math.degrees(S_lat)
    deg_E_lon = math.degrees(E_lon)

    north_west = (deg_N_lat, deg_W_lon)
    south_east = (deg_S_lat, deg_E_lon)
    bound = [north_west,south_east]
    return bound
   
