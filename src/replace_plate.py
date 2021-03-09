from src.find_plate import find_plate
import numpy as np
import imutils
import cv2
    

def replace_plate(image_PIL):
    '''
    Function that detect and replace the car old plate with new plate
    '''
    ## Read and grayscale the image
    img = cv2.cvtColor(np.array(image_PIL), cv2.COLOR_RGB2BGR)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ## Noise reduction
    #bfilter = cv2.bilateralFilter(img_gray, 11, 17, 17)

    ## Find edges for localization
    edged = cv2.Canny(img_gray, 170, 200)

    ## Find plate contour
    locations = find_plate(edged)
    if (len(locations) == 0):
        return False
    plate = locations[0]

    ## Show car plate
    mask = np.zeros(img_gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [plate], 0,255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    # Trait new plate

    ## plate
    img_plate = cv2.imread('./static/plate.png')

    pts_src = np.array([[img_plate.shape[1],0], [0,0],  [0, img_plate.shape[0]], [img_plate.shape[1], img_plate.shape[0]]])

    ## Calculate Homography
    h, status = cv2.findHomography(pts_src, plate)

    ## Wrap the source
    new_plate = cv2.warpPerspective(img_plate, h, (img.shape[1],img.shape[0]))

    # Put the new plate

    ## Now create a mask of logo and create its inverse mask also
    new_plate_gray = cv2.cvtColor(new_plate, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(new_plate_gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    ## Now black-out the area of the old plate
    img_bo = cv2.bitwise_and(img ,img, mask=mask_inv)

    ## Merge the images
    final_image = cv2.bitwise_or(img_bo, new_plate)

    ## Save the old image
    cv2.imwrite('./static/results/original.jpg', img.copy())

    ## Save the result image
    cv2.imwrite('./static/results/result_replace.jpg', final_image)

    return True
