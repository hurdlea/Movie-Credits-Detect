import cv2
import numpy as np

image = cv2.imread("/Users/alanhurdle/Documents/workspace/CreditDetect/test_files/17404.png", cv2.IMREAD_GRAYSCALE)
#image = cv2.imread("/Users/alanhurdle/Documents/workspace/CreditDetect/test_files/transformer00169.png", cv2.IMREAD_GRAYSCALE)
#image = cv2.imread("/Users/alanhurdle/Documents/workspace/CreditDetect/test_files/transformer00157.png", cv2.IMREAD_GRAYSCALE)
#image = cv2.imread("/Users/alanhurdle/Documents/workspace/CreditDetect/test_files/transformer00236.png", cv2.IMREAD_GRAYSCALE)
#cv2.imshow("img", image)
#cv2.waitKey(0)


height, width = image.shape
mser = cv2.MSER_create(4, 10, 8000, 0.8, 0.2, 200, 1.01, 0.003, 5)

blur = cv2.GaussianBlur(image,(3,3),0)
adapt_threshold = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,5,-25)
cv2.imshow("Thresh1",adapt_threshold)
#blur = cv2.GaussianBlur(image,(5,5),0)
#threshold = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#cv2.imshow("Thresh2",threshold[1])

#cv2.waitKey(0)
contours = mser.detectRegions(adapt_threshold, None)
#_,contours,hierarchy = cv2.findContours(adapt_threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE )

# for each contour found, draw a rectangle around it on original image
rects = []
for contour in contours:
    
    # get rectangle bounding contour
    [x,y,w,h] = cv2.boundingRect(contour)
    if w<2 or h<2:
        continue;
    
    # Test the aspect ratio
    if w/h > 1:
        continue;
    
    # Test area wrt image
    #if (width/w < 10) | (height/h < 10) | (height/h > 20) | (width/w > 40):
    #    continue
    
    # Test the eccentricity
    #(xe,ye),(MA,ma),angle = cv2.fitEllipse(contour)
    #if (MA / ma) > .995:
    #    continue;
    
    # Test solidity
    #area = cv2.contourArea(contour)
    #hull = cv2.convexHull(contour)
    #hull_area = cv2.contourArea(hull)
    #if hull_area == 0:
    #    continue;
    
    #if (area/hull_area) < .3:
    #    continue;
    
    # Test Extent
    #rect_area = w*h
    #extent = area/rect_area
    #if extent < 0.2 or extent > 0.9:
    #    continue;

    # Euler Number
    #filterIdx = filterIdx | [mserStats.EulerNumber] < -4;

    # draw rectangle around contour on original image
    #cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
    #cv2.imshow("Keypoints", image)
    rects.append(cv2.boundingRect(contour))


# Mask of original image
mask = np.zeros((height,width, 1), np.uint8)
# To expand rectangles, i.e. increase sensitivity to nearby rectangles. Doesn't have to be (10,10)--can be anything
scaleFactor = 4
for box in rects:
    [x,y,w,h] = box
    # Draw filled bounding boxes on mask
    cv2.rectangle(mask, (x-scaleFactor,y-scaleFactor),(x+w+scaleFactor,y+h+scaleFactor), (255,255,255), cv2.FILLED)
    
cv2.imshow("Mask", mask)
cv2.waitKey(0)

# Find contours in mask
# If bounding boxes overlap, they will be joined by this function call
rectangles = []
contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE);
for contour in contours[1]:
    rect = cv2.boundingRect(contour)
    [x,y,w,h] = rect
    if w/h <1.5:
        continue;
    
    rectangles.append(rect)

    
#rectangles = cv2.groupRectangles(rects,0,0.8)
for r in rectangles:
    [x,y,w,h] = r
    cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
    
cv2.imshow("Keypoints", image)
cv2.waitKey(0)
