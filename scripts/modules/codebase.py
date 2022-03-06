from adafruit_servokit import ServoKit

import board
import busio
import time

class Servo:
	def __init__(self, kit, pin):
		self.kit = kit
		self.pin = pin
		self.set(0)

	def set(self, position):
		self.kit.servo[self.pin].angle = position
		self.position = position

	def moveRange(self, position):
		interval = 1 if position >= self.position else -1
		sweep = range(self.position, position, interval)
		for degree in sweep:
			self.set(degree)
			time.sleep(0.01) # Quiet them down in the library

	#def moveConstant(self, frequency):
		#dutyCycle = 4096 * frequency
		#self.kit.setPWM(self.pin, 0, dutyCycle)

class Motor:
	def __init__(self, kit, positive_pin, negative_pin):
		self.kit = kit
		self.positive_pin = positive_pin
		self.negative_pin = negative_pin

	def move(self, speed):
		if speed is not None and (speed > 1.0 or speed < -1.0):
			raise ValueError("Throttle must be None or between -1.0 and +1.0")
		
		if speed is None:
			positiveValue = 0
			negativeValue = 0
		elif speed == 0:
			positiveValue = 1
			negativeValue = 1
		else:
			if speed > 0:
				positiveValue = speed
				negativeValue = 0
			else:
				positiveValue = 0
				negativeValue = speed

		print(positiveValue, negativeValue)

		self.kit.continuous_servo[self.positive_pin].throttle = positiveValue
		self.kit.continuous_servo[self.negative_pin].throttle = negativeValue

class Robot:
	def __init__(self, flipperPin, lowerHatchPin, upperHatchPin, motorLeftPins, motorRightPins):
		self.kit = self.setupI2C()

		self.flipper = Servo(self.kit, flipperPin)
		self.lowerHatch = Servo(self.kit, lowerHatchPin)
		self.upperHatch = Servo(self.kit, upperHatchPin)
		self.motorLeft = Motor(self.kit, motorLeftPins[0], motorLeftPins[1])
		self.motorRight = Motor(self.kit, motorRightPins[0], motorRightPins[1])

	def testServo(self):
		self.upperHatch.moveRange(180)
		time.sleep(1)
		self.lowerHatch.moveRange(180)
		time.sleep(1)
		self.upperHatch.moveRange(0)
		time.sleep(1)
		self.lowerHatch.moveRange(0)

	def setupI2C(self):
		print("Initialising I2C Bus")
		i2c_bus = (busio.I2C(board.SCL_1, board.SDA_1))
		print("Initialising ServoKit")
		return ServoKit(channels=16, i2c=i2c_bus)
			
def startViewer():
	return
	   
