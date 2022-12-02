#==============================================================================
#
# Class : CS 5420
#
# Author : Tyler Martin
#
# Project Name : Project 7 | Integral Images
#
# Date: 12-06-2022
#
# Description: This project calculates the integral image from a given
#              image and then allows the user to draw a bounding rect
#              in which the integral image is used to find the sum of
#              the pixels in the area, and the average pixel value in
#              the area. It is then reapplied to threshold the area in
#              the original image
#
# Notes: Since I know you prefer to read and work in C++, this file is set
#        up to mimic a standard C/C++ flow style, including a __main__()
#        declaration for ease of viewing. Also, while semi-colons are not 
#        required in python, they can be placed at the end of lines anyway, 
#        usually to denote a specific thing. In my case, they denote globals, 
#        and global access, just to once again make it easier to parse my code
#        and see what it is doing and accessing.
#
#==============================================================================

#"header" file imports
from imports import *
from checkImages import *
from getMetaData import *
from grayScaleImage import *
from restrictIntensities import *
from integralImage import *

#================================================================
#
# GLOBALS
#
#================================================================
currentImg = 0;
maxSize = 0;
currentImage = 0;
originalName = "out";
originalImage = 0;
boxIdentifier = None
boxCorners = []
globalpath = "/"
x = 1080;
y = 720;
integralImage = None;

#================================================================
#
# Class: ImageBox
#
# Description: This class serves as the GUI for the application.
#              It allows selecting a region of the opened image
#              by clicking in one area then dragging the mouse to
#              a new area before releasing the click. That region
#              will then have histogram equalization applied to it.
#
#================================================================
class imageBox(Tk):
    def __init__(self):
        super().__init__()
        
        #gain temporary access to globals
        global currentImage;
        global originalImage;
        global x;
        global y;

        #setup the basic window features
        self.title('Image Highlighter')
        self.resizable(0, 0)

        #no windows smaller than 720x1080
        #(Also setting a variable to let me know
        # how long the word wrap should be)
        if (x < 0 or y < 0):
            self.geometry("1080x720")
            self.realWindowLength = 1080
        else:
            self.geometry(str(x) + 'x' + str(y))
            self.realWindowLength = x

        #setting up the Canvas
        self.canvas = tk.Canvas()
        self.canvas.pack()

        #binding the mouse events to canvas actions
        self.canvas.bind('<Button-1>', self.setup)
        self.canvas.bind('<B1-Motion>', self.drawBox)
        self.canvas.bind('<ButtonRelease-1>', self.endBox)

        #setting the canvas size
        self.canvas.configure(width=x, height=y)

        #convert our image back to PIL format
        #(essentially just swapping bgr pixel
        # order to rgb for pil)
        #self.blue, self.green, self.red = cv2.split(resizeImage(originalImage, x, y, getMetaData(originalImage)))
        self.imageArray, self.delta = (originalImage, 1)
        self.img = cv2.merge(cv2.split(self.imageArray))
        self.icon = ImageTk.PhotoImage(image=Image.fromarray(self.img))

        #set key handler listener
        self.bind("<Key>", self.key_handler)

        #drawing the image to the canvas
        self.imageReference = self.canvas.create_image(0, 0, anchor=NW, image=self.icon)

