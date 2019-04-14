# Send a command to Arduino and wait the confirmation for
# command executed or eeror
import serial
import sys

# Define the serial port

# USB Serial port
ser = serial.Serial('/dev/ttyACM0',9600)
s = [0, 1]

# Get the command parameter
command = sys.argv[1]

# Initialize the serial port and clean the input buffer
ser.flushInput()

# Send the command
ser.write(b'A')

commandOk = False

# Wait confirm from Arduino
print("Waiting for an answer")

readOk = False
while readOk is not True:
    s[0] = str(int (ser.readline()))
    # print(s[0])
    print("read serial")
    readOk = True
