import serial
from uservo import UartServoManager
import argparse
import os
import sys
import winsound

SERVO_PORT_NAME =  'COM13'		
SERVO_BAUDRATE = 115200			
SERVO_1_ID = 3   # Angle of directionality
SERVO_2_ID = 6   # Angle of incidence
DANGERZONE = False

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

# Get current servo angle rounded to the nearest multiple of 15 degrees
def getCurrentAngle(uservo):
	return 15 * round(uservo.query_servo_angle(SERVO_1_ID) / 15)

# Rotate servo 90 degrees counterclockwise
def resetOffset(uservo):
	uservo.set_wheel_time(SERVO_1_ID, interval=2000, is_cw=False, mean_dps=287.5, is_wait=True)

# Rotate servo 90 degrees clockwise
def setOffset(uservo):
	uservo.set_wheel_time(SERVO_1_ID, interval=2000, is_cw=True, mean_dps=287.5, is_wait=True)

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

def manualInput():
	# Optionally make manual servo angle adjustments in case of inacurracies
	cmd = input('Manually adjust rotational angle? (y/n): ')
	while cmd != 'n':
		if cmd == 'y':
			angle = int(input('Enter rotational angle: '))
			setAngle(uservo, *angles[angle])
		if cmd == 'reset':
			resetOffset(uservo)
		cmd = input('Manually adjust rotational angle? (y/n): ')

if __name__=='__main__':
	### PROGRAM INIT ###
	parser = argparse.ArgumentParser()
	parser.add_argument('-r', '--reset_offset', action='store_true')
	parser.add_argument('-i', '--incident_angle', type=int, nargs=1, default=[-1])
	parser.add_argument('-f', '--file', type=str, nargs=1, default=[''])
	parser.add_argument('-skip', '--skip', type=int, nargs=1, default=[-1])
	args = parser.parse_args()
	
	uart = serial.Serial(port=SERVO_PORT_NAME, baudrate=SERVO_BAUDRATE,\
						parity=serial.PARITY_NONE, stopbits=1,\
						bytesize=8,timeout=0)
	uservo = UartServoManager(uart, is_debug=True)

	# If set flag is set, return servo to custom position specified by user
	if not args.incident_angle[0] < 0:
		if abs(incident_angles[args.incident_angle[0]] - uservo.query_servo_angle(SERVO_2_ID)) > 2.0:
			setIncidentAngle(uservo, incident_angles[args.incident_angle[0]])
		exit()

	if args.reset_offset:
		resetOffset(uservo)
		exit()

	# Set the servo to neutral state
	setAngle(uservo, angles[180][0])

	### PROGRAM START ###
	waitForInput('Press enter to start: ')

	filename = args.file[0] + '_order.txt'
	f = open(os.path.join(sys.path[0], 'orders', filename), encoding = "utf8")
	
	# Determine starting line in file
	if args.skip[0] > 0:
		for i in range(args.skip[0] + 1):
			next(f)
	else:
		next(f)

	# Execute samples
	sample_count = 0
	for line in f:
		sample = line.strip().split(',')
		target_angle = int(sample[2])
		target_angle_mapped = angles[int(sample[2])][0]
		offset = angles[int(sample[2])][1]

		print('\n' + str(sample_count % 60 + 1) + '# sample ' + str(sample))
	
		# Reset the offset if it was set previously
		while DANGERZONE:
			print('Resetting offset, please wait...')
			resetOffset(uservo)
			DANGERZONE = False

		# Rotate the servo to the right angle
		# print('Setting rotational angle to ' + str(target_angle) + ' degrees')
		while(getCurrentAngle(uservo) != target_angle_mapped):
			setAngle(uservo, target_angle_mapped)

		# If offset is set, move the servo an additional 90 degrees in the specified direction
		if offset:
			print('Setting offset, please wait...')
			# uservo.set_wheel_time(SERVO_1_ID, interval=2000, is_cw=(angle >= 0), mean_dps=287.5)
			uservo.set_wheel_time(SERVO_1_ID, interval=2000, is_cw=True, mean_dps=287.5)
			DANGERZONE = True

		# manualInput()

		print('Current angle: ', target_angle)
		# notify()

		# Continue to next sample
		waitForInput('Press enter for the next sample: ')
	
		sample_count += 1

	f.close()
	