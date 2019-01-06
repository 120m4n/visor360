from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import gdal
import fiona
from fiona.crs import from_epsg
from shapely.geometry import mapping, Point
import time

def ListImages(rootdir):
    filesnames =[]
    for subdir, __ , files in os.walk(rootdir):
        for file in files:
            #filepath = subdir + '/' + file
            filepath = file
            if filepath.endswith(".jpg"):
                filesnames.append(filepath)
                #print (filepath)
    return filesnames

def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data

def _get_if_exist(data, key):
    if key in data:
        return data[key]
		
    return None
	
def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:		
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon


################
# Example ######
################
if __name__ == "__main__":

    output = os.path.realpath('./shapefiles/panoramas_360.shp')

    #proyeccion cartografica UTM 16 N
    f_crs=from_epsg(4326)

    # columnas contenidas en el archivo shapefile
    schema = {
    'geometry': 'Point',
    'properties': {
                'id'        :   'int:4',
                'filename'  :   'str:30'
        }                
    }

    folderpath = 'C:/360/images'

    imagelist = ListImages(folderpath)
    
        


    start = time.time()
    id = 0

    with fiona.open(output,'w', driver='ESRI Shapefile', crs=f_crs, schema=schema) as c:
        for imagename in imagelist:
            #print(imagename)
            image = Image.open(folderpath + '/' + imagename)
            exif_data = get_exif_data(image)
            lat,lon = get_lat_lon(exif_data)
            print('{},{},{}'.format(imagename,lat,lon))
            id = id + 1
            point=Point(lon,lat)
            c.write({
                'geometry': mapping(point),
                'properties': {
                'id'        :   id,
                'filename'  :  imagename
            }
            })

    print("proceso finalizado")

    elapsed = (time.time() - start)
    print(' TIEMPO TOTAL DE PROCESAMIENTO')
    print ('		' + str(elapsed/60)+" Minutos")
        