#!/usr/bin/env/ python2
import serial
import time
import random
"""
Successful connection
"""

def setupComm(port, baudrate):
    ser = serial.Serial(port, baudrate, timeout=1)
    ser.reset_input_buffer()
    return ser

def receiveFromArd(ser):
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        return line
    else: # If nothing
        print("-1 -1 -1 -1 -1")
        return "-1 -1 -1 -1 -1"


def sendToArd(ser, data):
    #print("Sending: "+str(data))
    ser.write(data+b"\n")
