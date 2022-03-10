import cv2
import numpy as np

def fun(_):
    return

cv2.namedWindow("controls")

cv2.createTrackbar("yHueL", "controls", 0, 255, fun)
cv2.createTrackbar("yHueU", "controls", 0, 255, fun)
cv2.createTrackbar("ySatL", "controls", 0, 255, fun)
cv2.createTrackbar("ySatU", "controls", 0, 255, fun)
cv2.createTrackbar("yValL", "controls", 0, 255, fun)
cv2.createTrackbar("yValU", "controls", 0, 255, fun)
cv2.createTrackbar("wHueL", "controls", 0, 255, fun)
cv2.createTrackbar("wHueU", "controls", 0, 255, fun)
cv2.createTrackbar("wSatL", "controls", 0, 255, fun)
cv2.createTrackbar("wSatU", "controls", 0, 255, fun)
cv2.createTrackbar("wValL", "controls", 0, 255, fun)
cv2.createTrackbar("wValU", "controls", 0, 255, fun)
cv2.createTrackbar("blur", "controls", 0, 255, fun)
cv2.createTrackbar("wallHueL", "controls", 0, 255, fun)
cv2.createTrackbar("wallHueU", "controls", 0, 255, fun)
cv2.createTrackbar("wallSatL", "controls", 0, 255, fun)
cv2.createTrackbar("wallSatU", "controls", 0, 255, fun)
cv2.createTrackbar("wallValL", "controls", 0, 255, fun)
cv2.createTrackbar("wallValU", "controls", 0, 255, fun)
cv2.createTrackbar("blur", "controls", 0, 255, fun)
cv2.createTrackbar("blurSigma", "controls", 0, 255, fun)

cv2.setTrackbarPos("yHueL", "controls", 30)
cv2.setTrackbarPos("yHueU", "controls", 51)
cv2.setTrackbarPos("ySatL", "controls", 56)
cv2.setTrackbarPos("ySatU", "controls", 248)
cv2.setTrackbarPos("yValL", "controls", 45)
cv2.setTrackbarPos("yValU", "controls", 193)

cv2.setTrackbarPos("wHueL", "controls", 5)
cv2.setTrackbarPos("wHueU", "controls", 100)
cv2.setTrackbarPos("wSatL", "controls", 0)
cv2.setTrackbarPos("wSatU", "controls", 22)
cv2.setTrackbarPos("wValL", "controls", 122)
cv2.setTrackbarPos("wValU", "controls", 216)

cv2.setTrackbarPos("wallHueL", "controls", 105)
cv2.setTrackbarPos("wallHueU", "controls", 121)
cv2.setTrackbarPos("wallSatL", "controls", 0)
cv2.setTrackbarPos("wallSatU", "controls", 16)
cv2.setTrackbarPos("wallValL", "controls", 206)
cv2.setTrackbarPos("wallValU", "controls", 255)

cv2.setTrackbarPos("blur", "controls", 2)
cv2.setTrackbarPos("blurSigma", "controls", 2)

useCam = False
if useCam:
    cam = cv2.VideoCapture(0)
    while cam == None:
        cam = cv2.VideoCapture(0)

while True:
    if useCam:
        ret, frame = cam.read()
        if not ret:
            continue
    else:
        frame = cv2.imread('../apriltags/test_environment_2.png', 1)
    
    size = 720
    ratio = frame.shape[1] / frame.shape[0]   
    frame = cv2.resize(frame, (int(size * ratio), size))
 
    val = int(cv2.getTrackbarPos("blur", "controls"))
    kernelSize = int((size*.1)-1)
    if val % 2 == 0:
        kernelSize = val + 1
    else:
        kernelSize = val
    frame = cv2.GaussianBlur(frame, (kernelSize, kernelSize), int(cv2.getTrackbarPos("blurSigma","controls")))
        
    # Colour banding. Yellow and white
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
    yellowL = (int(cv2.getTrackbarPos("yHueL","controls")), int(cv2.getTrackbarPos("ySatL","controls")), int(cv2.getTrackbarPos("yValL","controls")))
    yellowU = (int(cv2.getTrackbarPos("yHueU","controls")), int(cv2.getTrackbarPos("ySatU","controls")), int(cv2.getTrackbarPos("yValU","controls")))
    
    whiteL = (int(cv2.getTrackbarPos("wHueL","controls")), int(cv2.getTrackbarPos("wSatL","controls")), int(cv2.getTrackbarPos("wValL","controls")))
    whiteU = (int(cv2.getTrackbarPos("wHueU","controls")), int(cv2.getTrackbarPos("wSatU","controls")), int(cv2.getTrackbarPos("wValU","controls")))
    
    wallL = (int(cv2.getTrackbarPos("wallHueL","controls")), int(cv2.getTrackbarPos("wallSatL","controls")), int(cv2.getTrackbarPos("wallValL","controls")))
    wallU = (int(cv2.getTrackbarPos("wallHueU","controls")), int(cv2.getTrackbarPos("wallSatU","controls")), int(cv2.getTrackbarPos("wallValU","controls")))
        
    hsvYellow = cv2.inRange(hsv, yellowL, yellowU)
    hsvWhite = cv2.inRange(hsv, whiteL, whiteU)
    hsvWall = cv2.inRange(hsv, wallL, wallU)
    
    cv2.imshow("Walls", hsvWall)
    
    contoursYellow, _ = cv2.findContours(hsvYellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contourYellow = cv2.cvtColor(hsvYellow, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(contourYellow, contoursYellow, -1, (255,0,0), 5)
    
    contoursWhite, _ = cv2.findContours(hsvWhite, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contourWhite = cv2.cvtColor(hsvWhite, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(contourWhite, contoursWhite, -1, (255,0,0), 4)
    
    contour_img = contourYellow + contourWhite
    cv2.imshow("contours", contour_img)
        
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
    #cv2.imshow("gray", gray)
    #cv2.imshow("s", s)
    #cv2.imshow("v", v)
    #cv2.imshow("sv", sv)
    
    
    passFirst = True

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()
