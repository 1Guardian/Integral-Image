from imports import *

#================================================================
#
# Function: createIntegralImage(image)
#
# Description: This function takes in an image and creates
#              an integral image from it. The integral image is 
#              padded along the sides to allow for easy calculation
#              padding is removed when the image is returned.
#
# Returns: integralImage: an 'image' where each value is a 
#          sum of neighboring pixels 
#
#================================================================
def createIntegralImage(image):

    #get bounds
    y, x = image.shape 

    #pad
    paddedY = y + 2
    paddedX = x + 2

    #init image
    integralImage = np.zeros((paddedY,paddedX))

    #get sum from original image
    for i in range(y):
        for j in range(x):
            integralImage[i+1][j+1] = integralImage[i][j+1] + (integralImage[i+1][j] - integralImage[i][j]) + image[i][j]


    #slice away the padding
    integralImage = integralImage[1:-1,1:-1]

    return integralImage