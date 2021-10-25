from imutils import paths
from vidgear.gears import CamGear
import numpy as np
import imutils
import cv2
from pyzbar.pyzbar import decode
import time


def afstand_bereken(points):
    print(points)
    width = points[2, 0] - points[0, 0]
    print(points[3, 0])
    print(points[0, 0])
    print(width)
    distance = (0.2 * 655) / width
    print(distance)
    return distance


def decoder(image):
    gray_img = cv2.cvtColor(image, 0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        (x, y, w, h) = obj.rect
        pts = np.array(points, np.int32)

        distance = afstand_bereken(points)
        # print(pts)
        # width = pts[2, 0] - pts[0, 0]
        # print(pts[3, 0])
        # print(pts[0, 0])
        # print(width)
        # Distance =(0.2 * 655) / width
        # print(Distance)

        cv2.putText(image, "%.2f m" % distance,
                    (image.shape[1] - 300, image.shape[0] - 100), cv2.FONT_HERSHEY_SIMPLEX,
                    2.0, (0, 255, 0), 3)
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type
        string = "Data: " + str(barcodeData) + " | Type: " + str(barcodeType)

        cv2.putText(frame, string, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        print("Barcode: "+barcodeData + " | Type: "+barcodeType)
        # time.sleep(1)


# cap = cv2.VideoCapture(0)
stream = CamGear(source=0).start()
scale = 1
while True:
    frame = stream.read()

    height, width, channels = frame.shape
    # centerX, centerY = int(height / 2), int(width / 2)
    # prepare the crop
    centerX, centerY = int(height / 2), int(width / 2)
    radiusX, radiusY = int(centerX * scale), int(centerY * scale)

    minX, maxX = centerX - radiusX, centerX + radiusX
    minY, maxY = centerY - radiusY, centerY + radiusY

    cropped = frame[minX:maxX, minY:maxY]
    frame = cv2.resize(cropped, (width, height))

    if frame is None:
        break

    decoder(frame)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    if code == ord('u'):
        scale = scale + 0.05  # +5

    if code == ord('d'):
        scale = scale - 0.05  # +5

    if cv2.waitKey(1) == 27:
        break  # esc to quit
cv2.destroyAllWindows()
stream.stop()

