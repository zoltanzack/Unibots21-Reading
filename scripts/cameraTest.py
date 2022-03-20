import cv2

gstreamer_string = "nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, framerate=30/1, format=(string)NV12 ! nvvidconv flip-method=2 ! video/xraw(memory:NVMM) ! drop=true"

cam = cv2.VideoCapture(gstreamer_string, cv2.CAP_GSTREAMER)
while not cam.isOpened():
	cam = cv2.VideoCapture(gstreamer_string, cv2.CAP_GSTREAMER)

key = 27
while True:
	if key == 27:
		break

	ret, frame = cam.read()
	print(ret)
	if ret:
		cv2.imshow("Frame", frame)	

	key = cv2.waitKey(0)

