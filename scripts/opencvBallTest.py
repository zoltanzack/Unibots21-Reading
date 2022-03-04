import cv2
from matplotlib import pyplot as plt
import numpy as np
import methods

cam = cv2.VideoCapture(0)

while cam == None:
    cam = cv2.VideoCapture(0)

def fun(_):
    return

cv2.namedWindow("1")
cv2.createTrackbar("hueL", "1", 0, 255, fun)
cv2.createTrackbar("hueU", "1", 0, 255, fun)
cv2.createTrackbar("satL", "1", 0, 255, fun)
cv2.createTrackbar("satU", "1", 0, 255, fun)
cv2.createTrackbar("valL", "1", 0, 255, fun)
cv2.createTrackbar("valU", "1", 0, 255, fun)

cv2.setTrackbarPos("hueL", "1", 100)
cv2.setTrackbarPos("hueU", "1", 120)
cv2.setTrackbarPos("satL", "1", 100)
cv2.setTrackbarPos("satU", "1", 255)
cv2.setTrackbarPos("valL", "1", 50)
cv2.setTrackbarPos("valU", "1", 220)

#cv2.createTrackbar("min", "1", 0, 255, fun)
#cv2.createTrackbar("max", "1", 0, 255, fun)

passFirst = False
prevMasks = []
maxMasks = 0

while True:
    ret, frame = cam.read()
    if not ret:
        continue
       
    size = 420
    ratio = frame.shape[1] / frame.shape[0]
       
    frame = cv2.resize(frame, (int(size * ratio), size))
    
    kernelSize = int((size*.1)-1)
    kernelSize = 69
    frame = cv2.GaussianBlur(frame, (kernelSize, kernelSize), 0)
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower = (int(cv2.getTrackbarPos("hueL","1")), int(cv2.getTrackbarPos("satL","1")), int(cv2.getTrackbarPos("valL","1")))
    upper = (int(cv2.getTrackbarPos("hueU","1")), int(cv2.getTrackbarPos("satU","1")), int(cv2.getTrackbarPos("valU","1")))
    
    newMask = cv2.inRange(frame, lower, upper)
    newMask = cv2.erode(newMask, None, iterations=3)
    #newMask = cv2.dilate(newMask, None, iterations=2)
    
    if passFirst:
        mask = newMask
        
        if len(prevMasks) < maxMasks:
            prevMasks.append(newMask)
        
        nextMask = None
        for i in range(0, len(prevMasks)):
            index = len(prevMasks)-i-1
            if i == 0:
                nextMask = prevMasks[index]
                prevMasks[index] = newMask
            else:
                curMask = prevMasks[index]
                prevMasks[index] = nextMask
                nextMask = curMask
                
            mask = cv2.bitwise_and(mask, prevMasks[index])
             
        cv2.imshow("2", mask)
    
    
    prevMask = newMask
    
    frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # -- DFT --
    
    sample = gray
    
    img_h = cv2.getOptimalDFTSize(sample.shape[0])
    img_w = cv2.getOptimalDFTSize(sample.shape[1])
    padded_img = cv2.copyMakeBorder(sample, 0, img_h-sample.shape[0], 0, img_w-sample.shape[1], cv2.BORDER_CONSTANT, value=0)
    complex_arr = [np.float32(padded_img), np.zeros(padded_img.shape, np.float32)]
    complex_img = cv2.merge(complex_arr)
    
    complex_mag, complex_phase, mag_img = methods.fft(complex_img)
    
    mag_img = mag_img.copy()
    xcenter = mag_img.shape[1] // 2
    ycenter = mag_img.shape[0] // 2
    highpass_img = cv2.circle(mag_img, (xcenter, ycenter), radius=100, color=0, thickness=cv2.FILLED)
    #threshold_img = cv2.threshold(highpass_img, 170, 255, cv2.THRESH_BINARY)[1]
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    #mask_img = cv2.morphologyEx(threshold_img, cv2.MORPH_DILATE, kernel)     
    #complex_mag[mask_img != 0] = 0
    complex_mag[highpass_img == 0] = 0
    
    spatial_img = methods.ifft(complex_mag, complex_phase)
    cv2.imshow("spatial_img", spatial_img)
    cv2.imshow("highpass_img", highpass_img)
    
    # // DFT //
    
    #frame32 = np.float32(newMask)
    #dft = cv2.dft(frame32, flags = cv2.DFT_COMPLEX_OUTPUT)
    #dft_shift = np.fft.fftshift(dft)
    
    # Display dft
    #magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
    #magnitude_spectrum = np.uint8(magnitude_spectrum)
    #cv2.imshow("magnitude_spectrum", magnitude_spectrum)
    
    # Create mask
    #blank = np.zeros_like(dft_shift)
    #mask = cv2.circle(blank, (int(blank.shape[0]/2), int(blank.shape[1]/2)), 50, (255,255), -1)
    #mask = cv2.circle(blank, (int(frame.shape[1]/2),int(frame.shape[0]/2)), 100, (255,255), -1)

    # Apply mask and inverse
    #fshift = dft_shift*mask
    #f_ishift = np.fft.ifftshift(fshift)
    
    # Display masked dft
    #magnitude_spectrum_2 = 20*np.log(cv2.magnitude(fshift[:,:,0],fshift[:,:,1]))
    #magnitude_spectrum_2 = np.uint8(magnitude_spectrum_2)
    #cv2.imshow("magnitude_spectrum_2", magnitude_spectrum_2)
    
    #img_back = cv2.idft(f_ishift)
    #img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])
    #img_back = np.uint8(img_back)
    #cv2.imshow("img_back", img_back)
    
    #hist = cv2.calcHist([frame], [0], None, [256], [0, 256])
    #cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    #plt.plot(hist, color="k")
    
    cv2.imshow("1", frame)
    
    
    passFirst = True

    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()
