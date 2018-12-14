
import bme280
import machine
from machine import Pin
try:
  import usocket as socket
except:
  import socket
import time
import gc
host="192.168.10.19"
port=100
s=None
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
bme = bme280.BME280(i2c=i2c)

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET = Address family IPv4. SOCK_STREAM = TCP


while True:
            various = bme.read_compensated_data()
            temp = ("{}C".format(various[0] / 100))
            print(temp)
            p = various[1] // 255
            pi = p // 100
            pd = p - pi * 100
            press = ("{}.{:02d}hPa".format(pi, pd))
            print(press)
            hi = various[2] // 1024
            hd = various[2] * 100 // 1024 - hi * 100
            humid = ("{}.{:02d}%".format(hi, hd))
            print(humid)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET = Address family IPv4. SOCK_STREAM = TCP
            s.connect((host,port)) #the adress and port of the target socket
            s.send("Temp = " +str (temp))
            s.close()
            gc.collect()
            #temp = bme.values[0]
            #press = bme.values[1]
            #humid = bme.values[2]
            
            print("I've made it this far")
            time.sleep_ms(5000)
