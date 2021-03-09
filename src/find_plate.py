import imutils
import cv2

def find_plate(edged):
    '''
    Find the contours and return the contour of the plate
    '''
    ## Find Contours
    keypts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypts)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    ## Validate Contours
    locations = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 5, True)
        if len(approx) == 4:
            locations.append(approx)
    
    return locations
