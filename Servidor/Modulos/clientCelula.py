import time
from socket import *

IP = "192.168.1.100"

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
            return float(data)
                                                
    except:
        
        getvalue()

        
    

    
    
def calibrar():
    MSG = "ca"
    MSG =MSG.encode()
    
    clientSocket.sendto(MSG, addr)
    try:
            data, server = clientSocket.recvfrom(1024)
            return float(data)
                                                
    except:
        
        getvalue()

        

    


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
            #print ('%s' % (data))                                     
    except:
        tare()

        






