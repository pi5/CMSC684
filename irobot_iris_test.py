# This python script will connect to the iris mote over
# the defined serial and send some iRobot commands that
# tells the iRobot to move forward.

# To use this script you need to have two iris motes
# programmed with the "iris2irobot" code.

import serial
from time import sleep
import struct

# Open the serial port to communicate with iris gateway
# default port is /dev/ttyUSB1, but it can cange based on
# which port was avaliable when you plugged in the device.
# 57600 is the default serial speed on the iris motes.
ser = serial.Serial('/dev/ttyUSB1', 57600, timeout=5)
print ser.name

# Send serial command that the iRobot can understand check
# the "iRobot Create Open Interface_v2.pdf" for more info
# the commands that can be used to control the robot.

ser.write(chr(128)) # 128 is Start command
ser.write(chr(131)) # 131 is Safe mode command

cmd_seq = [
"137 1 44 128 0",
"156 1 44",
"137 0 0 128 0"
]



#cmds = [137, 1, 244, 128, 0]
#cmds = [152, 17, 158, 5, 158, 251, 139, 2, 0, 0, 158, 5, 158, 251, 139, 0, 0, 0, 153]
for action in cmd_seq:
	cmds = action.split()
	for cmd in cmds:
		ser.write(chr(int(cmd)))



# ser.write(chr(137)) # Drive
# ser.write(chr(0))   # Velocity high byte (-500 ~ 500 mm/s)
# ser.write(chr(100)) # Velocity low byte
# ser.write(chr(128)) # Radius high byte (-2000 ~ 2000 mm)
# ser.write(chr(0))   # Radius low byte
#
# ser.write(chr(156))
# ser.write(chr(1))
# ser.write(chr(44))
# ser.write(chr(137))
# ser.write(chr(0))
# ser.write(chr(0))
# ser.write(chr(128))
# ser.write(chr(0))

print "done..."

# close the serial port
ser.close
