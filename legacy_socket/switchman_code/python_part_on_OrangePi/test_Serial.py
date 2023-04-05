#!/bin/python3
import serial
import time
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()
while True:
    port = input(' -> ')
    ser.write((port+"\n").encode('utf-8'))
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    time.sleep(1)
