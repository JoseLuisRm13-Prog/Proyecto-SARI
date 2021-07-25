#Importamos librerias necesarias
import network, time, urequests
from machine import Pin, ADC, I2C, PWM
from Funciones_modulo.Funciones import conectaWifi, uso_apis, map
from ssd1306 import SSD1306_I2C

#Configuracion Pantalla oled
ancho = 128
alto = 64
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(ancho, alto, i2c)

#Conectamos los sensores
sensor = ADC(Pin(39))
sensor.width(ADC.WIDTH_10BIT)
sensor.atten(ADC.ATTN_11DB)

#Conectamos el servo como simulacion de riego automatico
servo = PWM(Pin(27), freq = 50)

#Llamamos las funciones para conectar con el Api-rest (IFTTT)
url =  uso_apis('Enviar_correo')
url_2 = uso_apis('humedad')

if conectaWifi("Familia Rubiano Villarraga", "50A5DC61600B"):
    #Inicializamos la ejecucion del programa
    while True:
        #Realizamos la lectura del sensor
        lectura = float(sensor.read())
        #Transmitimos los datos a nuestra hoja de excel en el drive con (IFTTT)
        respuesta_2 = urequests.get(url_2+"&value1="+str(lectura))
        respuesta_2.close()
        #Convertimos los datos a enviar a la pantalla oled
        lectura_oled = ('HM Cultivo: '+ str(lectura))
        oled.text(lectura_oled,0,20)
        oled.show()
        oled.fill(0)
        time.sleep(0.03)
        
        #Validamos las lecturas, buscando la humedad deseada
        if lectura < 700:
            print('Demasiada humedad en el terreno, no regar y esperar nuevos datos del sensor')
            print('Humedad Actual: \n', lectura)
            #Lectura de cero/ cero grados
        elif lectura >= 700 and lectura < 760:
            print('La humedad es perfecta para el cultivo')
            print('Humedad Actual: \n', lectura)
            #Lectura de cero/ cero grados
        elif lectura >= 760:
            print('Se debe realizar un riego sobre el cultivo')
            print('Humedad Actual: \n', lectura)
            #Notificamos al granjero que debe realizar el riego
            respuesta = urequests.get(url+"&value1="+str(lectura))
            respuesta.close()
            #Realizamos el giro de 90 grados al servo, simulando la activacion del riego
            angulo = 180
            m = map(angulo)
            servo.duty(m)
            break
        time.sleep (5)
        
    print("El sistema SARI se ejecutara nuevamente en unos minutos")

else:
       print ("Imposible conectar")
       miRed.active (False)