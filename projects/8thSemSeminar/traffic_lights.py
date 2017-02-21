import cv2
import numpy as np

img = cv2.imread('./images/traffic_signal.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
output = img.copy()
# ensure at least some circles were found
if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")

    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        print img[x + 10, y + 10]
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)

    # show the output image
    cv2.imshow("output", np.hstack([img, output]))
    cv2.waitKey(0)