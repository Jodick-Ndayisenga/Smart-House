try:
 import usocket as socket        #importing socket
except:
 import socket
import network #importing network
from machine import Pin
import esp                 #importing ESP
esp.osdebug(None)
import gc
from time import sleep
gc.collect()
ssid = 'qweueioqeioqwe'                  #Set access point name 
password = '12345678'      #Set your access point password

sensor = dht.DHT11(Pin(14))

ap = network.WLAN(network.AP_IF)
ap.active(True)            #activating
ap.config(essid=ssid, password=password)

while ap.active() == False:
  pass

print('Reseau Wifi active avec le nom: %s ' % ssid)
print('Parametres :')
print(ap.ifconfig())


led1 = Pin(15, Pin.OUT)
led2 = Pin(2, Pin.OUT)
led3 = Pin(4, Pin.OUT)
led4 = Pin(5, Pin.OUT)

bp1 = Pin(18, Pin.IN, Pin.PULL_UP)
bp2 = Pin(19, Pin.IN, Pin.PULL_UP)
bp3 = Pin(21, Pin.IN, Pin.PULL_UP)
bp4 = Pin(22, Pin.IN, Pin.PULL_UP)
ir = Pin(33, Pin.IN, Pin.PULL_UP)

gpio1_state = "OFF"
gpio2_state = "OFF"
gpio3_state = "OFF"
gpio4_state = "OFF"

Temperature = 0
Humidity = 0

def bp_read():
  try:
    if bp1.value() == 0:
        led1.value(not led1.value())
        print('BP1')
        while bp1.value() == 0:
            sleep(0.5)
      
    if bp2.value() == 0:
        led2.value(not led2.value())
        print('BP2')
        while bp2.value() == 0:
            sleep(0.5)
      
    if bp3.value() == 0:
        led3.value(not led3.value())
        print('BP3')
        while bp3.value() == 0:
            sleep(0.5)
      
    if bp4.value() == 0:
        led4.value(not led4.value())
        print('BP4')
        while bp4.value() == 0:
            sleep(0.5)
      
  except OSError as e:
    print('Failed to read sensor.')

def callback(data, addr, ctrl):
    if data > 0:  # NEC protocol sends repeat codes.
        print('Valeur {:02x}'.format(data))
        print(ir_key[data])
        if ir_key[data] == '1':
            led1.value(not led1.value())
            
        if ir_key[data] == '2':
            led2.value(not led2.value())
      
        if ir_key[data] == '3':
            led3.value(not led3.value())
      
        if ir_key[data] == '4':
            led4.value(not led4.value())

def web_page():
  dht_read()
  
  if led1.value() == 1:
    gpio1_state="ON"
  else:
    gpio1_state="OFF"
    
  if led2.value() == 1:
    gpio2_state="ON"
  else:
    gpio2_state="OFF"
    
  if led3.value() == 1:
    gpio3_state="ON"
  else:
    gpio3_state="OFF"
    
  if led4.value() == 1:
    gpio4_state="ON"
  else:
    gpio4_state="OFF"
  
