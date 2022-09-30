from multiprocessing.connection import wait
import serial
from uservo import UartServoManager
import argparse
import os
import sys
import winsound

SERVO_PORT_NAME =  'COM8'		
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

def setOffset(uservo):
	uservo.set_wheel_time(SERVO_1_ID, interval=2000, is_cw=True, mean_dps=287.5)

def setAngle(uservo, angle, offset):
	# Move the servo to the relative angle specified by the second parameter
	curr_angle = 15 * round(uservo.query_servo_angle(SERVO_1_ID) / 15)
	if curr_angle != angle:
		uservo.set_servo_angle(SERVO_1_ID, angle, interval=0)
		uservo.wait()
	
	# If offset is set, move the servo an additional 90 degrees in the specified direction
	if offset:
		# uservo.set_wheel_time(SERVO_1_ID, interval=2000, is_cw=(angle >= 0), mean_dps=287.5)
		uservo.set_wheel_time(SERVO_1_ID, interval=2000, is_cw=True, mean_dps=287.5)

def setIncidentAngle(uservo, angle):
	uservo.set_servo_angle(SERVO_2_ID, angle, interval=0)
	uservo.wait()

def waitForInput(message):
	cmd = input(message)
	while cmd != '':
		cmd = input(message)

if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--set_angles', type=int, nargs=2, default=[-1, -1])
	parser.add_argument('-f', '--file', type=str, nargs=1, default=[''])
	parser.add_argument('-skip', '--skip', type=int, nargs=1, default=[-1])

	args = parser.parse_args()
	
	uart = serial.Serial(port=SERVO_PORT_NAME, baudrate=SERVO_BAUDRATE,\
						parity=serial.PARITY_NONE, stopbits=1,\
						bytesize=8,timeout=0)
	uservo = UartServoManager(uart, is_debug=True)

	# If set flag is set, return servo to custom position specified by user
	if not args.set_angles[0] < 0 and not args.set_angles[1] < 0:
		if abs(incident_angles[args.set_angles[0]] - uservo.query_servo_angle(SERVO_2_ID)) > 2.0:
			setIncidentAngle(uservo, incident_angles[args.set_angles[0]])
		setAngle(uservo, *angles[args.set_angles[1]])
		exit()

	# Set the servo to initial resting state
	setAngle(uservo, *angles[180])

	# PROGRAM START
	waitForInput('Press enter to start: ')

	filename = args.file[0] + '_order.txt'
	f = open(os.path.join(sys.path[0], 'orders', filename), encoding = "utf8")
	
	if args.skip[0] > 0:
		for i in range(args.skip[0] + 1):
			next(f)
	else:
		next(f) # Skip first line of file

	sample_count = 0
	for line in f:
		sample = line.strip().split(',')
		angle = int(sample[2])

		print('\n' + str(sample_count % 40 + 1) + '# sample ' + str(sample))

		# Rotate the servo to the right angle
		print('Setting rotational angle to ' + str(angle) + ' degrees')
		setAngle(uservo, *angles[angle])

		# Optionally make manual servo angle adjustments in case of inacurracies
		cmd = input("Manually adjust rotational angle? (y/n)")
		while cmd != 'n':
			if cmd == 'y':
				angle = input("Enter rotational angle.")
				setAngle(uservo, *angles[angle])
			cmd = input("Manually adjust rotational angle? (y/n)")

		# Notify participant
		waitForInput('Press enter to notify participant: ')
		winsound.Beep(1000, 600)  # Beep at 1000 Hz for 600 ms

		# Continue to next sample
		waitForInput('Press enter for the next sample: ')

		# Reset the offset if previous angle >= 270
		if angle >= 270:
			print('\nResetting offset, please wait...')
			resetOffset(uservo)
			setAngle(uservo, *angles[180])

		sample_count += 1

	f.close()
	