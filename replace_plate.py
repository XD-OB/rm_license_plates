from tools import rotate, get_rect_list, find_most_occurring_color
from PIL import Image as Image_main
from PIL.Image import Image
import cv2
import numpy
import os
    

def replace_plate(image_PIL):
    '''
    Function that hide the car plate
    '''
    ## Car image
    image_CV = cv2.cvtColor(numpy.array(image_PIL), cv2.COLOR_RGB2BGR)

    ## Plate image
    plate_path = './static/plate.png'
    plate_PIL = Image_main.open(plate_path)
    plate_CV = cv2.cvtColor(numpy.array(plate_PIL), cv2.COLOR_RGB2BGR)


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
    # Fill the plate with most occurente color
    x,y,w,h = cv2.boundingRect(plate_contour)
    print("w: ", w)
    print("h: ", h)
    plate_image = image_CV[y:y+h, x:x+w]
    plate_image_blur = cv2.GaussianBlur(plate_image, (25, 25), 0)
    plate_mo_color = find_most_occurring_color(plate_image_blur)
    final_image = cv2.drawContours(final_image, [box], -1, plate_mo_color, -1)
    # Put the plate
    ## resize the plate regarding the space of the contour
    plate_CV_X = cv2.resize(plate_CV, (w,h))
    final_image[y:y+h, x:x+w] = plate_CV_X


    ## Save the result image
    cv2.imwrite('./static/results/original.jpg', image_CV.copy())

    ## Save the result image
    cv2.imwrite('./static/results/result_replace.jpg', final_image)
