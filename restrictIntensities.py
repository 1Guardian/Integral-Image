from imports import *

#================================================================
#
# Function: restrictIntensities(image, x, y, metaData)
#
# Description: This function restricts the intensities of the 
#              passed in image randomly via thresholding. 
#
# Returns: restricted image
#
#================================================================
def restrictIntensities(image):

    #get bounds
    y, x = image.shape 

    #loop over every pixel and restrict them
    for i in range(y):
        for j in range(x):
            if image[i][j] < 50:
                image[i][j] = 50
            elif image[i][j] < 100:
                image[i][j] = 100
            elif image[i][j] < 150:
                image[i][j] = 150
            elif image[i][j] < 170:
                image[i][j] = 170
            elif image[i][j] < 190:
                image[i][j] = 190
            elif image[i][j] < 200:
                image[i][j] = 200
            elif image[i][j] < 250:
                image[i][j] = 250
            elif image[i][j] < 255:
                image[i][j] = 255

    return image