#===========================================
    #this is a callback function. It is fired
    #when a bind event happens to check for a key
    #fire event. If a valid key fire is detected,
    #globals are updated, and the displayed image
    #is as well
    #===========================================
    def key_handler(self, event):
        #gain access to the global
        global currentImg;
        global maxSize;
        global ImgList;
        global ImagePathList;
        global x;
        global y;
        action = event.keysym;

        #listen for keystrokes
        if action == 'q':
            quit();
    
    #===========================================
    #this is a callback function. It is fired
    #every 100 milliseconds to check for a key
    #fire event. If a key fire is detected, the
    #globals are updated, and the displayed image
    #is as well
    #===========================================
    def update(self):

        #gain access to the global
        global currentImage;
        global ImagePathList;
        global originalName;

        #listen for keystrokes
        if keyboard.is_pressed("q"):
            quit();
        if keyboard.is_pressed("s"):
            saveImage(currentImage, ".jpg", "./", originalName)
        
        #recursive call to keep listening
        self.imgBox.after(100, self.update)

    #===========================================
    #this function starts the drawing of the
    #highlight box that the user can designate 
    #as the area that should have the histogram
    #equalization applied to it.
    #===========================================
    def drawBox(self, event):
        global boxIdentifier
        global boxCorners

        #remove the old mouse position and add the current one
        if len(boxCorners) > 2:
            boxCorners = boxCorners[:len(boxCorners)-2]
        boxCorners.extend((event.x, event.y))

        #ensure that we are not drawing multiple boxes,
        #but clearing all old boxes on new box draw
        if boxIdentifier is not None:
            self.canvas.delete(boxIdentifier)
        boxIdentifier = self.canvas.create_rectangle(boxCorners, outline='red')

    #===========================================
    #this function is fired when the first click
    #happens. It sets the initial starting point
    #as well as clearing out any other boxes
    #that were draw before the current box being
    #drawn started to exist.
    #===========================================
    def setup(self, event):
        global boxCorners
        global boxIdentifier

        #reset the box for each redraw 
        self.canvas.delete(boxIdentifier)
        boxIdentifier = None
        boxCorners.clear()

        #add initial mouse position to draw the box from
        boxCorners.extend((event.x, event.y))

    #===========================================
    #this function will actually initiate the 
    #histogram equalization and will add the 
    #selected region back into the image.
    #===========================================
    def endBox(self, event=None):

        #get access to the coordinates of our selection
        #and the image
        global boxCorners
        global originalImage
        global x
        global y
        global delta
        global integralImage

        #sum of pixels
        pixelSum = 0
        count = 0

        #make sure we don't print misfires
        if len(boxCorners) < 3:
            return

        #handle the histogram equalization here
        scaledBoxCorners = np.copy(boxCorners)

        #round the values to their nearest pixels
        scaledBoxCorners = np.copy(boxCorners)
        for i in range(len(scaledBoxCorners)):
            scaledBoxCorners[i] = int(scaledBoxCorners[i] * self.delta)

        #get the average of the pixels in that region
        smallX = min(scaledBoxCorners[1], scaledBoxCorners[3])
        largeX = max(scaledBoxCorners[1], scaledBoxCorners[3])
        smallY = min(scaledBoxCorners[0], scaledBoxCorners[2])
        largeY = max(scaledBoxCorners[0], scaledBoxCorners[2])

        pixelSum = integralImage[largeX][largeY] - integralImage[largeX][smallY-1] - integralImage[smallX-1][largeY] + integralImage[smallX-1][smallY-1]
        count = (((largeX - smallX)+1) * ((largeY - smallY)+1))

        #print and get average for threshold
        print("Pixel Sum of Bounded Area: ", pixelSum)
        pixelAverage = int(pixelSum / count)
        print("Pixel Average of Bounded Area: ", pixelAverage)
        print("Pixel Count in Bounded Area: ", count)

        #make copy of image for modification
        modifiedImage = np.copy(originalImage)
        histoImage = modifiedImage[min(scaledBoxCorners[1], scaledBoxCorners[3]):max(scaledBoxCorners[1], scaledBoxCorners[3]), min(scaledBoxCorners[0],scaledBoxCorners[2]):max(scaledBoxCorners[0],scaledBoxCorners[2])]
        x, y = histoImage.shape
        #cv2.threshold(src, thresh, maxval, type)
        print(histoImage.shape)

        histoImage = cv2.threshold(histoImage, pixelAverage, 255, cv2.THRESH_BINARY)[1]

        modifiedImage = np.copy(originalImage)

        #dim the image and reimpose the histogram equalized version on the original
        modifiedImage[min(scaledBoxCorners[1], scaledBoxCorners[3]):max(scaledBoxCorners[1], scaledBoxCorners[3]), min(scaledBoxCorners[0],scaledBoxCorners[2]):max(scaledBoxCorners[0],scaledBoxCorners[2])] = histoImage

        #draw the new image back to the canvas
        self.icon = ImageTk.PhotoImage(image=Image.fromarray(modifiedImage))

        #drawing the image to the canvas
        self.imageReference = self.canvas.create_image(0, 0, anchor=NW, image=self.icon)
        
        return

#================================================================
#
# Function: __main__
#
# Description: This function is the python equivalent to a main
#              function in C/C++ (added just for ease of your
#              reading, it has no practical purpose)
#
#================================================================

def __main__(argv):

    #gain access to our globals
    global maxSize;
    global currentImg;
    global currentImage;
    global originalImage;
    global originalName;
    global globalpath;
    global integralImage;
    global x;
    global y;

    #variable to hold path
    path = "nothing"
    thresh = False
    Huffman = False

    # get arguments and parse
    try:
      opts, args = getopt.getopt(argv,"th:i:")
    except getopt.GetoptError:
        print("ii.py -h -t -b -i imagefile")
        print("===========================================================================================================")
        print("-i : image file that you want to work on")
        print("-t : whether or not to generate a thresholded image (8 levels)")
        sys.exit(2)
    for opt, arg in opts:
        if opt == ("-h"):
            print("ii.py -h -t -b -i imagefile")
            print("===========================================================================================================")
            print("-i : image file that you want to work on")
            print("-t : whether or not to generate a thresholded image (8 levels)")
            sys.exit(2)
        elif opt in ("-i", "--img"):
            path = arg
        elif opt in ("-t", "--thresh"):
            thresh = True

    #make sure we got at the least, a path
    if (path == "nothing"):
        print("you must provide an image to start with!")
        sys.exit(2)

    #set max size global
    originalImage = grayScaleImage(checkImages(path))
    currentImage = originalImage

    #check and see if we are supposed to restrict the intensities
    if thresh:
        currentImage = restrictIntensities(currentImage)

    #set the window size
    globalpath = path
    originalName = os.path.splitext(os.path.basename(path))[0]
    meta = getMetaData(currentImage)
    x = meta.get("sizeX")
    y = meta.get("sizeY")

    #get integral image
    integralImage = createIntegralImage(currentImage)

    #make the imagebrowser gui
    ws = imageBox()
    ws.mainloop()

#start main
argv = ""
__main__(sys.argv[1:])