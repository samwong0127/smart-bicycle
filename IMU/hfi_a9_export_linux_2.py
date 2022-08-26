#!/usr/bin/env python
# -*- coding:utf-8 -*-
import serial
import struct
import platform
import serial.tools.list_ports
import math
import time
import pandas as pd

# This file is compatible with python 2.7 and 3.7 in rapsberry pi 4B


def printSerialData(acceleration, angularVelocity, angle_degree, magnetometer):
    
    print('''
		加速度(m/s²)：
			x轴：%.2f
			y轴：%.2f
			z轴：%.2f

		角速度(rad/s)：
			x轴：%.2f
			y轴：%.2f
			z轴：%.2f

		欧拉角(°)：
			x轴：%.2f
			y轴：%.2f
			z轴：%.2f

		磁场：
			x轴：%.2f
			y轴：%.2f
			z轴：%.2f
		''' % (acceleration[0] * -9.8, acceleration[1] * -9.8, acceleration[2] * -9.8,
			   angularVelocity[0], angularVelocity[1], angularVelocity[2],
			   angle_degree[0], angle_degree[1], angle_degree[2],
			   magnetometer[0], magnetometer[1], magnetometer[2]
			  ))
		
# Similar to above one but different in parameters
def printSerialData2(dataPrev, dataCur):
    print('''
		加速度(m/s²):
			x-axis: %.2f
			y-axis: %.2f
			z-axis: %.2f

		角速度(rad/s):
			x-axis: %.2f
			y-axis: %.2f
			z-axis: %.2f

		Euler angles Cur(°):
			x-axis: %.2f
			y-axis: %.2f
			z-axis: %.2f

		Euler angles Prev(°):
			x-axis: %.2f
			y-axis: %.2f
			z-axis: %.2f
		''' % (dataCur['x-acc'], dataCur['y-acc'], dataCur['z-acc'],
			   dataCur['x-aVec'], dataCur['y-aVec'], dataCur['z-aVec'],
			   dataCur['x-EDeg'], dataCur['y-EDeg'], dataCur['z-EDeg'],
			   dataPrev['x-EDeg'], dataPrev['y-EDeg'], dataPrev['z-EDeg']
			  ))

# 查找 ttyUSB* 设备
def find_ttyUSB():
    print('imu 默认串口为 /dev/ttyUSB0, 若识别多个串口设备, 请在 launch 文件中修改 imu 对应的串口')
    posts = [port.device for port in serial.tools.list_ports.comports() if 'USB' in port.device]
    print('当前电脑所连接的 {} 串口设备共 {} 个: {}'.format('USB', len(posts), posts))


# crc 校验
def checkSum(list_data, check_data):
    data = bytearray(list_data)
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return hex(((crc & 0xff) << 8) + (crc >> 8)) == hex(check_data[0] << 8 | check_data[1])


# 16 进制转 ieee 浮点数
def hex_to_ieee(raw_data):
    ieee_data = []
    raw_data.reverse()
    for i in range(0, len(raw_data), 4):
        data2str =hex(raw_data[i] | 0xff00)[4:6] + hex(raw_data[i + 1] | 0xff00)[4:6] + hex(raw_data[i + 2] | 0xff00)[4:6] + hex(raw_data[i + 3] | 0xff00)[4:6]
        if python_version == '2':
            ieee_data.append(struct.unpack('>f', data2str.decode('hex'))[0])
        if python_version == '3':
            ieee_data.append(struct.unpack('>f', bytes.fromhex(data2str))[0])
    ieee_data.reverse()
    return ieee_data


# 处理串口数据
def handleSerialData(raw_data):
    global buff, key, angle_degree, magnetometer, acceleration, angularVelocity, pub_flag
    if python_version == '2':
        buff[key] = ord(raw_data)
    if python_version == '3':
        buff[key] = raw_data

    key += 1
    if buff[0] != 0xaa:
        key = 0
        return
    if key < 3:
        return
    if buff[1] != 0x55:
        key = 0
        return
    if key < buff[2] + 5:  # 根据数据长度位的判断, 来获取对应长度数据
        return

    else:
        data_buff = list(buff.values())  # 获取字典所以 value

        if buff[2] == 0x2c and pub_flag[0]:
            if checkSum(data_buff[2:47], data_buff[47:49]):
                data = hex_to_ieee(data_buff[7:47])
                angularVelocity = data[1:4]
                acceleration = data[4:7]
                magnetometer = data[7:10]
            else:
                print('校验失败')
            pub_flag[0] = False
        elif buff[2] == 0x14 and pub_flag[1]:
            if checkSum(data_buff[2:23], data_buff[23:25]):
                data = hex_to_ieee(data_buff[7:23])
                angle_degree = data[1:4]
            else:
                print('校验失败')
            pub_flag[1] = False
        else:
            print("该数据处理类没有提供该 " + str(buff[2]) + " 的解析")
            print("或数据错误")
            buff = {}
            key = 0

        buff = {}
        key = 0
        if pub_flag[0] == True or pub_flag[1] == True:
            return
        pub_flag[0] = pub_flag[1] = True
        #acc_k = math.sqrt(acceleration[0] ** 2 + acceleration[1] ** 2 + acceleration[2] ** 2)

        printSerialData(acceleration, angularVelocity, angle_degree, magnetometer)
		# Output logged data
        outputDict = {
            'x-acc':acceleration[0] * -9.8, 
            'y-acc':acceleration[1] * -9.8, 
            'z-acc':acceleration[2] * -9.8,
            'x-aVec':angularVelocity[0], 
            'y-aVec':angularVelocity[1], 
            'z-aVec':angularVelocity[2],
            'x-EDeg':angle_degree[0], 
            'y-EDeg':angle_degree[1], 
            'z-EDeg':angle_degree[2]
        }

        return outputDict




