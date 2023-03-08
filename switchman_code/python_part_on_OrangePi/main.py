#!/bin/python3
import serial
import time
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()
while True:
    ser.write(b"P1\n")
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    time.sleep(1)
    ser.write(b"P4\n")
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    time.sleep(1)