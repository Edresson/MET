import time

import socket
import os
import time
from threading import  Thread
import sys
import threading
def threaded(func):
    def wrapper(*_args, **kwargs):
        t = threading.Thread(target=func, args=_args)
        t.start()
        return
    return wrapper


class thread_motor(Thread):

    def run(self):

        inicio =  time.time()
        fim = 0
        while True:
            
            if fim - inicio > 3:
                #print(fim - inicio)
                
                inicio = time.time()
                #pong()
                
            fim = time.time()


            
log_file=open('MET_Logs.log', 'w')
try:
    arquivo = open("IP-Raspberry.txt","r")
    IP = arquivo.readline()
except:
    print("O Arquivo IP-Raspberry.txt está corrompido ou foi excluido, crie o arquivo e coloque o IP do Raspberry Pi",file=log_file)
    sys.exit()


        
IP = str(IP)

PORT = 12001
addr = (IP, PORT)
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect(addr)


#@threaded
def Subir_descer(vel,controle,deslocamento):
    print("calculando S_D")	
    freq  = vcalcular(vel)
    MSG = "SeD:"+str(vel)+':'+str(freq)+':'+str(controle)+':'+str(deslocamento)
    MSG =MSG.encode()

    ##print(MSG)
    tcp.send(MSG)
    print("mensagem enviada S_D")
    
#@threaded    
def Parar():
    
    MSG = b"STOP"    
    tcp.send(MSG)
    
#@threaded        
def subir():
    
    MSG = b"SUBIR"    
    tcp.send(MSG)
    
#@threaded
def baixar():
    
    MSG = b"BAIXAR"    
    tcp.send(MSG)


def vcalcular(valor) :
 """
 Função  vcalcular calcula a frequência necessária para o o deslocamento em min/mm (parametro da função)
 como não foi encontrado nenhum tendencia na curva de frequência do controle do motor foi
 criado varias pequenas retas. como criar estas retas para o meu motor de passo ??
 Para nossa maquina de teste usamos a velocidade de 8 mm/min até 175 mm/min
 como pode ser visto no comandos condicionais utilizados a baixo(if),
 traçamos pequenas retas entre dois pontos no primeira condição percebe-se  que o deslocamento está de
 8mm/min a 14 mm/min  e a variavel frequencia é a variavel utilizada para armazenar a equeção da reta que
 receberá o valor de mm/min que a maquina deve andar e calcula a frequencia necessaria para tal.
 após a thread responsavel por movimentar o motor será inicializada e o motor começará a andar na velocidade desejada.
 Para obter a equação da reta você deve chutar um frequencia você pode fazer issom usando  a função get_pontos(frequencia_chutada),
 essa função manterá a maquina ligada por 1 min, após a maquina parar você deve medir a distancia percorrida por ela usando um paquimetro
 ou outro equipamento com boa precisão após pegue o valor chutado e o resultado obtido pela sua medição em uma tabela, quando
 tiver calculado 2 pontos poderá fazer o calculo de sua primeira reta.
 """
 global frequencia
 valor = float(valor)
 velocidadei = valor;
 
 if (valor >= 8 and valor <= 14) :
   
    return   (4.166666666666667*valor  + 16.666666666666664)*0.96;
   
    
    
 if (valor > 14  and valor <= 16) :
    
    return   (12.5*valor  - 100)*0.96;
   
    
 if (valor > 16  and valor <= 21) :
    
    return   (5*valor  + 20)*0.96;
    
    
 if (valor > 21  and valor <= 26) :
    
    return   (5*valor  + 20)*0.96;
   
    
 if (valor > 26  and valor <= 33) :
   
    return   (7.142857142857143*valor  - 35.71428571428572)*0.96;
   
    
    
 if (valor > 33  and valor <= 45) :

    return   (4.166666666666667*valor  + 62.5)*0.96;
    



  
 elif(valor > 45 and valor <= 49 ) :
    return  (12.5*valor -312.5)*0.96;
    
    

    
  
 elif(valor > 49 and valor <= 58) :
    
    return   (5.555555555555555*valor  + 27.77777777777777)*0.96
    #print(frequencia)
    
  
 elif(valor > 58 and valor <=  67) :

    
    return   (5.555555555555555*valor + 27.77777777777777)*0.96;
    
    
  
 elif(valor > 67 and valor <= 73) :
    
    return  (8.333333333333334 *valor -158.33333333333337)*0.96;
    
    
  
 elif(valor > 73 and valor <= 83) :
    
    return   (5 *valor  + 85)*0.96
    
  
 elif(valor > 83 and valor <= 87) :
    return  (10*valor -330)*0.96;

    
    
  
 elif(valor > 87 and valor <= 97) :
    
    return  (6*valor+18)*0.96;

    
  
 elif(valor > 97 and valor <= 106) : 
    
    return   (5.555555555555555*valor +61.111111111111086)*0.96

    
    
  
 elif(valor > 106 and valor <= 113):
    return (7.142857142857143 *valor -107.14285714285722)*0.96
    
  
 elif(valor > 113 and valor <= 119):
    return (8.333333333333334*valor -241.66666666666674)*0.96

    
  
 elif(valor > 119 and valor <= 126):
    return   (7.142857142857143*valor- 100)*0.96;

    
  
 elif(valor > 126 and valor <= 133):
    return  (7.142857142857143*valor - 100)*0.96
    
  
 elif(valor > 133 and valor <=  141) :

    return  (4.545454545454546*valor + 245.45454545454538)*0.96

    
 elif(valor > 141 and valor <=  175) :
     return  (6.323529411764706* valor +8.382352941176464)*0.96

#@threaded
def calcular(valor):

    freq = vcalcular(valor)
    
    MSG = "Cal:"+str(valor)+':'+str(freq)
    MSG =MSG.encode()
    ##print(MSG)
    tcp.send(MSG)

    
#@threaded
def pong():
    MSG = "1"
    MSG =MSG.encode()
    tcp.send(MSG)
   
def ping():
    print(" ENVIANDO Ping")
    MSG = "ping"
    MSG =MSG.encode()
    tcp.send(MSG)
    try:
            data = tcp.recv(1024)
            print(" ping recebido")
            return [1,IP,PORT]                                    
    except:
        return [0,IP,PORT]

def start_thread():    
    
    thrMotor = thread_motor()
    thrMotor.start()
#@threaded
def freqparabotao():
    freqbt = vcalcular(70)

    MSG = "fb:"+str(freqbt)
    MSG =MSG.encode()
    ##print(MSG)
    tcp.send(MSG)


'''subir()
baixar()
Parar()
Subir_descer(100.1,1,120)
calcular(150)'''

