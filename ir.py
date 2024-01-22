from machine import Pin
import esp                 #importing ESP
esp.osdebug(None)
import gc
from ir_rx import NEC_16
from time import sleep
gc.collect()
ir_key = {
    0x45: '1',
    0x46: '2',
    0x47: '3',
    0x44: '4',
    0x40: '5',
    0x43: '6',
    0x07: '7',
    0x15: '8',
    0x09: '9',
    0x16: '*',
    0x19: '0',
    0x0D: '#',
    0x08: 'ARR',
    0x1C: 'OK',
    0x5A: 'SUIV',
    0x52: 'BAS',
    0x4A: 'HAUT'
    }
def telecommande(data, addr, ctrl):
    if data > 0:  # NEC protocol sends repeat codes.
        print('Valeur {:02x}'.format(data))
        print(ir_key[data])

while True:
  NEC_16(Pin(23, Pin.IN), telecommande)


