from threading import  Thread
import RPi.GPIO as GPIO
from PyQt4 import QtTest

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)
GPIO.setup(20, GPIO.IN)
precionado = False
precionado2 = False
class thread3(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global precionado2
        global precionado
        while(True):
            QtTest.QTest.qWait(300)
            
            if(GPIO.input(21) == False and precionado == False):
                precionado = True
                print("Subir21")
            elif(GPIO.input(21) == True and precionado == True):
                precionado = False
                print("Parar21")
                
            if(GPIO.input(20) == False and precionado2 == False):
                precionado2 = True
                print("Descer20")
            elif(GPIO.input(20) == True and precionado2 == True):
                precionado2 = False
                print("Parar20")


thr3 = thread3()
thr3.start()
            
        
