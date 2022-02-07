
# System states
softInterrupts = [] # Tuple of form (time, callback) to execute callback at specified time

# Button press
buttonState = 0 # 0 = Sleep mode, 1 = First press; localise self, 2 = begin operation
def buttonPressInterrupt():
    buttonState = 0 if buttonState == 2 else buttonState+1

timer = 1 # Mock representation of timer

# Perform run
# gracePeriodLength: Amount of time to wait to start moving
#   - 0 for no grace period
# 
def runOperation(gracePeriodLength):

    # Wait for grace period
    while timer <= gracePeriodLength:
        Sleep(1) # Sleep 1 second
    
    
    while (True):
        # Check soft interrupts
        for interrupt in softInterrupts:
            # Rough mock of checking the time of the interrupt
            if interrupt[0] == now(): exec(interrupt[1])
            

# Process camera frame        
def processFrame():
    continue


# WIP: Motor control
    # Motor feedback control
    motor1Target = 0, motor2Target = 0
    def motorControl():
        continue

    # Drive robot
    # <left/right>Rotation: Amount to move motor
    # <left/right>Duration: Amount of time to take to move the motor
    motor1 = 0, motor2 = 1 # Mock representation of motor ESC controls
    def move(leftRotation, rightRotation, leftDuration, rightDuration):

        # Set PWM control for motors
        motor1Target = leftRotation
        motor2Target = rightRotation

        # Set interrupts to stop motors
        addSoftInterrupt(now()+leftDuration, stopMotor, motor1)
        addSoftInterrupt(now()+rightDuration, stopMotor, motor2)
   
    
def addSoftInterrupt(time, callback, *args):
    softInterrupts.append((time, callback, args))

def setMotorSpeed(motor, dutyCycle):
    io_write(motor, dutyCycle) # Mock method to write to IO

# Utility method to stop the control of a motor
def stopMotor(motor):
    io_write(motor, 0) # Mock method to write to IO
