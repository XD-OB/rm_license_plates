from src.tools import rotate, get_rect_list
from PIL import Image as Image_main
from PIL.Image import Image
import cv2
import numpy
import os
    

def hide_plate(image_PIL):
    '''
    Function that hide the car plate
    '''
    ## Car image
    image_CV = cv2.cvtColor(numpy.array(image_PIL), cv2.COLOR_RGB2BGR)

    ### Preprocessing the image
    gray = cv2.cvtColor(image_CV, cv2.COLOR_BGR2GRAY)
    bilateral = cv2.bilateralFilter(gray, 11, 17, 17)
    blur = cv2.GaussianBlur(bilateral, (5, 5), 0)

    ## Canny Edge Detection
    edged = cv2.Canny(blur, 170, 200)

    ## Find Contours
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    # get list of rectangles contours
    rectangle_contours = get_rect_list(contours)

    ## Hide plate
    plate_contour = rectangle_contours[0]
    # get the four points coord
    rect = cv2.minAreaRect(plate_contour)
    box = numpy.int0(cv2.boxPoints(rect))
    # Copy Image
    final_image = image_CV.copy()
    # Fill the plate with WHITE color
    final_image = cv2.drawContours(final_image, [box], -1, (255, 255, 255), -1)
    # Put the BORDER
    final_image = cv2.drawContours(final_image, [box], 0, (207, 149, 1), 2)


    ## Save the result image
    cv2.imwrite('./static/results/original.jpg', image_CV.copy())

    ## Save the result image
    cv2.imwrite('./static/results/result_hide.jpg', final_image)
