from ast import arg
import serial
from uservo import UartServoManager
import argparse

SERVO_PORT_NAME =  'COM4'		
SERVO_BAUDRATE = 115200			
SERVO_1_ID = 3   # Angle of directionality
SERVO_2_ID = 6   # Angle of incidence

angles = {
	0 : (-120, False), 
	15 : (-105, False), 
	30 : (-90, False),
	45 : (-75, False),
	60 : (-60, False),
	75 : (-45, False),
	90 : (-30, False),
	105 : (-15, False),
	120 : (0, False),
	135 : (15, False),
	150 : (30, False),
	165 : (45, False),
	180 : (60, False),
	195 : (75, False),
	210 : (90, False),
	225 : (105, False),
	240 : (120, False),
	255 : (135, False),
	270 : (60, True),
	285 : (75, True),
	300 : (90, True),
	315 : (105, True),
	330 : (120, True),
	345 : (135, True)
}

# 0 => PARALLEL, 90 => PERPENDICULAR
incident_angles = {
	0 : 135,
	30 : 105,
	60 : 75,
	90 : 45
}

def resetOffset(uservo):
	uservo.set_wheel_time(SERVO_1_ID, interval=2000, is_cw=False, mean_dps=287.5)

# Example use setAngle(uservo, *DEG_0)
def setAngle(uservo, angle, offset):
	# Move the servo to the relative angle specified by the second parameter
	uservo.set_servo_angle(SERVO_1_ID, angle, interval=0)
	uservo.wait()
	
	# If offset is set, move the servo an additional 90 degrees in the specified direction
	if offset:
		# uservo.set_wheel_time(SERVO_1_ID, interval=2000, is_cw=(angle >= 0), mean_dps=287.5)
		uservo.set_wheel_time(SERVO_1_ID, interval=2000, is_cw=True, mean_dps=287.5)

def setIncidentAngle(uservo, angle):
	uservo.set_servo_angle(SERVO_2_ID, angle, interval=0)
	uservo.wait()

if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-r', '--reset_angle', type=str, nargs=1, default=['0'])
	parser.add_argument('-i', '--incident_angle', type=int, nargs=1, default=[-1])
	parser.add_argument('-a', '--angle', type=int, nargs=1, default=[180])

	args = parser.parse_args()
	
	uart = serial.Serial(port=SERVO_PORT_NAME, baudrate=SERVO_BAUDRATE,\
						parity=serial.PARITY_NONE, stopbits=1,\
						bytesize=8,timeout=0)
	uservo = UartServoManager(uart, is_debug=True)

	print(args.angle[0], args.reset_angle[0])

	# IF PREVIOUS DEGREE >= 270 RESET THE OFFSET
	if args.reset_angle[0] == '1':
		resetOffset(uservo)

	if not args.incident_angle[0] < 0:
		setIncidentAngle(uservo, incident_angles[args.incident_angle[0]])

	setAngle(uservo, *angles[args.angle[0]])
	