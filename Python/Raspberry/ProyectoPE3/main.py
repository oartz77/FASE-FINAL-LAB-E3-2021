
import sys
from time import sleep
import RPi.GPIO as gpio
import signal
from gpiozero import LED 
from threading import Thread
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from twython import Twython
from auth import  (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )

twitter = Twython (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )


gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(11, gpio.OUT)
gpio.setup(12, gpio.OUT)
LED4 =gpio.PWM(11, 50)
LED7 =gpio.PWM(12, 50)
LED4.start(2.5) #Porton
LED7.start(2.5) #Puerta

LED1 = LED(26) #Parqueo
LED2 = LED(20) #Interior
LED3 = LED(21) #exterior

LED5 = LED(6) #AC

LED6 = LED(16) #Fuente
LED8 = LED(24)#PIR

LED9 = LED(19) #Ventilador



PAHT_CRED = '/home/pi/Desktop/ProyectoPE3/proyecto-practicas-e3-firebase-adminsdk-jj1tc-6e66acd5ce.json'
URL_DB = 'https://proyecto-practicas-e3-default-rtdb.firebaseio.com/'
REF_HOME = 'home'
REF_LUCES = 'luces'
REF_LUZ_PARQUEO = 'luz_parqueo'
REF_LUZ_INTERIOR = 'luz_interior'
REF_LUZ_EXTERIOR = 'luz_exterior'
REF_LUZ_AC= 'luz_AC'
REF_PORTON ='porton'
REF_GARAJE ='garaje'
REF_FUENTES ='fuentes'
REF_FUENTE ='fuente'
REF_SEGURIDAD ='seguridad'
REF_ALARMA='alarma'
REF_ENTRADA= 'Entrada'
REF_PUERTA='Puerta'
REF_VENTILACION= 'ventilacion'
REF_VENTILADOR= 'ventilador'


class IOT():

    def __init__(self):
        cred = credentials.Certificate(PAHT_CRED)
        firebase_admin.initialize_app(cred, {
            'databaseURL': URL_DB
        })

        self.refHome = db.reference(REF_HOME)
        
        self.estructuraInicialDB() # solo ejecutar la primera vez

        self.refLuces = self.refHome.child(REF_LUCES)
        self.refLuzParqueo = self.refLuces.child(REF_LUZ_PARQUEO)        
        self.refLuzInterior = self.refLuces.child(REF_LUZ_INTERIOR)
        self.refLuzExterior = self.refLuces.child(REF_LUZ_EXTERIOR)
        self.refLuzAC = self.refLuces.child(REF_LUZ_AC)
        
        self.refPorton = self.refHome.child(REF_PORTON)
        self.refGaraje = self.refPorton.child(REF_GARAJE)
        
        self.refFuentes = self.refHome.child(REF_FUENTES)
        self.refFuente = self.refFuentes.child(REF_FUENTE)
        
        self.refSeguridad= self.refHome.child(REF_SEGURIDAD)
        self.refAlarma = self.refSeguridad.child(REF_ALARMA)
        
        self.refEntrada = self.refHome.child(REF_ENTRADA)
        self.refPuerta = self.refEntrada.child(REF_PUERTA)
        
        self.refVentilacion = self.refHome.child(REF_VENTILACION)
        self.refVentilador = self.refVentilacion.child(REF_VENTILADOR)



    def estructuraInicialDB(self):
        self.refHome.set({
            'luces': {
                'luz_parqueo':True,
                'luz_interior':True,
                'luz_exterior' :True,
                'luz_AC':True
            },
            'porton': {
                'garaje' :True
            },
            'fuentes': {
                'fuente' :True
            },
            'seguridad':{
                'alarma':True
            },
            'Entrada':{
                'Puerta':True
            },
            'ventilacion':{
                'ventilador':True
            }
                         
        })
   
   
   #leds
    def ledControlGPIO(self, estado):
        if estado:
            LED1.on()
            print('LED1 ON')
        else:
            LED1.off()
            print('LED1 OFF')
               

    def lucesStart(self):

        E, i = [], 0

        estado_anterior = self.refLuzParqueo.get()
        self.ledControlGPIO(estado_anterior)

        E.append(estado_anterior)

        while True:
          estado_actual = self.refLuzParqueo.get()
          E.append(estado_actual)

          if E[i] != E[-1]:
              self.ledControlGPIO(estado_actual)

          del E[0]
          i = i + i
          sleep(0.4)
          
          

    def led1ControlGPIO(self, estado):
        if estado:
            LED2.on()
            print('LED2 ON')
        else:
            LED2.off()
            print('LED2 OFF')
          
          
          
    
    def lucesStart1(self):

        E, i = [], 0

        estado_anterior = self.refLuzInterior.get()
        self.led1ControlGPIO(estado_anterior)

        E.append(estado_anterior)

        while True:
          estado_actual = self.refLuzInterior.get()
          E.append(estado_actual)

          if E[i] != E[-1]:
              self.led1ControlGPIO(estado_actual)

          del E[0]
          i = i + i
          sleep(0.4)
          
          
    
    def led2ControlGPIO(self, estado):
        if estado:
            LED3.on()
            print('LED3 ON')
        else:
            LED3.off()
            print('LED3 OFF')
          
          
          
    
    def lucesStart2(self):

        E, i = [], 0

        estado_anterior = self.refLuzExterior.get()
        self.led2ControlGPIO(estado_anterior)

        E.append(estado_anterior)

        while True:
          estado_actual = self.refLuzExterior.get()
          E.append(estado_actual)

          if E[i] != E[-1]:
              self.led2ControlGPIO(estado_actual)

          del E[0]
          i = i + i
          sleep(0.4)
          

