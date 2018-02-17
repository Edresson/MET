import time
from socket import *
import sys
import threading


def threaded(func):
    def wrapper(*_args, **kwargs):
        t = threading.Thread(target=func, args=_args)
        t.start()
        return
    return wrapper


log_file=open('MET_Logs.log', 'w')
try:
    arquivo = open("IP-Raspberry.txt","r")
    IP = arquivo.readline()
except:
    print("O Arquivo IP-Raspberry.txt está corrompido ou foi excluido, crie o arquivo e coloque o IP do Raspberry Pi",file=log_file)
    sys.exit()

        
IP = str(IP)


PORT = 12002
addr = (IP, PORT)
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

def getvalue():
    
    MSG = "gv"
    MSG =MSG.encode()
    #print(MSG)
    clientSocket.sendto(MSG, addr)
    try:
            data, server = clientSocket.recvfrom(1024)
            #print(float(data))
            return float(data)
                                                
    except:
        
        getvalue()

        
    

    
 
def calibrar():
    MSG = "ca"
    MSG =MSG.encode()
    
    clientSocket.sendto(MSG, addr)
    try:
            data, server = clientSocket.recvfrom(1024)
            #print(float(data))
            return float(data)
                                                
    except:
        #print('falhou')
        calibrar()

        

    

def iniciarcel(calib):
    MSG = "ini:"+str(calib)
    MSG =MSG.encode()
    
    clientSocket.sendto(MSG, addr)
    try:
            data, server = clientSocket.recvfrom(1024)
            #print ('%s' % (data))                                     
    except:
        iniciarcel(calib)
    
  

def tare():
    MSG = "tr"
    MSG =MSG.encode()
    
    clientSocket.sendto(MSG, addr)
    try:
            data, server = clientSocket.recvfrom(1024)
            
            print ('tare','%s' % (data))                                     
    except:
        tare()

    
def ping():
    MSG = "ping"
    MSG =MSG.encode()
    clientSocket.sendto(MSG, addr)
    try:
            data, server = clientSocket.recvfrom(1024)
            return [1,IP,PORT]                                    
    except:
        return [0,IP,PORT]

    




