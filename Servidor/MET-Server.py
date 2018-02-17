# -*- coding: utf-8 -*-
from threading import  Thread
from PyQt4 import QtTest
from time import time
import time

from socket import *

import Motor
import os
import celula

tcp = socket(AF_INET, SOCK_STREAM)
tcp.bind(('', 12001))
tcp.listen(7)

serverSocketCelula = socket(AF_INET, SOCK_DGRAM)
serverSocketCelula.bind(('', 12002))



class thread_motor(Thread):

    def run(self):
        global freq_botao
        inicio= time.time()
        while True:
            '''fim = time.time()
            if fim - inicio > 6:
                Motor.Parar()'''
            con, cliente = tcp.accept()
            pid = os.fork()
            if pid == 0:
                tcp.close()
                ##print 'Conectado por', cliente
                while True:
                    message = con.recv(1024)
                    if not message: continue
                    ##print cliente, msg
                    if message == "1":
                        inicio = time.time()
                
                
                    elif message == "STOP":
                        #print('parar')
                        Motor.Parar()
                        
                    elif message[0:9] == "getpontos":
                        try:
                            string,freqfb = message.split(':')
                            Motor.get_pontos(float(freqfb))
                        except:
                            pass




                    elif message == "ping":
                        #print('p')
                        con.send(B'ping')
                
                    elif message[0:2] =='fb':
                        try:
                            #print('fb')
                            string,freqfb = message.split(':')
                            Motor.freq_botao = float(freqfb)
                        except:
                            pass
                
                
                    elif message[0:3] =='SeD':
                        #print('SeD')
                        try:
                            Motor.Parar()
                            string,vel,freq,controle,deslocamento = message.split(':')
                            Motor.Subir_descer(float(vel),float(freq),int(controle),float(deslocamento))
                        except:
                            pass
                        
                    elif message[0:3] =='Cal':
                        #print('cal')
                        try:
                            cmd,valor,freq = message.split(':')
                            Motor.calcular(float(valor),float(freq))
                        except:
                            pass
                
                    elif message =="SUBIR":
                        
                        #print('Subir')
                        Motor.subir()
                    elif message =="BAIXAR":
                        #print('Baixar')
                        #####print(message)
                
                        Motor.baixar()
        

                #print('Motor parou, caiu a conexao')                   
                Motor.Parar()
                con.close()
                #sys.exit(0)
            else:
                con.close()


class thread_celula(Thread):

    def run(self):

        while True:
            try: 
                message, address = serverSocketCelula.recvfrom(1024)
                message = str(message).replace("b'",'')
                message = message.replace("'",'')
            except:
                message =""
                pass
            
            if message == "gv":
                try:
                    val = str(celula.getvalue())
                    val =val.encode()
                    serverSocketCelula.sendto(val, address)
                except:
                    pass
                
            elif message == "ping":
                 serverSocketCelula.sendto(B'ping', address)
                 
            elif message =='ca':
                try:
                    val = str(celula.calibrar())
                    val =val.encode()
                    serverSocketCelula.sendto(val, address)
                except:
                    pass
                

                
            elif message[0:3] =='ini':
                try:
                
                    serverSocketCelula.sendto(B'1', address)
                    cmd,valor = message.split(':')
                    celula.iniciarcel(float(valor))
                except:
                    pass
                
            elif message =="tr":
                serverSocketCelula.sendto(B'1', address)
                celula.tare()
    
    



thrCelula=thread_celula()
thrCelula.start()

thrMotor = thread_motor()
thrMotor.start()

