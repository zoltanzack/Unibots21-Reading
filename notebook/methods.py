import cv2
import math
import numpy as np

# Takes first img's type as aggregate image's type
def makeOutput(imgs, scalar):
    maxH, maxW = (0, 0)

    # Scale image
    scaled_imgs = []
    for img in imgs:
        h, w = (round(img.shape[0]*scalar), round(img.shape[1]*scalar))
                      
        scaled_imgs.insert(len(scaled_imgs), cv2.resize(img, (h, w)))
        
        maxH = h if maxH < h else maxH
        maxW = w if maxW < w else maxW
           
    gridWidth = math.ceil(math.sqrt(len(imgs)))
    gridHeight = math.ceil(len(imgs) / gridWidth)
       
    scaled_shape = (maxH * gridHeight, maxW * gridWidth)
    
    # Aggregate image
    out_img = np.zeros(scaled_shape, imgs[0].dtype)

    index = 0
    for y in range(0, scaled_shape[0], maxH):
        for x in range(0, scaled_shape[1], maxW):    
            h, w = (y+imgs[index].shape[0], x+imgs[index].shape[1]) # Not using scaled images
            out_img[y:h, x:w] = imgs[index]
            
            index = index + 1
            
            if(index == len(imgs)):
                return out_img

def fft(complex_img):

    # Compute the Definitive Fourier Transform 
    dft = cv2.dft(complex_img)
    dft = np.fft.fftshift(dft) # Shift the fourier image origin to the centre of the image instead of (0,0) (easier visualisation)
        
    # Calculate the magnitude and phase of the complex fourier image
    mag, phase = cv2.cartToPolar(dft[:,:,0], dft[:,:,1])
    
    # Convert the range to a logarthimic scale and then clamp the values between 0 and 255 (gray scale), so that the magnitude can be visualised.
    mag_img = cv2.add(np.ones(mag.shape, dtype = mag.dtype), mag) # Make coefficients > 1
    cv2.log(mag_img, mag_img) # Convert to logarthimic scale
    cv2.normalize(mag_img, mag_img, 0, 255, cv2.NORM_MINMAX)
    
    return [mag, phase, mag_img.astype(np.uint8)] # Return the fourier magnitude and phase, and the visualisation of the magnitude as a uint8 image.
    
def ifft(mag, phase):
    
    # Recalculate the two complex components of the DFT result, using the supplied magnitude and phase.
    real, imag = cv2.polarToCart(mag, phase)
   
    # Unshift the origin of the fourier image and convert it back to the spatial domain
    idft = np.fft.ifftshift(cv2.merge([real, imag]))
    idft = cv2.idft(idft)
    
    # Then decompose the spatial complex image matrix into a 2D array and combine complex components
    spatial_arr = cv2.split(idft)
    spatial_img = cv2.magnitude(spatial_arr[0], spatial_arr[1])
        
    # Convert the range back to 8-bit grayscale
    return cv2.normalize(spatial_img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    
    
    
    
    