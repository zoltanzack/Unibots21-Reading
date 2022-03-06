import cv2

def setupCamera():
    """ 
	gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
	Flip the image by setting the flip_method (most common values: 0 and 2)
	display_width and display_height determine the size of each camera pane in the window on the 		screen
	Default 1920x1080 displayd in a 1/4 size window
	"""

	def gstreamer_pipeline(
		sensor_id=0,
		capture_width=1920,
		capture_height=1080,
		display_width=960,
		display_height=540,
		framerate=30,
		flip_method=0,
	):
		return (
		    "nvarguscamerasrc sensor-id=0 ! "
		    "video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, framerate=30/1, 			format=(string)NV12 ! "
		    "nvvidconv flip-method=2 ! "
		    "video/x-raw(memory:NVMM), format=(string)BGR! appsink name=mysink"

		    #"nvarguscamerasrc sensor-id=%d !"
		    #"video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
		    #"nvvidconv flip-method=%d ! "
		    #"video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
		    #"videoconvert ! "
		    #"video/x-raw, format=(string)BGR ! appsink"
		    #% (
		    #    sensor_id,
		    #    capture_width,
		    #    capture_height,
		    #    framerate,
		    #    flip_method,
		    #    display_width,
		    #    display_height,
		    #)
		)

	# To flip the image, modify the flip_method parameter (0 and 2 are the most common)
	print(gstreamer_pipeline(flip_method=0))
	video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

def show_camera():
	window_title = "CSI Camera"

	
	if video_capture.isOpened():
	    try:
	        window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
	        while True:
	            ret_val, frame = video_capture.read()
	            # Check to see if the user closed the window
	            # Under GTK+ (Jetson Default), WND_PROP_VISIBLE does not work correctly. Under Qt it does
	            # GTK - Substitute WND_PROP_AUTOSIZE to detect if window has been closed by user
	            if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
	                cv2.imshow(window_title, frame)
	            else:
	                break 
	            keyCode = cv2.waitKey(10) & 0xFF
	            # Stop the program on the ESC key or 'q'
	            if keyCode == 27 or keyCode == ord('q'):
	                break
	    finally:
	        video_capture.release()
	        cv2.destroyAllWindows()
	else:
	    print("Error: Unable to open camera")


	#vc = cv2.VideoCapture(0)

	#if vc.isOpened(): # try to get the first frame
	#    is_capturing, frame = vc.read()
	#    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)    # makes the blues image look real colored
