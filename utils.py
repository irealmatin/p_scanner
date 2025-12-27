import numpy as np
import cv2 as cv


def order_points(pts):
    # Goal : to order the points in the order: top-left, top-right, bottom-right, bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # top-left has the smallest sum, bottom-right has the largest sum (x + y)
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)] # Top-Left
    rect[2] = pts[np.argmax(s)] # Bottom-Right

    # top-right has the smallest difference, bottom-left has the largest difference (x - y)
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)] # Top-Right
    rect[3] = pts[np.argmax(diff)] # Bottom-Left

    return rect



def four_point_transform(image, pts):
    # Goal : perform perspective transform to get top-down view of the document

    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # now calculate the width and height of the new image
    # new width is the maximum distance between bottom-right and bottom-left x-coordinates 
    # or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # new height is the maximum distance between the top-right and bottom-right y-coordinates
    # or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct the set of destination points
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv.getPerspectiveTransform(rect, dst)
    
    # apply warp perspective
    warped = cv.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped