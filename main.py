# pipline :get orginal image - > resize it - >  Gray sclae image -> blure -> 
# Edge detection -> Find contours -> Filter & Approximate ->  Order Points ->
# warp prespective -> later apply addaptive tresholding to get paper scan -> 
# save to disk

import cv2 as cv 
import numpy as np
from utils import four_point_transform 

def start_scan(img_path):

    image = cv.imread(img_path)
    if image is None:
        print("Could not read the image.")
        return
    
    image_copy = image.copy()

    #resize
    r = 500.0 / image.shape[0]
    dim = (int(image.shape[1] * r), 500)
    image = cv.resize(image, dim, interpolation=cv.INTER_AREA)

    # preprocessing
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    edge_detect = cv.Canny(blurred, 75, 200) 

    # #### for debug ######
    # cv.imshow("Edge Detected Image", edge_detect)

    # find contours
    contours, _ = cv.findContours(edge_detect.copy(), cv.RETR_EXTERNAL , cv.CHAIN_APPROX_SIMPLE)

    # sort contours by area, keep only the largest ones
    contours = sorted(contours, key=cv.contourArea, reverse=True)[:5]

    screen_contour = None # variable to hold the document contour
    for contour in contours:
        # approximate the contour : to less number of points
        peri = cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, 0.02 * peri, True)

        if len(approx) == 4:
            screen_contour = approx
            break

    if screen_contour is not None:
        print("paper found!")
        detected_pts = screen_contour.reshape(4, 2)
        
        # inverse the resize ratio to get points in original image
        ratio = image_copy.shape[0] / 500.0 
        detected_pts = detected_pts * ratio

        warped = four_point_transform(image_copy, detected_pts)

        cv.imshow("Scanned", warped)
        
        cv.drawContours(image, [screen_contour], -1, (0, 255, 0), 2)
        cv.imshow("Outline", image)
        
        cv.waitKey(0)
        cv.destroyAllWindows()
    else:
        print("No paper found!")
    
    

if __name__ == "__main__":
    img_path = "hand_on/document_scanner/input_image/img_for_scan5.jpg"
    start_scan(img_path)



