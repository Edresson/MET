# -*- coding: utf-8 -*-
from threading import  Thread
from PyQt4 import QtTest
from time import time
import time

from socket import *

import Motor

import celula

serverSocketMotor = socket(AF_INET, SOCK_DGRAM)
serverSocketMotor.bind(('', 12001))


serverSocketCelula = socket(AF_INET, SOCK_DGRAM)
serverSocketCelula.bind(('', 12002))



class thread_motor(Thread):

    def run(self):
        global freq_botao
        inicio= time.time()
        while True:
            fim = time.time()
            if fim - inicio > 6:
                Motor.Parar()
            	    
            message, address = serverSocketMotor.recvfrom(1024)	    
            message = str(message).replace("b'",'')
            message = message.replace("'",'')
            if message == "1":
                inicio = time.time()
                
                
            if message == "STOP":
                print('parar')
		serverSocketMotor.sendto(B'1', address) 
                Motor.Parar()
                
            elif message == "ping":
                print('p')
                serverSocketMotor.sendto(B'ping', address)
                
            elif message[0:2] =='fb':
                print('fb')
                string,freqfb = message.split(':')
                Motor.freq_botao = float(freqfb)
                
                
            elif message[0:3] =='SeD':
                print('SeD')
                serverSocketMotor.sendto(B'1', address)
                string,vel,freq,controle,deslocamento = message.split(':')
                Motor.Subir_descer(float(vel),float(freq),int(controle),float(deslocamento))
                
            elif message[0:3] =='Cal':
		print('cal')
                
                serverSocketMotor.sendto(B'1', address)
                cmd,valor,freq = message.split(':')
                Motor.calcular(float(valor),float(freq))
                
            elif message =="SUBIR":
                print('Subir')
                serverSocketMotor.sendto(B'1', address)
                Motor.subir()
            elif message =="BAIXAR":
                print('Baixar')
                ####print(message)
                serverSocketMotor.sendto(B'1', address)
                Motor.baixar()
        



class thread_celula(Thread):

    def run(self):

        while True:
            
            message, address = serverSocketCelula.recvfrom(1024)
            message = str(message).replace("b'",'')
            message = message.replace("'",'')
            
            if message == "gv":
                
                
            
                val = str(celula.getvalue())
                val =val.encode()
                serverSocketCelula.sendto(val, address)
                
            elif message == "ping":
                 serverSocketMotor.sendto(B'ping', address)
                 
            elif message =='ca':
                
                
                val = str(celula.calibrar())
                val =val.encode()
                serverSocketCelula.sendto(val, address)

                
            elif message[0:3] =='ini':
                
                serverSocketCelula.sendto(B'1', address)
                cmd,valor = message.split(':')
                celula.iniciarcel(float(valor))
                
            elif message =="tr":
                serverSocketCelula.sendto(B'1', address)
                celula.tare()
    
    



thrCelula=thread_celula()
thrCelula.start()

thrMotor = thread_motor()
thrMotor.start()

