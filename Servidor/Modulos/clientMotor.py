import time
from socket import *

IP = "192.168.1.100"

PORT = 12001
addr = (IP, PORT)
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

def Subir_descer(vel,controle,deslocamento):
    MSG = "SeD:"+str(vel)+':'+str(controle)+':'+str(deslocamento)
    MSG =MSG.encode()
    ##print(MSG)
    clientSocket.sendto(MSG, addr)
    try:
            data, server = clientSocket.recvfrom(1024)
            #print ('%s' % (data))                                     
    except:
        Subir_descer(vel,controle,deslocamento)
    
def Parar():
    
    MSG = b"STOP"    
    clientSocket.sendto(MSG, addr)
    try:
            data, server = clientSocket.recvfrom(1024)
            #print ('%s' % (data))                                     
    except:
        Parar()
        
def subir():
    
    MSG = b"SUBIR"    
    clientSocket.sendto(MSG, addr)
    try:
            data, server = clientSocket.recvfrom(1024)
            #print ('%s' % (data))                                     
    except:
        subir()        

def baixar():
    
    MSG = b"BAIXAR"    
    clientSocket.sendto(MSG, addr)
    try:
            data, server = clientSocket.recvfrom(1024)
            
            #print ('%s' % (data))                                     
    except:
        baixar()


def calcular(valor):
    MSG = "Cal:"+str(valor)
    MSG =MSG.encode()
    ##print(MSG)
    clientSocket.sendto(MSG, addr)
    try:
            data, server = clientSocket.recvfrom(1024)
            #print ('%s' % (data))                                     
    except:
        calcular(valor)
    

    

'''subir()
baixar()
Parar()
Subir_descer(100.1,1,120)
calcular(150)'''

