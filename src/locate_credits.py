import cv2
import numpy as np
import glob 
import time

def locate_text(image):
    height, width, depth = image.shape
    mser = cv2.MSER_create(4, 10, 8000, 0.8, 0.2, 200, 1.01, 0.003, 5)
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Pull out grahically overlayed text from a video image
    blur = cv2.GaussianBlur(grey,(3,3),0)
    adapt_threshold = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,5,-25)
    contours = mser.detectRegions(adapt_threshold, None)
    
    # for each contour get a bounding box and remove 
    rects = []
    for contour in contours:
        
        # get rectangle bounding contour
        [x,y,w,h] = cv2.boundingRect(contour)
        
        # Remove small rects
        if w<2 or h<2:
            continue;
        
        # Throw away rectangles which don't match a character aspect ratio
        if (float(w*h)/(width*height)) > 0.005 or float(w)/h > 1 :
            continue;
    
        rects.append(cv2.boundingRect(contour))
    
    
    # Mask of original image
    mask = np.zeros((height,width, 1), np.uint8)
    # To expand rectangles, i.e. increase sensitivity to nearby rectangles
    xscaleFactor = 12
    yscaleFactor = 0
    for box in rects:
        [x,y,w,h] = box
        # Draw filled bounding boxes on mask
        cv2.rectangle(mask, (x-xscaleFactor,y-yscaleFactor),(x+w+xscaleFactor,y+h+yscaleFactor), (255,255,255), cv2.FILLED)
    #cv2.imshow("Mask", mask)
    # Find contours in mask
    # If bounding boxes overlap, they will be joined by this function call
    rectangles = []
    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE);
    for contour in contours[1]:
        
        # Only preserve "squarish" features
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * peri, True)
     
        # the contour is 'bad' if it is not a rectangluarish
        if len(approx) > 8:
            cv2.drawContours(image, [contour], -1, (0,255,0))
            cv2.imshow("Rectangles", image)       
            continue;       

        rect = cv2.boundingRect(contour)

        [x,y,w,h] = rect
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
        
        # Remove small areas and areas that don't have text like features
        # such as a long width.
        if ((float(w*h)/(width*height)) < 0.006):
            # remove small areas
            if float(w*h)/(width*height) < 0.0018:
                continue;
            # remove areas that aren't long
            if (float(w)/h < 2.5): 
                continue;

        else:
            # General catch for larger identified areas that they have
            # a text width profile
            if float(w)/h < 1.8 :
                continue;
                
        rectangles.append(rect)
        
        #[x,y,w,h] = rect         
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
  
      
    cv2.imshow("Rectangles", image)
    cv2.waitKey(0)            
    return rectangles

files = glob.glob("/Users/alanhurdle/Documents/workspace/CreditDetect/test_files/bbc/*.png")

start_time = time.time()

# Locate the first time text is detected by splitting the list
# and working along the images until text is found
minimum = 0
m = len(files)
misses = 5
hitname = ""
index = 0

while(m > 0 and misses > 0):

    filename = files[m - 1]
    #print "filename: ", filename, " round: ", m

    image = cv2.imread(filename)
    rects = locate_text(image)

    if len(rects) == 0:
        misses = misses - 1

    else:
        # Only record significant detections to avoid
        # single false detections over-running the end of credits
        if len(rects) > 1:
            hitname = filename
            index = m
        misses = 5
    
    m = m - 1

# Need a way to determine if the sequence ran to the end
# Also, keep the snapshot of the 
if m > 0:
    print "Filename = " + hitname + "\nCredit start = Duration -", len(files) - index, "sec\n"
else:
    print "End of credits not found"
    
print("--- %s seconds ---" % (time.time() - start_time))
