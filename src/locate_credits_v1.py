import cv2
import numpy as np
import glob 

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
    xscaleFactor = 15
    yscaleFactor = 3
    for box in rects:
        [x,y,w,h] = box
        # Draw filled bounding boxes on mask
        cv2.rectangle(mask, (x-xscaleFactor,y-yscaleFactor),(x+w+xscaleFactor,y+h+yscaleFactor), (255,255,255), cv2.FILLED)
    cv2.imshow("Mask", mask)
    # Find contours in mask
    # If bounding boxes overlap, they will be joined by this function call
    rectangles = []
    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE);
    for contour in contours[1]:
        rect = cv2.boundingRect(contour)
        rect2 = cv2.minAreaRect(contour)
        [x,y,w,h] = rect
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
        
        
        # Test the eccentricity
        if len(contour) > 5:
            (xe,ye),(MA,ma),angle = cv2.fitEllipse(contour)
            if (float(MA) / ma) > .995:
                continue;
    
        #if (float(w*h)/(width*height)) < 0.01 or float(w)/width < 0.01 or (float(w)/h < 1.2 and float(h)/height < 0.2) :
        #    continue;
        if ((float(w)/h < 4) and (float(w*h)/(width*height)) < 0.06) or float(w)/width < 0.005 or (float(w)/h < 1.2 and float(h)/height < 0.2) :
            continue;
        
        rectangles.append(rect)
        
        [x,y,w,h] = rect         
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
    
    cv2.imshow("Rectangles", image)     
    cv2.waitKey(0)            
    return rectangles

files = glob.glob("/Users/alanhurdle/Documents/workspace/CreditDetect/test_files/bbc    /*.png")

# Locate the first time text is detected by splitting the list
# and working along the images until text is found
minimum = 0
m = len(files) - 1
misses = 5
hitname = ""
index = 0

while(m > 0 | misses > 0):
    print "round: ", m
    filename = files[m]
    image = cv2.imread(filename)
    rects = locate_text(image)

    if len(rects) == 0:
        misses = misses - 1
        if misses == 0:
            break;
        m = m - 1
    else:
        hitname = filename
        index = m
        misses = 5
        m = m - 1

print "Filename = " + hitname + " Offset = ", index
