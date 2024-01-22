try:
  import usocket as socket
except:
  import socket
import network
import esp
esp.osdebug(None)
import gc
gc.collect()
ssid = 'Mon_Point_d_Acces'
password = '123456789'
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)
while ap.active() == False:
  pass
print(ap.ifconfig())
def web_page():
  html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head><body><h2>Bonjour, BENIN!</h2><h1>EEIA 2023</h1></body></html>"""
  return html
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 80))
s.listen(5)
while True:
  conn, addr = s.accept()
  print('cinnection de %s' % str(addr))
  request = conn.recv(1024)
  print('Contenu = %s' % str(request))
  response = web_page()
  conn.send(response)
  #conn.close()