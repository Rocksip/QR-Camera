from imutils import paths
from vidgear.gears import CamGear
import numpy as np
import imutils
import cv2
from pyzbar.pyzbar import decode
import time

def distance_calc(points):
    print(points)
    width = points[2, 0] - points[0, 0]
    print(points[3, 0])
    print(points[0, 0])
    print(width)
    distance = (0.2 * 655) / width
    print(distance)
    return distance


def print_QR_information(image,pts,x, y, barcodeData,  barcodeType):
    red, green , blue = border_reconigtion(image, pts)
    cv2.polylines(image, [pts], True, (red, green, blue), 3)
    string = "Data: " + str(barcodeData) + " | Type: " + str(barcodeType)
    cv2.putText(frame, string, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    print("Barcode: " + barcodeData + " | Type: " + barcodeType)


def print_QR_distance(image, distance):
    cv2.putText(image, "%.2f m" % distance,
                (image.shape[1] - 300, image.shape[0] - 100), cv2.FONT_HERSHEY_SIMPLEX,
                2.0, (0, 255, 0), 3)


def decoder(image):
    gray_img = cv2.cvtColor(image, 0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        (x, y, w, h) = obj.rect
        pts = np.array(points, np.int32)
        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        distance = distance_calc(pts)
        print_QR_information(image,pts,x ,y, barcodeData, barcodeType)
        print_QR_distance(image, distance)


def digtal_zoom(image,scale, code):
    height, width, channels = image.shape
    if code == ord('u'):
        scale = scale + 0.05  # +5

    if code == ord('d'):
        scale = scale - 0.05  # +5
    # centerX, centerY = int(height / 2), int(width / 2)
    # prepare the crop
    print(scale)
    centerX, centerY = int(height / 2), int(width / 2)
    radiusX, radiusY = int(centerX * scale), int(centerY * scale)

    minX, maxX = centerX - radiusX, centerX + radiusX
    minY, maxY = centerY - radiusY, centerY + radiusY

    cropped = image[minX:maxX, minY:maxY]
    image = cv2.resize(cropped, (width, height))
    return image, scale


def border_reconigtion(image, pts):
    height, width, channels = image.shape
    left_border = width * 0.2
    right_border = width * 0.8
    tracker = points[0,0]
    if tracker < left_border:
        red = 255
        green = 0
        blue = 0
    elif tracker > right_border:
        red = 0
        green = 255
        blue = 0
    return red, green, blue
# cap = cv2.VideoCapture(0)
stream = CamGear(source=0).start()
scale = 1



while True:
    frame = stream.read()
    if frame is None:
        break
    decoder(frame)
    code = cv2.waitKey(10)
    frame, scale = digtal_zoom(frame,scale, code)
    cv2.imshow('Image', frame)
    if cv2.waitKey(1) == 27:
        break  # esc to quit
cv2.destroyAllWindows()
stream.stop()

