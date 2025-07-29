# coding=utf-8
import time
from typing import List, Optional
from smartpi.module import Uart3_funtions,base_driver


class app_funtion:
    #马达编码读取 port:连接M端口；
    def read_motor_code(port:bytes) -> Optional[bytes]:
        motor_str=[0xA0, 0x01, 0x01, 0xBE]           
        motor_str[0]=0XA0+port       
        response = Uart3_funtions.single_operate_sensor(motor_str)
        if response:
            return 0
        else:
            return -1
            
    #马达速度控制 port:连接M端口；speed:0~100
    def write_motor_speed(port:bytes,speed:bytes) -> Optional[bytes]:
        motor_str=[0xA0, 0x01, 0x02, 0x71, 0x00, 0xBE]           
        motor_str[0]=0XA0+port
        motor_str[4]=speed
        response = Uart3_funtions.single_operate_sensor(motor_str)
        if response:
            return 0
        else:
            return -1
            
    #马达速度编码控制 port:连接M端口；speed:0~100；code:0~65535
    def motor_servoctl(port:bytes,speed:bytes,code:int) -> Optional[bytes]:
        motor_str=[0xA0, 0x01, 0x04, 0x81, 0x00, 0x81, 0x00, 0x00, 0xBE]           
        motor_str[0]=0XA0+port
        motor_str[4]=speed
        motor_str[6]=code//256
        motor_str[7]=code%256
        response = Uart3_funtions.single_operate_sensor(motor_str)
        if response:
            return 0
        else:
            return -1
            
    #马达方向控制 port:连接M端口；dir:
    def write_motor_dir(port:bytes,direc:bytes) -> Optional[bytes]:
        motor_str=[0xA0, 0x01, 0x06, 0x71, 0x00, 0xBE]           
        motor_str[0]=0XA0+port
        motor_str[4]=direc
        response = Uart3_funtions.single_operate_sensor(motor_str)
        if response:
            return 0
        else:
            return -1

    #彩灯控制 port:连接P端口；command:0:关灯；1:红；2:绿；3:蓝；4:黄；5:紫；6:青；7:白
    def color_lamp_operate(port:bytes,command:bytes) -> Optional[bytes]:
        color_lamp_str=[0xA0, 0x05, 0x00, 0xBE]
        color_lamp_str[0]=0XA0+port
        color_lamp_str[2]=command
        response = Uart3_funtions.single_operate_sensor(color_lamp_str)
        if response:
            return 0
        else:
            return -1
        
    #触碰传感器 port:连接P端口
    def read_switch(port:bytes) -> Optional[bytes]:
        read_sw_str=[0xA0, 0x03, 0x01, 0xBE]
        read_sw_str[0]=0XA0+port   
        response = Uart3_funtions.single_operate_sensor(read_sw_str)
        if response:
            return 0
        else:
            return -1
            
    #光电读取 port:连接P端口；command:1:读取；2:开灯；3:关灯；
    def light_operate(port:bytes,command:bytes) -> Optional[bytes]:
        light_str=[0xA0, 0x02, 0x00, 0xBE]
        light_str[0]=0XA0+port
        light_str[2]=command 
        response = Uart3_funtions.single_operate_sensor(light_str)
        if response:
            return 0
        else:
            return -1

    #温湿度读取 port:连接P端口；command:0:读取湿度；1:读取温度；
    def humiture_operate(port:bytes,command:bytes) -> Optional[bytes]:
        humiture_str=[0xA0, 0x0C, 0x01, 0x71, 0x00, 0xBE]
        humiture_str[0]=0XA0+port
        humiture_str[2]=command 
        response = Uart3_funtions.single_operate_sensor(humiture_str)
        if response:
            return 0
        else:
            return -1

    #超声波读取 port:连接P端口；command:1:读取；
    def ultrasonic_operate(port:bytes,command:bytes) -> Optional[bytes]:
        ultrasonic_str=[0xA0, 0x06, 0x00, 0xBE]
        ultrasonic_str[0]=0XA0+port
        ultrasonic_str[2]=command 
        response = Uart3_funtions.single_operate_sensor(ultrasonic_str)
        if response:
            return 0
        else:
            return -1
            
    #舵机控制 port:连接P端口；command:
    def servo_operate(port:bytes,command:bytes,angle:bytes) -> Optional[bytes]:
        servo_str=[0xA0, 0x0E, 0x01, 0x71, 0x00, 0xBE]
        servo_str[0]=0XA0+port
        servo_str[2]=command
        servo_str[4]=angle
        response = Uart3_funtions.single_operate_sensor(servo_str)
        if response:
            return 0
        else:
            return -1