#AC
    def led4ControlGPIO(self, estado):
        if estado:
            LED5.on()
            print('AC ON')
        else:
            LED5.off()
            print('AC OFF')
          
          
          
    
    def lucesStart4(self):

        E, i = [], 0

        estado_anterior = self.refLuzAC.get()
        self.led4ControlGPIO(estado_anterior)

        E.append(estado_anterior)

        while True:
          estado_actual = self.refLuzAC.get()
          E.append(estado_actual)

          if E[i] != E[-1]:
              self.led4ControlGPIO(estado_actual)

          del E[0]
          i = i + i
          sleep(0.4)
    
  
#Fuente
    def led5ControlGPIO(self, estado):
        if estado:
            LED6.on()
            print('Fuente ON')
        else:
            LED6.off()
            print('Fuente OFF')
          
          
          
    
    def lucesStart5(self):

        E, i = [], 0

        estado_anterior = self.refFuente.get()
        self.led5ControlGPIO(estado_anterior)

        E.append(estado_anterior)

        while True:
          estado_actual = self.refFuente.get()
          E.append(estado_actual)

          if E[i] != E[-1]:
              self.led5ControlGPIO(estado_actual)

          del E[0]
          i = i + i
          sleep(0.4)
  
  
    
    
  #porton  
    def led3ControlGPIO(self, estado):
        if estado:
            
            LED4.ChangeDutyCycle(8)
            sleep(1)
            LED4.ChangeDutyCycle(0)
           
            print('Porton Abierto')
            
        else:
            LED4.ChangeDutyCycle(2.5)
            sleep(1)
            LED4.ChangeDutyCycle(0)
            
            print('Porton Cerrado')
               

    def lucesStart3(self):

        E, i = [], 0

        estado_anterior = self.refGaraje.get()
        self.led3ControlGPIO(estado_anterior)

        E.append(estado_anterior)

        while True:
          estado_actual = self.refGaraje.get()
          E.append(estado_actual)

          if E[i] != E[-1]:
              self.led3ControlGPIO(estado_actual)

          del E[0]
          i = i + i
          sleep(0.4)
    
    

 #Puerta  
    def led6ControlGPIO(self, estado):
        if estado:
            
            LED7.ChangeDutyCycle(8)
            sleep(1)
            LED7.ChangeDutyCycle(0)
           
            print('Puerta Abierto')
            
        else:
            LED7.ChangeDutyCycle(2.5)
            sleep(1)
            LED7.ChangeDutyCycle(0)
            
            print('Puerta Cerrado')
               

    def lucesStart6(self):

        E, i = [], 0

        estado_anterior = self.refPuerta.get()
        self.led6ControlGPIO(estado_anterior)

        E.append(estado_anterior)

        while True:
          estado_actual = self.refPuerta.get()
          E.append(estado_actual)

          if E[i] != E[-1]:
              self.led6ControlGPIO(estado_actual)

          del E[0]
          i = i + i
          sleep(0.4)
          
          