key = 0
flag = 0
buff = {}
angularVelocity = [0, 0, 0]
acceleration = [0, 0, 0]
magnetometer = [0, 0, 0]
angle_degree = [0, 0, 0]
pub_flag = [True, True]

python_version = platform.python_version()[0]

def IMU():
    
    find_ttyUSB()
    """
	May need to change port
	"""
    port = "/dev/ttyUSB0"
    baudrate = 921600

    try:
        hf_imu = serial.Serial(port=port, baudrate=baudrate, timeout=0.5)
        if hf_imu.isOpen():
            print("\033[32m串口打开成功...\033[0m")
        else:
            hf_imu.open()
            print("\033[32m打开串口成功...\033[0m")
    except Exception as e:
        print(e)
        print("\033[31m串口打开失败\033[0m")
        exit(0)
    else:
        dataPrev = {}
        c = 0
        try:
            while True:
                try:
                    buff_count = hf_imu.inWaiting()
                    
                except Exception as e:
                    print("exception:" + str(e))
                    print("imu 失去连接，接触不良，或断线")
                    c = 0
                    exit(0)
                else:
                    if buff_count > 0:
                        buff_data = hf_imu.read(buff_count)
                        for i in range(0, buff_count):
                            if c == 0:
                                dataPrev = handleSerialData(buff_data[i])
                                dataCur = dataPrev
                            else:
                                dataPrev = dataCur
                                dataCur = handleSerialData(buff_data[i])
                                
                                """
                                Do prediction,
                                control the led light,
                                send signal to Arduinos here
                                
                                """
                            c += 1
							
						#time.sleep(1)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            c = 0



if __name__ == "__main__":
    python_version = platform.python_version()[0]
    find_ttyUSB()
    """
	May need to change the port
	"""
    port = "/dev/ttyUSB0"
    """
    Try to change baudrate to lower the speed of data to be sent.
    In arduino you can use 300, 600, 1200, 2400, 4800, 9600, 14400, 
        19200, 28800, 38400, 57600, or 115200.
    """
    baudrate = 921600

    try:
        hf_imu = serial.Serial(port=port, baudrate=baudrate, timeout=0.5)
        if hf_imu.isOpen():
            print("\033[32m串口打开成功...\033[0m")
        else:
            hf_imu.open()
            print("\033[32m打开串口成功...\033[0m")
    except Exception as e:
        print(e)
        print("\033[31m串口打开失败\033[0m")
        exit(0)
    else:
        #dataPrev = {}
        c = 0
        try:
            while True:
                try:
                    buff_count = hf_imu.inWaiting()
                    
                except Exception as e:
                    print("exception:" + str(e))
                    print("imu 失去连接，接触不良，或断线")
                    c = 0
                    exit(0)
                else:
                    if buff_count > 0:

                        buff_data = hf_imu.read(buff_count)

                        output_at_once = pd.DataFrame()
                        for i in range(0, buff_count):
                            output = handleSerialData(buff_data[i])
                            if output is not None:
                                output_at_once = output_at_once.append(output, ignore_index=True)
                        if output_at_once.empty:
                            #print('output_at_once is empty')
                            asdasdf = 1 # Do nothing
                        else:
                            dictToResult = {}
                            # Group the data into one row with their mean
                            for col in output_at_once:
                                dictToResult[col] = output_at_once[col].mean()
                            
                            if c == 0:
                                dataPrev = dictToResult
                                dataCur = dataPrev
                            else:
                                dataPrev = dataCur
                                dataCur = dictToResult
                            c += 1
                            printSerialData2(dataPrev, dataCur)

                            """
                            Do prediction,
                            Control LED light,
                            Signal the motor,
                            Here?
                            """
			            #time.sleep(1)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            c = 0