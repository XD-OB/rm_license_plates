from flask import jsonify
from os import path
import cv2


def rotate(image, angle, scale = 1.0):
    '''
    Return rotated image
    '''
    (h, w) = image.shape[:2]
    if center is None:
        center = (w / 2, h / 2)
    # Rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated


def get_rect_list(contours):
    '''
    filter to get a list of rectangles contours
    '''
    rectangle_contours = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approximationAccuracy = 0.02 * perimeter
        approximation = cv2.approxPolyDP(contour, approximationAccuracy, True)
        if len(approximation) == 4:
            rectangle_contours.append(contour)
    return rectangle_contours


def find_most_occurring_color(cvImage) -> (int, int, int):
    width, height, channels = cvImage.shape
    colorCount = {}
    for y in range(0, height):
        for x in range(0, width):
            BGR = (int(cvImage[x, y, 0]), int(cvImage[x, y, 1]), int(cvImage[x, y, 2]))
            if BGR in colorCount:
                colorCount[BGR] += 1
            else:
                colorCount[BGR] = 1
    maxCount = 0
    maxBGR = (0, 0, 0)
    for BGR in colorCount:
        count = colorCount[BGR]
        if count > maxCount:
            maxCount = count
            maxBGR = BGR
    return maxBGR


def verify_file(file, upload_exts):
    '''
    Verify the image
    '''
    file_name = file.filename
    # Check if the file input was empty
    if (file_name == ''):
        return jsonify({
            'error': "no image"
        })
    # Check extension of the file
    file_ext = path.splitext(file_name)[1]
    if file_ext not in upload_exts:
        return jsonify({
            'error': "wrong image extension"
        })
    return None