#PIR  
    def led7ControlGPIO(self, estado):
        if estado:
            
            LED8.on()
            print('Seguridad ON')
            message = "Sistema de seguridad activado"
            image = open ("seguridad_activado.jpg" , "rb" )
            response = twitter.upload_media(media=image)              
            media_id = [response["media_id"]]              
            twitter.update_status(status=message, media_ids=media_id)
            print("Tweeted: " + message)
            
            
        else:
            LED8.off()
            print('Seguridad Off')
            message = "Sistema de seguridad desactivado"
            image = open ("seguridad_desactivada.jpg" , "rb" )
            response = twitter.upload_media(media=image)              
            media_id = [response["media_id"]]              
            twitter.update_status(status=message, media_ids=media_id)
            print("Tweeted: " + message) 
               
    
    def lucesStart7(self):

        E, i = [], 0

        estado_anterior = self.refAlarma.get()
        self.led7ControlGPIO(estado_anterior)

        E.append(estado_anterior)

        while True:
          estado_actual = self.refAlarma.get()
          E.append(estado_actual)

          if E[i] != E[-1]:
              self.led7ControlGPIO(estado_actual)

          del E[0]
          i = i + i
          sleep(0.4)
          
#Ventilación
    def led8ControlGPIO(self, estado):
        if estado:
            LED9.on()
            print('Ventilacion ON')
        else:
            LED9.off()
            print('ventilacion OFF')
               

    def lucesStart8(self):

        E, i = [], 0

        estado_anterior = self.refVentilador.get()
        self.led8ControlGPIO(estado_anterior)

        E.append(estado_anterior)

        while True:
          estado_actual = self.refVentilador.get()
          E.append(estado_actual)

          if E[i] != E[-1]:
              self.led8ControlGPIO(estado_actual)

          del E[0]
          i = i + i
          sleep(0.4)



print ('START !')
iot = IOT()

subproceso_led = Thread(target=iot.lucesStart)
subproceso_led.daemon = True
subproceso_led.start()


subproceso_led = Thread(target=iot.lucesStart1)
subproceso_led.daemon = True
subproceso_led.start()


subproceso_led = Thread(target=iot.lucesStart2)
subproceso_led.daemon = True
subproceso_led.start()


subproceso_led = Thread(target=iot.lucesStart3)
subproceso_led.daemon = True
subproceso_led.start()

subproceso_led = Thread(target=iot.lucesStart4)
subproceso_led.daemon = True
subproceso_led.start()

subproceso_led = Thread(target=iot.lucesStart5)
subproceso_led.daemon = True
subproceso_led.start()

subproceso_led = Thread(target=iot.lucesStart6)
subproceso_led.daemon = True
subproceso_led.start()

subproceso_led = Thread(target=iot.lucesStart7)
subproceso_led.daemon = True
subproceso_led.start()

subproceso_led = Thread(target=iot.lucesStart8)
subproceso_led.daemon = True
subproceso_led.start()
