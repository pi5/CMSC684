# This python script will connect to the iris mote over
# the defined serial and send some iRobot commands that
# tells the iRobot to move forward.

# To use this script you need to have two iris motes
# programmed with the "iris2irobot" code.

import serial
from time import sleep
import struct
import sys
import time

CELL_SIZE = 55

# Get two's complement of a number represented in 16 bit
def twos_compl(num):
    if num >= 0:
        return num

    else:
        num = -num
        return ((pow(2,16) - 1) & ~num) + 1

# Get high and low byte of a 16 bit word
def get_bytes(integer):
    return divmod(twos_compl(integer), 0x100)


# Function to get move forward command
def get_forward_command(distance=55, speed=20):

	dist_high, dist_low = get_bytes(distance*10)
	speed_high, speed_low = get_bytes(speed*10)

	drive = "137 " + str(speed_high) + " " + str(speed_low) + " 128 0 "
	wait = "156 " + str(dist_high) + " " + str(dist_low) + " "
	stop = "137 0 0 128 0"

	return drive + wait + stop


def forward_until_bump(speed=25):

	speed_high, speed_low = get_bytes(speed*10)

	drive = "137 " + str(speed_high) + " " + str(speed_low) + " 128 0 "
	wait = "158 5 "
	stop = "137 0 0 128 0"

	return drive + wait + stop


# Move forward until you bump and get travelled time
def get_bump_time():
	start_time = time.time()
	execute(forward_until_bump())
	get_sensor_value()
	end_time = time.time()
	execute(back_off())

	return (end_time - start_time)


def back_off(speed=-25, distance=-10):

	if (speed > 0):
		speed = -speed

	if distance > 0:
		distance = -distance

	speed_high, speed_low = get_bytes(speed*10)
	dist_high, dist_low = get_bytes(distance*10)

	drive_back = "137 " + str(speed_high) + " " + str(speed_low) + " 128 0 "
	wait_reverse = "156 " + str(dist_high) + " " + str(dist_low) + " "
	stop = "137 0 0 128 0"

	return drive_back + wait_reverse + stop

def get_left_command(angle=90, speed=25):

	angle_high, angle_low = get_bytes(angle)
	speed_high, speed_low = get_bytes(speed*10)

	drive = "137 " + str(speed_high) + " " + str(speed_low) +  " 0 1 "
	wait = "157 " + str(angle_high) + " " + str(angle_low) +  " "
	stop = " 137 0 0 128 0"

	return drive + wait + stop


def get_right_command(angle=-90, speed=25):

	if (angle > 0):
		angle = -angle

	angle_high, angle_low = get_bytes(angle)
	speed_high, speed_low = get_bytes(speed*10)

	drive = "137 " + str(speed_high) + " " + str(speed_low) +  " 255 255 "
	wait = "157 " + str(angle_high) + " " + str(angle_low) + " "
	stop = " 137 0 0 128 0"

	return drive + wait + stop


def get_uturn_command():
	return get_right_command() + " " + get_right_command()



def get_sensor_value():
	ser = serial.Serial('/dev/ttyUSB1', 57600, timeout=8)
	# print ser.name
	ser.write(chr(128)) # 128 is Start command
	ser.write(chr(132)) # 131 is Safe mode command, 132 is full mode
	action = "142 7"
	cmds = action.split()
	for cmd in cmds:
		ser.write(chr(int(cmd)))
		time.sleep(0.001)

	val = 0
	x = ser.read()
	for i in x:
		val = struct.unpack('B', i)[0]
		#print val

	ser.close

	return val


def execute(action):
	# Open the serial port to communicate with iris gateway
	# default port is /dev/ttyUSB1, but it can cange based on
	# which port was avaliable when you plugged in the device.
	# 57600 is the default serial speed on the iris motes.
	ser = serial.Serial('/dev/ttyUSB1', 57600, timeout=5)
	# print ser.name
	ser.write(chr(128)) # 128 is Start command
	ser.write(chr(132)) # 131 is Safe mode command

	cmds = action.split()
	for cmd in cmds:
		ser.write(chr(int(cmd)))
		time.sleep(0.01)

	ser.close



# print "done..."
