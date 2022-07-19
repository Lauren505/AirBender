import argparse
from fileinput import filename
import sys
sys.path.append("./")
import time
import struct
import serial
from uservo import UartServoManager

focal_points = ['A', 'B', 'C', 'D', 'E']
angle_of_incidence = ['0', '30', '60']
directions = ['0', '15', '30', '45', '60', '75', '90', '105', '120', '135', '150', '165', '180', '195', '210', '225', '240', '255', '270', '285', '300', '315', '330', '345']
orders = []

SERVO_PORT_NAME =  'COM4'		
SERVO_BAUDRATE = 115200			
SERVO_1_ID = 0   # control angle of incidence
SERVO_2_ID = 0   # control angle of direction	
SERVO_HAS_MTURN_FUNC = False	

def set_angle(uservo, inc_angle, dir_angle, wait_time):
	uservo.set_servo_angle(SERVO_1_ID, inc_angle, interval=0)
	uservo.wait()
	print("-> {}".format(uservo.query_servo_angle(SERVO_1_ID)))
	uservo.set_servo_angle(SERVO_2_ID, dir_angle, interval=0)
	uservo.wait()
	print("-> {}".format(uservo.query_servo_angle(SERVO_2_ID)))
	time.sleep(wait_time) # waiting time

def read_file(filename):
	with open(filename) as f:
		header = f.readline()
		for line in f:
			orders.append(line.strip('\n').split(','))
	print(orders)

def servo(uservo):
	for i, s in enumerate(orders):
		inc_angle = int(s[1])
		dir_angle = 0 if inc_angle==0 else int(s[2])

		if i<(len(orders)-1) and s[0]==orders[i+1][0]:
			set_angle(uservo, inc_angle, dir_angle, 10)
		else:
			set_angle(uservo, inc_angle, dir_angle, 30)

if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--filename', type=str)
	args = parser.parse_args()

	uart = serial.Serial(port=SERVO_PORT_NAME, baudrate=SERVO_BAUDRATE,\
						parity=serial.PARITY_NONE, stopbits=1,\
						bytesize=8,timeout=0)
	uservo = UartServoManager(uart, is_debug=True)

	read_file(args.filename)
	servo(uservo)