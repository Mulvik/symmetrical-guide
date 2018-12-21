
# Complete project details at https://RandomNerdTutorials.com

#def web_page():
  #if led.value() == 1:
  #  gpio_state="ON"
  #else:
  #  gpio_state="OFF"
  
  #html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  #<link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  #h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  #border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  #.button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
  #<p>GPIO state: <strong>""" + gpio_state + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
  #<p><a href="/?led=off"><button class="button button2">OFF</button></a></p></body></html>"""
  #return html


import uselect
import time
import usocket

READ_ONLY = uselect.POLLIN
READ_WRITE = READ_ONLY | uselect.POLLOUT


websok = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
websok.bind(('192.168.0.20', 100))
websok.listen(5)
webpol = uselect.poll() # creates uselect.poll class under the name webpol
webpol.register(websok, READ_ONLY)

while True:

    print("waiting for the next event")
    events = webpol.ipoll(10000, 0)
    for event in events:  
      print(event)
      conn, addr = websok.accept()
      print('Got a connection from %s' % str(addr))
      request = conn.recv(1024)
      request = str(request)
      print('Content = %s' % request)
      time.sleep_us(5000)
      conn.close()