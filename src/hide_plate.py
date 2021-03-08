from src.find_plate import find_plate
import numpy as np
import cv2
    

def hide_plate(image_PIL):
    '''
    Function that detect and hide the car plate
    '''
    ## Read and grayscale the image
    img = cv2.cvtColor(np.array(image_PIL), cv2.COLOR_RGB2BGR)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ## Noise reduction
    bfilter = cv2.bilateralFilter(img_gray, 11, 17, 17)

    ## Find edges for localization
    edged = cv2.Canny(bfilter, 30, 200)

    ## Find plate contour
    locations = find_plate(edged)
    if (len(locations) == 0):
        return False
    plate = locations[0]
    
    ## Hide plate
    if (len(locations) > 0):
        plate = locations[0]

    # get the four points coord
    rect = cv2.minAreaRect(plate)
    box = np.int0(cv2.boxPoints(rect))

    final_image = img.copy()

    # Fill the plate with WHITE color
    final_image = cv2.drawContours(final_image, [box], -1, (255, 255, 255), -1)
    
    # Put the BORDER
    final_image = cv2.drawContours(final_image, [box], 0, (207, 149, 1), 2)

    ## Save the old image
    cv2.imwrite('./static/results/original.jpg', img.copy())

    ## Save the result image
    cv2.imwrite('./static/results/result_hide.jpg', final_image)

    return True
