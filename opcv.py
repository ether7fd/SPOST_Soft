import cv2
import time
import numpy as np
import imutils
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import statistics

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def sizeopencv():
    width = 3 #Reference width
    HEIGHT = 600
    WIDTH = 900
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'));
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,HEIGHT)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,WIDTH)
    
    allsize = np.zeros((10,2))
    
    count = 0
    for x in range(10):
        time.sleep(0.5)
        ret,frame = cap.read()

        # img = cv2.imread(args["image"])
        image = imutils.resize(frame, width=400)
        # image = cv2.resize(img, dsize=(500,500))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        edged = cv2.Canny(gray, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)

        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        (cnts, _) = contours.sort_contours(cnts)
        pixelsPerMetric = None
        
        orig = image.copy()

        i = 0
        for c in cnts:
            if cv2.contourArea(c) > 100:
                i += 1

        num = 0
        list = np.zeros((i+1, 3))
        list2 = []

        for c in cnts:
            if cv2.contourArea(c) < 100:
                continue
            # compute the rotated bounding box of the contour
            # orig = image.copy()
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")

            box = perspective.order_points(box)
            cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
            # loop over the original points and draw them
            for (x, y) in box:
                cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
                    # unpack the ordered bounding box, then compute the midpoint
            # between the top-left and top-right coordinates, followed by
            # the midpoint between bottom-left and bottom-right coordinates
            (tl, tr, br, bl) = box
            (tltrX, tltrY) = midpoint(tl, tr)
            (blbrX, blbrY) = midpoint(bl, br)
            # compute the midpoint between the top-left and top-right points,
            # followed by the midpoint between the top-righ and bottom-right
            (tlblX, tlblY) = midpoint(tl, bl)
            (trbrX, trbrY) = midpoint(tr, br)
            # draw the midpoints on the image
            cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)
            # draw lines between the midpoints
            cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                (255, 0, 255), 2)
            cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                (255, 0, 255), 2)
                # compute the Euclidean distance between the midpoints
            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

            if pixelsPerMetric is None:
                #pixelsPerMetric = dB / args["width"]
                pixelsPerMetric = dB / width

                # compute the size of the object
            dimA = dA / pixelsPerMetric
            dimB = dB / pixelsPerMetric

            list[num][0]=dimA
            list[num][1]=dimB
            list[num][2]=dimA*dimB

            # draw the object sizes on the image
            ###cv2.putText(img, text, Basyo, font, scale, color, Hutosa, lineType)
            cv2.putText(orig, "{:.3f}cm".format(dimA),
                (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (255, 255, 255), 2)
            cv2.putText(orig, "{:.3f}cm".format(dimB),
                (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (255, 255, 255), 2)
            num += 1

        list2=list[:,2]
        
        if len(list2) == 0:
            max_index = 0
        else:
            max_index = np.argmax(list2)
        # show the output image
        #cv2.imshow("Image", orig)
    
        allsize[count][0], allsize[count][1] = list[max_index][0], list[max_index][1]
        count += 1

    tate = statistics.median(allsize[:,0])
    yoko = statistics.median(allsize[:,1])

    return tate, yoko