import cv2
from matplotlib import pyplot as plt
import numpy as np
import methods

cam = cv2.VideoCapture(0)

while cam == None:
    cam = cv2.VideoCapture(0)

def fun(_):
    return

cv2.namedWindow("controls")

cv2.createTrackbar("bHueL", "controls", 0, 255, fun)
cv2.createTrackbar("bHueU", "controls", 0, 255, fun)
cv2.createTrackbar("bSatL", "controls", 0, 255, fun)
cv2.createTrackbar("bSatU", "controls", 0, 255, fun)
cv2.createTrackbar("bValL", "controls", 0, 255, fun)
cv2.createTrackbar("bValU", "controls", 0, 255, fun)
cv2.createTrackbar("wHueL", "controls", 0, 255, fun)
cv2.createTrackbar("wHueU", "controls", 0, 255, fun)
cv2.createTrackbar("wSatL", "controls", 0, 255, fun)
cv2.createTrackbar("wSatU", "controls", 0, 255, fun)
cv2.createTrackbar("wValL", "controls", 0, 255, fun)
cv2.createTrackbar("wValU", "controls", 0, 255, fun)
cv2.createTrackbar("blur", "controls", 0, 255, fun)
cv2.createTrackbar("blurSigma", "controls", 0, 255, fun)

cv2.setTrackbarPos("bHueL", "controls", 100)
cv2.setTrackbarPos("bHueU", "controls", 120)
cv2.setTrackbarPos("bSatL", "controls", 100)
cv2.setTrackbarPos("bSatU", "controls", 255)
cv2.setTrackbarPos("bValL", "controls", 50)
cv2.setTrackbarPos("bValU", "controls", 255)

cv2.setTrackbarPos("wHueL", "controls", 37)
cv2.setTrackbarPos("wHueU", "controls", 97)
cv2.setTrackbarPos("wSatL", "controls", 9)
cv2.setTrackbarPos("wSatU", "controls", 139)
cv2.setTrackbarPos("wValL", "controls", 154)
cv2.setTrackbarPos("wValU", "controls", 235)

cv2.setTrackbarPos("blur", "controls", 13)
cv2.setTrackbarPos("blurSigma", "controls", 2)

while True:
    ret, frame = cam.read()
    if not ret:
        continue
       
    size = 420
    ratio = frame.shape[1] / frame.shape[0]
       
    frame = cv2.resize(frame, (int(size * ratio), size))
    
    
    val = int(cv2.getTrackbarPos("blur","controls"))
    kernelSize = int((size*.1)-1)
    if val % 2 == 0:
        kernelSize = val + 1
    else:
        kernelSize = val
        
    frame = cv2.GaussianBlur(frame, (kernelSize, kernelSize), int(cv2.getTrackbarPos("blurSigma","controls")))
        
    # Colour banding. Blue and white
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
    blueL = (int(cv2.getTrackbarPos("bHueL","controls")), int(cv2.getTrackbarPos("bSatL","controls")), int(cv2.getTrackbarPos("bValL","controls")))
    blueU = (int(cv2.getTrackbarPos("bHueU","controls")), int(cv2.getTrackbarPos("bSatU","controls")), int(cv2.getTrackbarPos("bValU","controls")))
    
    whiteL = (int(cv2.getTrackbarPos("wHueL","controls")), int(cv2.getTrackbarPos("wSatL","controls")), int(cv2.getTrackbarPos("wValL","controls")))
    whiteU = (int(cv2.getTrackbarPos("wHueU","controls")), int(cv2.getTrackbarPos("wSatU","controls")), int(cv2.getTrackbarPos("wValU","controls")))
        
    hsvBlue = cv2.inRange(hsv, blueL, blueU)
    hsvWhite = cv2.inRange(hsv, whiteL, whiteU)
    
    contoursBlue, hierarchyBlur = cv2.findContours(hsvBlue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contourBlue = cv2.cvtColor(hsvBlue, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(contourBlue, contoursBlue, -1, (255,0,0), 5)
    
    contoursWhite, hierarchyWhite = cv2.findContours(hsvWhite, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contourWhite = cv2.cvtColor(hsvWhite, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(contourWhite, contoursWhite, -1, (255,0,0), 4)
    

    contour_img = contourBlue + contourWhite
    cv2.imshow("contours", contour_img)

    ret, ballMask = cv2.threshold(cv2.cvtColor(contour_img, cv2.COLOR_BGR2GRAY), 244, 255, cv2.THRESH_BINARY)

    ballMask = cv2.cvtColor(ballMask, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(ballMask, contoursWhite, -1, (0,0,255), 2)
    cv2.drawContours(ballMask, contoursBlue, -1, (0,0,255), 2)
        
    cv2.imshow("ballMask", ballMask)
        
    hsv2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv2[hsv == 0] = 1
    hsv2 = np.float32(hsv2)
    
    h,s,v = cv2.split(hsv2)

    s1 = s/2
    v1 = v/2
    
    sv = s1+v1
    
    s = np.uint8(s)
    v = np.uint8(v)
    sv = np.uint8(sv)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow("frame", frame)
    cv2.imshow("gray", gray)
    #cv2.imshow("s", s)
    #cv2.imshow("v", v)
    #cv2.imshow("sv", sv)
    
    
    passFirst = True

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()
