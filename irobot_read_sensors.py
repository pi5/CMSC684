import serial
from time import sleep
import struct

# Open the serial port to communicate with iris gateway
# default port is /dev/ttyUSB1, but it can cange based on
# which port was avaliable when you plugged in the device.
# 57600 is the default serial speed for iris mote.
ser = serial.Serial('/dev/ttyUSB1', 57600, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=0)
print ser.name

# Send serial command that the iRobot can understand check
# the "iRobot Create Open Interface_v2.pdf" for more info
# the commands that can be used to control the robot.

ser.write(chr(128)) # 128 is Start command
ser.write(chr(131)) # 131 is Safe mode command

# Request to real all sensors
ser.write(chr(142))
# ser.write(chr(3))
ser.write(chr(7))
# ser.write(chr(9))
# ser.write(chr(13))

# The response from iRobot is 52 bytes long
x = ser.read()
count = 0
#print int(x[0])
for i in x:

    print "byte:" + str(count)
    # print format(255,i);
    print struct.unpack('B', i)[0]
    count = count + 1

# close the serial port
ser.close
