from imports import *

#================================================================
#
# Function: getMetaData(image)
#
# Description: This function gets the metadata of the passed
#              image file. MetaData collected includes: name
#              path, image file type, image size, number of 
#              pixels, and image file size
#
# Returns: metaData | type: dictionary of metadata
#
#================================================================
def getMetaData(image):

    #dict of metadata for image
    metaData = dict()

    #get image size (x and y)
    y, x = image.shape 
    metaData.update({"sizeX": x})
    metaData.update({"sizeY": y})

    #get image size (total pixels)
    metaData.update({"pixelCt": x*y})

    return metaData
