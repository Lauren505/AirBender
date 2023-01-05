import serial
from uservo import UartServoManager
import argparse
import os
import sys
import winsound

SERVO_PORT_NAME =  'COM26'		
SERVO_BAUDRATE = 115200			
SERVO_1_ID = 3   	# Angle of directionality
# SERVO_2_ID = 6   	# Angle of incidence
SERVO_2_ID = 0   	# Angle of incidence
UNDEFINED = -1

angles = {
	0 : (-120, False), 
	15 : (-105, False),
	22.5 : (-98.5, False),
	30 : (-90, False),
	45 : (-75, False),
	60 : (-60, False),
	67.5 : (-53.5, False),
	75 : (-45, False),
	90 : (-30, False),
	105 : (-15, False),
	112.5 : (-8.5, False),
	120 : (0, False),
	135 : (15, False),
	150 : (30, False),
	157.5 : (37.5, False),
	165 : (45, False),
	180 : (60, False),
	195 : (75, False),
	202.5 : (82.5, False),
	210 : (90, False),
	225 : (105, False),
	240 : (120, False),
	247.5 : (128.5, False),
	255 : (135, False),
	270 : (150, False),
	285 : (75, True),
	292.5 : (82.5, True),
	300 : (90, True),
	315 : (105, True),
	330 : (-150, False),
	337.5 : (-142.5, False),
	345 : (-135, False)
}

# 0 => PARALLEL, 90 => PERPENDICULAR
incident_angles = {
	0 : 0,
	30 : -35,
	60 : -60,
	90 : -90
}

# OLD SERVO
# incident_angles = {
# 	# OLD SERVO
# 	0 : 135,
# 	30 : 107,
# 	# 30 : 105,
# 	# 60 : 75,
# 	60 : 82,
# 	90 : 52,
# 	# 90 : 45
# }

# Get current servo angle rounded to the nearest multiple of 15 degrees
def getCurrentAngle(uservo):
	return 15 * round(uservo.query_servo_angle(SERVO_1_ID) / 15)

def getNextAngle(idx):
	return targets[idx + 1][1] if idx < len(targets) - 1 else UNDEFINED

def getPreviousAngle(idx):
	return targets[idx - 1][1] if idx > 0 else UNDEFINED

# Rotate servo 90 degrees counterclockwise
def resetOffset(uservo):
	# uservo.set_wheel_time(SERVO_1_ID, interval=2000, is_cw=False, mean_dps=287.5, is_wait=True)
	uservo.set_wheel_time(SERVO_1_ID, interval=1500, is_cw=False, mean_dps=500.0, is_wait=False)

# Rotate servo 90 degrees clockwise
def setOffset(uservo):
	# uservo.set_wheel_time(SERVO_1_ID, interval=2000, is_cw=True, mean_dps=287.5, is_wait=True)
	uservo.set_wheel_time(SERVO_1_ID, interval=1500, is_cw=True, mean_dps=500.0, is_wait=False)

# Set the rotational angle of the servo
def setAngle(uservo, angle):
	if getCurrentAngle(uservo) != angle:
		uservo.set_servo_angle(SERVO_1_ID, angle, interval=0)
		uservo.wait()

# Set the incidental angle of the servo
def setIncidentAngle(uservo, angle):
	uservo.set_servo_angle(SERVO_2_ID, angle, interval=0)
	uservo.wait()

# Pause the program until `Enter` is pressed
def waitForInput(message):
	cmd = input(message)
	while cmd != '':
		cmd = input(message)

# Notify participant
def notify():
	waitForInput('Press enter to notify participant: ')
	winsound.Beep(1000, 600)  # Beep at 1000 Hz for 600 ms

if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-r', '--reset_offset', action='store_true')
	parser.add_argument('-s', '--set_angle', type=float, nargs=2, default=[UNDEFINED, UNDEFINED])
	parser.add_argument('-f', '--file', type=int, nargs=2, default=[UNDEFINED, UNDEFINED])
	parser.add_argument('-skip', '--skip', type=int, nargs=1, default=[0])
	args = parser.parse_args()
	
	uart = serial.Serial(port=SERVO_PORT_NAME, baudrate=SERVO_BAUDRATE,\
						parity=serial.PARITY_NONE, stopbits=1,\
						bytesize=8,timeout=0)
	uservo = UartServoManager(uart, is_debug=True)

	# Code for setting custom angles
	if not args.set_angle[0] == UNDEFINED and not args.set_angle[1] == UNDEFINED:
		setAngle(uservo, angles[args.set_angle[0]][0])
		setIncidentAngle(uservo, incident_angles[args.set_angle[1]])
		exit()

	if args.reset_offset:
		resetOffset(uservo)
		exit()

	# Initialize system
	user_index, incident_angle = str(args.file[0]), str(args.file[1])
	setAngle(uservo, angles[180][0])

	# Open file
	waitForInput('Press enter to start: ')
	filename = user_index + '\\' + user_index + '_' + incident_angle + 'deg_order.txt'
	f = open(os.path.join(sys.path[0], 'orders', filename), encoding = "utf8")
	next(f)

	# Preparse file
	targets = []
	for line in f:
		sample = line.strip().split(',')
		targets.append((sample[0], float(sample[2])))

	# Execute samples
	sample_count = args.skip[0]
	previous_angle = 180
	for target in targets[args.skip[0]:]:
		focal_point = target[0]
		target_angle = target[1]
		target_angle_mapped, offset = angles[target_angle]

		print('\n' + str(sample_count % 60 + 1) + '# sample: ' + focal_point + ", " + str(target_angle))
		
		if not target_angle == getPreviousAngle(sample_count):
			# Rotate the servo to specified angle
			setAngle(uservo, target_angle_mapped)

			# Add 90 degree offset if the target angle is 285, 300 or 315
			if offset:
				setOffset(uservo)

		# notify() TODO uncomment this

		# Continue to next sample
		waitForInput('Press enter for the next sample: ')

		# Reset the offset if it was set previously
		if offset and not target_angle == getNextAngle(sample_count):
			print("Resetting offset")
			resetOffset(uservo)
			uservo.wait()
			setAngle(uservo, angles[180][0])
	
		sample_count += 1

	f.close()

	setAngle(uservo, angles[180][0])
