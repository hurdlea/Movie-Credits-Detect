# Movie Credits Detect

Use OpenCV 3.0 to traverse a set of image grabs from a piece of video content to determine when the credits start.

# Strategy

Use FFMPEG to generate a sequence of PNG images at 1 second intervals starting 10 minutes from the end of the content.

FFMPEG -s {hh:mm:ss} -i {filename} -r 1 -f image2 {output}%03d.png