#  html = """<html><head><title>ESP Web Server</title><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="icon" href="data:,"> <link rel="stylesheet" href="all.css"><style>  html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}  h1{color: #0F3376; padding: 2vh;}  p{font-size: 1.5rem;}  .button  {display: inline-block; background-color: #e7bd3b; border: none; border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}  .button2  {background-color: #4286f4;}</style></head><body> <h1>EEIA 2022</h1> <p><i class="fas fa-thermometer-half" style="color:#059e8a;"></i> <span class="dht-labels">Temperature</span> <span id="temperature">""" + Temperature + """</span><sup class="units">&deg;C</sup></p><p><i class="fas fa-tint" style="color:#00add6;"></i> <span class="dht-labels">Humidity</span><span id="humidity">""" + Humidity + """</span><sup class="units">&percnt;</sup></p><p><a href="/?led1=on"><button class="button">ON</button></a><a href="/?led1=off"><button class="button button2">OFF</button></a>Statut: <strong>""" + gpio1_state + """</strong></p></p><p><a href="/?led2=on"><button class="button">ON</button></a><a href="/?led2=off"><button class="button button2">OFF</button></a>Statut: <strong>""" + gpio2_state + """</strong></p></p><p><a href="/?led3=on"><button class="button">ON</button></a><a href="/?led3=off"><button class="button button2">OFF</button></a>Statut: <strong>""" + gpio3_state + """</strong></p></p><p><a href="/?led4=on"><button class="button">ON</button></a><a href="/?led4=off"><button class="button button2">OFF</button></a>Statut: <strong>""" + gpio4_state + """</strong></p></p>  </body></html>"""
  html = """
    <html>
    <head>
    <title>ESP Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <link rel="stylesheet" href="all.css">
    <style>
    html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}
    p{font-size: 1.5rem;}
    .button
    {
    display: inline-block;
    background-color: #e7bd3b;
    border: none;
    border-radius: 4px;
    color: white; padding: 16px 40px;
    text-decoration: none;
    font-size: 30px;
    margin: 2px;
    cursor: pointer;
    }
    .button2
    {
    background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>EEIA 2022</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="dht-labels">Temperature</span> 
    <span id="temperature">""" + str(Temperature) + """</span>
    <sup class="units">&deg;C</sup>
    </p>
    <p>
    <i class="fas fa-tint" style="color:#00add6;"></i> 
    <span class="dht-labels">Humidity</span>
    <span id="humidity">""" + str(Humidity) + """</span>
    <sup class="units">&percnt;</sup>
    </p>
    <p>
    <a href="/?led1=on"><button class="button">ON</button></a>
    <a href="/?led1=off"><button class="button button2">OFF</button></a>
    <strong>""" + gpio1_state + """</strong></p>
    </p>
    <p>
    <a href="/?led2=on"><button class="button">ON</button></a>
    <a href="/?led2=off"><button class="button button2">OFF</button></a>
    <strong>""" + gpio2_state + """</strong></p>
    </p>
    <p>
    <a href="/?led3=on"><button class="button">ON</button></a>
    <a href="/?led3=off"><button class="button button2">OFF</button></a>
    <strong>""" + gpio3_state + """</strong></p>
    </p>
    <p>
    <a href="/?led4=on"><button class="button">ON</button></a>
    <a href="/?led4=off"><button class="button button2">OFF</button></a>
    <strong>""" + gpio4_state + """</strong></p>
    </p>
    </body>
    </html>
    </script> """ 
#    <script>window.setInterval('refresh()', 30000); 
#    // Call a function every 10000 milliseconds 
#    // (OR 10 seconds).
#    // Refresh or reload page.
#    function refresh() {
#        window .location.reload();
#    }
#    </script> """  
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(10)
conn = ''
while True:
  #conn, addr = s.accept()
  try:
     if gc.mem_free() < 102000:
            gc.collect()
     conn, addr = s.accept()
     print('Got a connection from %s' % str(addr))
     request = conn.recv(1024)
     request = str(request)
     print('Content = %s' % request)
     led1_on = request.find("/?led1=on")
     print('Content = %s' % led1_on)
     led1_off = request.find('/?led1=off')
     led2_on = request.find('/?led2=on')
     led2_off = request.find('/?led2=off')
     led3_on = request.find('/?led3=on')
     led3_off = request.find('/?led3=off')
     led4_on = request.find('/?led4=on')
     led4_off = request.find('/?led4=off')
     
     if led1_on > 0:
       print('LED 2 ON')
       led1.value(1)
     if led1_off > 0:
       print('LED 1 OFF')
       led1.value(0)

     if led2_on > 0:
       print('LED 2 ON')
       led2.value(1)
       
     if led2_off > 0:
       print('LED OFF')
       led2.value(0)
       
     if led3_on > 0:
       print('LED 3 ON')
       led3.value(1)
     if led3_off > 0:
       print('LED 3 OFF')
       led3.value(0)
     if led4_on > 0:
       print('LED 4 ON')
       led4.value(1)
     if led4_off > 0:
       print('LED 4 OFF')
       led4.value(0)
       
     response = web_page()
     conn.send('HTTP/1.1 200 OK\n')
     conn.send('Content-Type: text/html\n')
     conn.send('Connection: close\n\n')
     conn.sendall(response)
     conn.close()
  except OSError as e:
     pass
     #conn.close()
     print('Connection closed')
  bp_read()

