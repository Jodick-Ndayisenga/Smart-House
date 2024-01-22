import gc
gc.collect()

from ir_rx import NEC_16
import dht
from time import sleep

#version définitive
import network
import socket
import time
#parametre du serveur
import parametres  
repertoire = parametres.repertoire
index_page = parametres.index_page
ssid = parametres.ssid
password = parametres.password
ir_key = parametres.ir_key

#module de changements dynamiques des variables 
import mdvd 
#module  traitement de commandes dynamiques   
import mtcd

#led allumée durant les échanges client-serveur
from machine import Pin
Led_builtin = Pin(2, Pin.OUT)
Led_builtin.off()
sensor = dht.DHT11(Pin(14))
led1 = Pin(15, Pin.OUT)
led2 = Pin(25, Pin.OUT)
led3 = Pin(4, Pin.OUT)
led4 = Pin(5, Pin.OUT)

bp1 = Pin(18, Pin.IN, Pin.PULL_UP)
bp2 = Pin(19, Pin.IN, Pin.PULL_UP)
bp3 = Pin(21, Pin.IN, Pin.PULL_UP)
bp4 = Pin(22, Pin.IN, Pin.PULL_UP)
ir = Pin(33, Pin.IN, Pin.PULL_UP)

humidity = 0
temperature = 0

def dht_read():
  try:
    print('Lecture Capteur')
    global humidity
    global temperature
    sensor.measure()
    temperature = sensor.temperature()
    humidity = sensor.humidity()
    print('Temperature: %3.1f C' %temperature)
    print('Humidity: %3.1f %%' %humidity)
    sleep(2)
  except OSError as e:
    print('Failed to read sensor.')

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

def telecommande(data, addr, ctrl):
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


'''
def connexion_wifi_STA(pssid,ppassword) : # Connexion wifi mode STATION

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(pssid, ppassword)

    print("Borne wifi : ", pssid)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(pssid, ppassword) 
        while not wlan.isconnected(): 
            pass
    if wlan.isconnected():
        print('network config:', wlan.ifconfig()) # interface's IP/netmask/gw/DNS addresses
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )
        Led_builtin.on()
        time.sleep(3)
        Led_builtin.off()
   
'''
def connexion_wifi_AP(pssid,ppassword): #Connexion wifi mode ACCESS POINT
    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid= pssid , password = ppassword)
    wlan.active(True)
    while wlan.active == False :
        pass
    print("Access point actif")
    print(wlan.ifconfig())
    print('Réseau wifi : ',pssid, 'et mot de passe :',ppassword)
    Led_builtin.on()
    time.sleep(3)
    Led_builtin.off()   
    

def construction_dico_dynamiques(dico): #construction du dico_valeurs_dynamiques à partir de dico.txt
    with open(repertoire + '/dico.txt', 'r') as file:   
        ligne = file.readline()
        while ligne != "":
            ligne_split = ligne.split(':')
            dico[ligne_split[0]] = ligne_split[1][:-2]
            ligne = file.readline()
    return(dico)

def insertion_valeurs_dynamiques (fichier_lu) :
    debut_recherche = 0
    while True :
        # recherche du premier {{
        start = fichier_lu.find(b"{{", debut_recherche)
        if start ==-1 :
            break
        end = fichier_lu.find(b"}}", start)
        nom_variable = fichier_lu[start + 2:end].strip()
        nom_variable_str = nom_variable.decode()
        valeur_nom_variable = dico_valeurs_dynamiques.get(nom_variable_str)
        if valeur_nom_variable != None :
            fichier_lu = fichier_lu[0:start]+ valeur_nom_variable + fichier_lu[end+2::]   
        #recherche de la prochaine insertion capteur 
        debut_recherche = end + 2
    return fichier_lu

def exec_commande(action) :
    #global led1_off
    print (action)
    led1_off = action.find('1=off')
    led1_on = action.find('1=on')
    led2_on = action.find('2=on')
    led2_off = action.find('2=off')
    led3_on = action.find('3=on')
    led3_off = action.find('3=off')
    led4_on = action.find('4=on')
    led4_off = action.find('4=off')
    print (led1_off)
    if led1_on > 0:
       print('LED 1 ON')
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

def acquisition_commande(request_file_name) :
    #analyse de la requête, recherche de la commande        
    commande = ''
    if "/?" in request_file_name:
        indice_debut = request_file_name.find("?")+1
        commande = request_file_name[indice_debut:]
    return commande
 
def get_request_file(request_file_name):
    #page index par défaut
    if request_file_name == '/' :  
        request_file_name = '/'+index_page
    with open(repertoire + request_file_name, 'rb') as file:   #byte
        file_requested= file.read()
        print(repertoire + request_file_name)
    file_requested = insertion_valeurs_dynamiques(file_requested)  # commentaire alors tailles des imahges plus grandes mais pas d'insertion dynamique de données
    return file_requested   
#debut programme principal
#connexion wifi
if parametres.mode_wifi== 'AP' : 
    connexion_wifi_AP(ssid,password)
elif parametres.mode_wifi== 'STA' :
    connexion_wifi_STA(ssid,password)

#Construction dico_valeurs_dynamiques à partir du fichier dico.txt
dico_valeurs_dynamiques = {} 
dico_valeurs_dynamiques = construction_dico_dynamiques(dico_valeurs_dynamiques)

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(5)
s.settimeout(0.01) #evite de rester bloquer à attendre une connexion dans la boucle principale 
print('listening on', addr) # Listen for connections

while True:
    if gc.mem_free() < 102000:
        gc.collect()
    commande = ''
    #Mise à jour donnéees dynamiques : Capteurs....
    dico_valeurs_dynamiques= mdvd.modifications_dico_valeurs_dynamiques(dico_valeurs_dynamiques)
    try:
        cl, addr = s.accept()
        #Allume LED pour indiquer un client connecté 
        Led_builtin.on()
        #reception de la demande
        request = cl.recv(1024)
        #turns the request into a string
        request = str(request)        
        #recherche des données demandées
        request = request.split()[1]
        if '.html' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'
        elif '.css' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: text/css\r\n\r\n'
        elif '.js' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: text/javascript\r\n\r\n'
        elif '.svg' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: image/svg+xml\r\n\r\n'
        elif '.json' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: application/json\r\n\r\n'  #json
        elif '.svgz' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: image/svg+xml\r\n\r\n'
        elif '.png' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: image/png\r\n\r\n'
        elif '.ico' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: image/x-icon\r\n\r\n'
        elif '.jpg' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: image/jpg\r\n\r\n'
        elif '.webp' in request:
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: image/webp\r\n\r\n'   #webp
        # serve index if you don't know
        else:
            file_header = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n'
        #lecture du ficher demandé + recherche commande  
        #recherche d'une commande
        commande = acquisition_commande(request)
        #traitement commandes dynamiques
        print('la commande est :',commande)
        #mtcd.traitement_commandes_dynamiques(commande)
        #pas de commande mais simple appel de page
        if commande=='' :
            #lecture du ficher demandé + insertion data 
            response = get_request_file(request)
            #envoie file header
            cl.send(file_header)
            #envoie réponse
            cl.sendall(response)
            cl.close()
            #eteindre la led  : fin de la communication
            Led_builtin.off()
        else:
            exec_commande(commande)
    except :
        #cl.close()
        Led_builtin.off()
        #print('pas de connexion')
    time.sleep(0.1)    
    sleep(0.5)
    NEC_16(Pin(23, Pin.IN), telecommande)
    dht_read()
    bp_read()   
