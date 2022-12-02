# Integral-Image
Project to compute the integral image of an input image

## Notes
This project is quite simple: it just computes the integral image, and then thresholds a selection region using the average intensity value of the pixels in that region

## Usage:
<pre>
python ii.py -h -t -i imagefile
        -i : image file that you want to work on
        -t : whether or not to generate a thresholded image (8 levels)
            
