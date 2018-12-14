
# This file is executed on every boot (including wake-boot from deepsleep)

#import esp

#esp.osdebug(None)

import gc

#import webrepl
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('Ghost_NET2.4', 'NeighboursAreCunts')
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig())
#webrepl.start()

gc.collect()



