from umqtt.simple import MQTTClient
from machine import UART
import machine
import ubinascii
import uselect

import time

#led = Pin(12, Pin.OUT)
#button = Pin(13, Pin.IN)

#topselect = 0
#topic = ["Sensor 1", "Sensor 2", "Sensor 3"]

READ_ONLY = uselect.POLLIN
uart = UART(2, 9600)
uart.init(9600, 8, None, 1)
allpoll = uselect.poll() # creates uselect.poll class under the name webpol
allpoll.register(uart, READ_ONLY)


# Modify below section as required
CONFIG = {"MQTT_BROKER": "192.168.1.104","USER": "","PASSWORD": "","PORT": 1883,"TOPIC": b"test","CLIENT_ID": b"esp8266_" + ubinascii.hexlify(machine.unique_id())
}
 
# Method to act based on message received   
def onMessage(topic, msg): # Add some sort of message that i can reset the ESP with when the database dies
    print("Topic: %s, Message: %s" % (topic, msg))

    #if msg == b"on":
       # pin.off()
       # led.on()
 
    #elif msg == b"off":
       # pin.on()
        #led.off()

      
def listen():
    #Create an instance of MQTTClient 
    client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'], port=CONFIG['PORT'])
    # Attach call back handler to be called on receiving messages
    client.set_callback(onMessage)
    client.connect()
    client.publish(CONFIG['TOPIC'], "ESP8266 is Connected")
    #client.publish(CONFIG['TOPIC'], "off")
    #client.subscribe(CONFIG['TOPIC'])
    print("ESP8266 is Connected to %s and subscribed to %s topic" % (CONFIG['MQTT_BROKER'], CONFIG['TOPIC']))
    #wind.start_timer()
    #print("Timer started")

    while True:
            
            events = allpoll.ipoll(1250, 1)
            for event in events:
                #print(event) 
                print("this is the event")
                #print(event[0])
                #print(globals())
                time.sleep_us(200)
                event_type = (str(event[0])[0:4])
                print(event_type)
                try_stuff(event_type, allpoll, client)


def try_stuff(event_type, allpoll, client):      
            if event_type == "UART" :
                uartlive(allpoll, client)
         
            else:
                time.sleep_us(500)
                #listen()

def humanline(sens, u_bytes): #parses the uart data that can be converted directly from HEX
    raw = (sens)
    man = str(raw[0:3])
    serial = str(raw[4:13])
    pump_cycle = int((raw[22:28]), 16)
    pump_time = int((raw[29:37]), 16)
    days_pumped = int((raw[38:42]), 16)
    alm_activs = int((raw[43:47]), 16)
    alarm_time = int((raw[48:56]), 16)
    relay_on = raw[57]
    total_time = int((raw[59:67]), 16)
    switch_config = raw[68]
    is_alarmed = raw[74]
    is_pumping = raw[72]
    # = [x - 0x20 for x in raw]
    
    raws = u_bytes[14:21]       #parses uart data that needs the offset of 0x20 
    ws = u_bytes[70]
    #print(raws)
    man_day = str((raws[0]) - 0x20)
    #print(raws[1])
    man_mo = str((raws[1]) - 0x20)
    man_yr = str((raws[2]) - 0x20)
    inst_day = str((raws[4]) - 0x20)
    inst_mo = str((raws[5]) - 0x20)
    inst_yr = str((raws[6]) - 0x20)
    water_level_mm = str((ws) - 0x20)
    if inst_yr == "0":
        inst_yr = "00"
    man_date = str(man_day)+"-"+str(man_mo)+"-20"+str(man_yr)       #builds date string
    inst_date = str(inst_day)+"-"+str(inst_mo)+"-20"+str(inst_yr)
    #Next line builds the MQTT string 
    human = ("Sensor 1", str(man), str(serial), str(man_date), str(inst_date), str(pump_cycle), str(pump_time), str(days_pumped), str(alm_activs), str(alarm_time), str(relay_on), str(total_time), str(switch_config), str(water_level_mm), str(is_alarmed), str(is_pumping))
    #print("hello")
    time.sleep_us(200)
    return human

def uartlive(allpoll, client):
    u_bytes = uart.readline()
    sens = (u_bytes.decode('ascii'))
    print("made it so far")
    print(sens)
    human = humanline(sens, u_bytes)
    print(human)
    client.publish("test", str(human))          #should set this out as a TRY operator if it fails go back to Listen
                                                # if that goes wrong too? Try reconnecting to the wifi!
    #split = sens.split(';')
    #split.insert(0, "Sensor 1")
    allpoll.modify(uart, 1)
    
    
    #if split[1] == "####\r\n" :
    time.sleep_us(200)
        
    #else:    
        #print(split)
        #time.sleep_us(200)
        
    

listen() 
