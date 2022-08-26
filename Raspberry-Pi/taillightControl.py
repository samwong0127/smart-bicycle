#!/usr/bin/python
# -*- coding:utf-8 -*-
from ctypes import *
import time
import RPi.GPIO as GPIO

hspi = CDLL('./dev_hardware_SPI.so')
#hspi = CDLL('/home/pi/mu_code/dev_hardware_SPI.so')


T_disp = [0x18,0x3c,0x7E,0xFE,0x18,0x18,0x18,0x18]# Top Arrow
R_disp = [0x08, 0x0c, 0x0e, 0xff, 0xff, 0x0e, 0x0c, 0x08] # Right Arrow
L_disp = [0x10, 0x30, 0x70, 0xff, 0xff, 0x70, 0x30, 0x10] # Left Arrow
D_disp = [0x18, 0x18, 0x18, 0x18, 0xff, 0x7e, 0x3c, 0x18] # Down Arrow
None_disp = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]# None
All_disp = [0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE]#ALL


hspi.DEV_HARDWARE_SPI_begin("/dev/spidev0.0")
hspi.DEV_HARDWARE_SPI_ChipSelect(3)

class MAX7219:
    def __init__(self):
        self.cs_pin = 8
        GPIO.setmode(GPIO.BCM) # Choose BCM or BOARD
        GPIO.setwarnings(False)
        GPIO.setup(self.cs_pin, GPIO.OUT) # set a port/pin as an output

    def WriteByte(self, Reg):
        GPIO.output(self.cs_pin, 0)
        hspi.DEV_SPI_WriteByte(Reg)

    def Write(self, address1, dat1, address2, dat2):# dat1: 2nd and 4th, dat2: 1st and 3rd
        GPIO.output(self.cs_pin, 0)
        self.WriteByte(address1)
        self.WriteByte(dat1)
        self.WriteByte(address2)
        self.WriteByte(dat2)
        GPIO.output(self.cs_pin, 1)

    # Show none
    def Init(self):
        disp = [None_disp,]
        for i in range(1,9):
            self.Write(i, disp[0][i-1], i, disp[0][i-1] )
        time.sleep(1)

    # timeToSleep: time interval of the led signals, iterations: number of occurances of led signals
    def TurningRight(self, timeToSleep=0.2, iterations=4):
        if iterations < 1 or timeToSleep < 0:
            print('iterations must >= 1 and timeToSleep >= 0')
            return
        print("TurningRight")
        disp = [
            R_disp,
            None_disp,
        ]
        index = 0
        for t in range(iterations):
            if index == 0:
                for i in range(1, 9):
                    self.Write(i, disp[1][i-1], i, disp[0][i-1] )
                # Displaying something
                #time.sleep(0.1)
                index = 1
            else:
                for i in range(1, 9):
                    self.Write(i, disp[0][i-1], i, disp[1][i-1] )
                # Displaying something
                #time.sleep(0.1)
                index = 0
            time.sleep(timeToSleep)
        for i in range(1, 9):
            self.Write(i, disp[1][i-1], i, disp[1][i-1] )


    def TurningLeft(self, timeToSleep=0.2, iterations=4):
        if iterations < 1 or timeToSleep < 0:
            print('iterations must >= 1 and timeToSleep >= 0')
            return
        print("TurningLeft")
        disp = [
            L_disp,
            None_disp,
        ]
        index = 0
        for t in range(iterations):
            if index == 1:
                for i in range(1, 9):
                    self.Write(i, disp[1][i-1], i, disp[0][i-1] )
                # Displaying something
                #time.sleep(0.1)
                index = 0
            else:
                for i in range(1, 9):
                    self.Write(i, disp[0][i-1], i, disp[1][i-1] )
                # Displaying something
                #time.sleep(0.1)
                index = 1
            time.sleep(timeToSleep)
        for i in range(1,9):
            self.Write(i, disp[1][i-1], i, disp[1][i-1] )


    def SlowingDown(self, timeToSleep=0.2, iterations=4):
        if iterations < 1 or timeToSleep < 0:
            print('iterations must >= 1 and timeToSleep >= 0')
            return
        print('Slowing Down')
        disp = [
            None_disp,
            All_disp,
        ]
        index = 0
        for t in range(iterations):
            if index == 0:
                for i in range(1, 9):
                    self.Write(i, disp[1][i-1], i, disp[1][i-1] )
                # Displaying something
                #time.sleep(0.1)
                index = 1
            else:
                for i in range(1, 9):
                    self.Write(i, disp[0][i-1], i, disp[0][i-1] )
                # Displaying something
                #time.sleep(0.1)
                index = 0
            time.sleep(timeToSleep)
        for i in range(1,9):
            self.Write(i, disp[0][i-1], i, disp[0][i-1] )


if __name__ == '__main__':
    led = MAX7219()
    led.Init()
    led.TurningRight()
    time.sleep(1)
    led.TurningLeft()
    time.sleep(1)
    led.SlowingDown()
    time.sleep(1)
    led.Init()