from machine import Pin
import network
import time
from time import sleep
from umqtt.robust import MQTTClient
import sys


WIFI_SSID     = 'raspi-webgui-04'
WIFI_PASSWORD = 'raspberrypi'

MQTT_IO_URL = '10.3.141.1'

mqtt_client_id = bytes('cliente_'+'12321', 'utf-8') # um ID de cliente aleatorio

# Caso o servidor MQTT exija usuario e senha
# MQTT_USERNAME   = 'usuario'
# MQTT_IO_KEY     = 'senha'



motor1      = Pin(5, Pin.OUT)
motor2      = Pin(4, Pin.OUT)


ini_tempo = 0


def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(WIFI_SSID,WIFI_PASSWORD)
    if not wifi.isconnected():
        print('Conectando...')
        timeout = 0
        while (not wifi.isconnected() and timeout < 10):
            print(10 - timeout)
            timeout = timeout + 1
            time.sleep(1) 
    if(wifi.isconnected()):
        print('Conectado')
    else:
        print('Nao conectado')
        sys.exit()


# Conecta ao roteador WiFi
connect_wifi()

# Caso o servidor MQTT nao exija usuario e senha
client = MQTTClient(client_id=mqtt_client_id, server=MQTT_IO_URL)

# Caso o servidor MQTT exija usuario e senha
# client = MQTTClient(client_id=mqtt_client_id, server=MQTT_IO_URL, user=MQTT_USERNAME, password=MQTT_IO_KEY,ssl=False)
try:
    client.connect()
except Exception as e:
    print('Nao foi possivel conectar ao servidor MQTT {}{}'.format(type(e).__name__, e))
    sys.exit()

def mapear(x, in_min, in_max,out_min, out_max):
    return (x - in_min) *(out_max - out_min) / (in_max - in_min) + out_min

def cb(topic, msg):
    print('Received Data:  Topic = {}, Msg = {}'.format(topic, msg))
    #recieved_data = int(str(msg,'utf-8'))
    #valor_mapeado = mapear(recieved_data,0,100,0,10)
    #if valor_mapeado == 0:
    #    led.value(0)
    #if valor_mapeado == 1:
    #    led.value(1)
    
    if topic == b'aviao/motor/1':
        if msg == b'ligar/desligar':
            print('Ligando desligando motor 1')
            motor1.value(not motor1.value())
    
    if topic == b'aviao/motor/2':
        if msg == b'ligar/desligar':
            print('Ligando desligando motor 2')
            motor2.value(not motor2.value())


# Funcao Callback
client.set_callback(cb)

# Inscricao nos topicos

client.subscribe(b'aviao/motor/1')
client.subscribe(b'aviao/motor/2')


while True:
    try:
        client.check_msg()
        
    except:
        client.disconnect()
        sys.exit()