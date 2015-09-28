# Movie Credits Detect

Use OpenCV 3.0 to traverse a set of image grabs from a piece of video content to determine when the credits start. 

This is a proof of concept that looks for general shapes that are text like and have aspect ratios that are similar to words. The tunable parameters are sensative to the size of the input image. The larger the input image the better confidence of text detection at the expense of processing time. A good compromise is 704 x 396 as this has enough vertical resolution to distinguish dense movie credits.

# Strategy
First find the content duration by using ffprobe.

Use FFMPEG to generate a sequence of PNG images at 1 second intervals starting between 2 to 10 minutes from the end of the content.

ffmpeg -ss {hh:mm:ss} -i {filename} -r 1 -f image2 {output}%03d.png

Use the python script to analyse the images to detect the approximate start of captions.

