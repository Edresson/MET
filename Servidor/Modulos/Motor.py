from threading import  Thread
import RPi.GPIO as GPIO
from PyQt4 import QtTest


from time import time

CP = 18 #CLOCK PULSE
CW = 19 #CLOCK WISE
EN = 26 #ENABLE
frequencia = 0
parou = 0
flag = 0


GPIO.setmode(GPIO.BCM)
GPIO.setup(CP, GPIO.OUT)
GPIO.setup(CW, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)
GPIO.setup(21, GPIO.IN)
GPIO.setup(20, GPIO.IN)

precionado = False
precionado2 = False
GPIO.setwarnings(False)

class thread2(Thread):
    def __init__(self,vel,deslocamento):
        self.vel = vel
        self.deslocamento = deslocamento
        Thread.__init__(self)

    def run(self):
        
        self.tempo = time()
        while( ((time() - self.tempo)/60)*float(self.vel) <= self.deslocamento ):
            pass


        Parar()
        


class thread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global frequencia
        ligar(frequencia);
    



class thread3(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global precionado2
        global precionado
        global parou
        while(True):
            
                

                
            #print(GPIO.input(EN))
            QtTest.QTest.qWait(300)
            
            if(GPIO.input(21) == False and precionado == False):
                precionado = True
                subir()
                #print("subir21")
                calcular(str(70))
            elif(GPIO.input(21) == True and precionado == True):
                precionado = False
                Parar()
                #print("parar")
            if(GPIO.input(20) == False and precionado2 == False):
                precionado2 = True
                #print("baixar20")
                baixar()
                calcular(str(70))
                
            elif(GPIO.input(20) == True and precionado2 == True):
                precionado2 = False
                Parar()
                #print("parar")
                
    
                


def subir():
    GPIO.output(EN, GPIO.HIGH)
    QtTest.QTest.qWait(100)
    
    GPIO.output(CW, GPIO.LOW)
    QtTest.QTest.qWait(100)
    
    GPIO.output(EN, GPIO.LOW)

                
def baixar():
    GPIO.output(EN, GPIO.HIGH)
    QtTest.QTest.qWait(100)
    
    GPIO.output(CW, GPIO.HIGH)
    QtTest.QTest.qWait(100)
    
    GPIO.output(EN, GPIO.LOW)

    
def ligar(tempo):
    #print("teste")
    a = time()
    GPIO.output(EN, GPIO.LOW)
    global parou
    global flag
    parou = 0
    
    pwm=GPIO.PWM(CP,float(tempo))
    pwm.start(80)

    
    while(parou == 0):
        pass
        
        
            
        #pwm.start(1)
    
        
       


        
        

        
    
def Parar():
    global parou
    parou = 1
    #print("parar")
    GPIO.output(EN, GPIO.HIGH)
    


def calcular(valor) :
 """
 Função calcular calcula a frequência necessária para o o deslocamento em min/mm (parametro da função)
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
 thr= thread()
 valor = float(valor)
 velocidadei = valor;
 
 if (valor >= 8 and valor <= 14) :
   
    frequencia =  (4.166666666666667*valor  + 16.666666666666664)*0.96;
   
    thr.start()
    
 if (valor > 14  and valor <= 16) :
    
    frequencia =  (12.5*valor  - 100)*0.96;
   
    thr.start()
 if (valor > 16  and valor <= 21) :
    
    frequencia =  (5*valor  + 20)*0.96;
    
    thr.start()
 if (valor > 21  and valor <= 26) :
    
    frequencia =  (5*valor  + 20)*0.96;
   
    thr.start()
 if (valor > 26  and valor <= 33) :
   
    frequencia =  (7.142857142857143*valor  - 35.71428571428572)*0.96;
   
    thr.start()
    
 if (valor > 33  and valor <= 45) :

    frequencia =  (4.166666666666667*valor  + 62.5)*0.96;
    thr.start()



  
 elif(valor > 45 and valor <= 49 ) :
    frequencia = (12.5*valor -312.5)*0.96;
    
    thr.start()

    
  
 elif(valor > 49 and valor <= 58) :
    
    frequencia =  (5.555555555555555*valor  + 27.77777777777777)*0.96
    #print(frequencia)
    thr.start()
  
 elif(valor > 58 and valor <=  67) :

    
    frequencia =  (5.555555555555555*valor + 27.77777777777777)*0.96;
    
    thr.start()
  
 elif(valor > 67 and valor <= 73) :
    
    frequencia = (8.333333333333334 *valor -158.33333333333337)*0.96;
    
    thr.start()
  
 elif(valor > 73 and valor <= 83) :
    
    frequencia =  (5 *valor  + 85)*0.96
    thr.start()
  
 elif(valor > 83 and valor <= 87) :
    frequencia = (10*valor -330)*0.96;

    
    thr.start()
  
 elif(valor > 87 and valor <= 97) :
    
    frequencia = (6*valor+18)*0.96;

    thr.start()
  
 elif(valor > 97 and valor <= 106) : 
    
    frequencia =  (5.555555555555555*valor +61.111111111111086)*0.96

    
    thr.start()
  
 elif(valor > 106 and valor <= 113):
    frequencia =(7.142857142857143 *valor -107.14285714285722)*0.96
    thr.start()
  
 elif(valor > 113 and valor <= 119):
    frequencia =(8.333333333333334*valor -241.66666666666674)*0.96

    thr.start()
  
 elif(valor > 119 and valor <= 126):
    frequencia =  (7.142857142857143*valor- 100)*0.96;

    thr.start()
  
 elif(valor > 126 and valor <= 133):
    frequencia = (7.142857142857143*valor - 100)*0.96
    thr.start()
  
 elif(valor > 133 and valor <=  141) :

    frequencia = (4.545454545454546*valor + 245.45454545454538)*0.96

    thr.start()
 elif(valor > 141 and valor <=  175) :
     frequencia = (6.323529411764706* valor +8.382352941176464)*0.96
     thr.start()
     
def get_pontos(frequencia_teste):
    inicio = time.time()
    ligar(frequencia_teste)
    
    while (time.time() - inicio < 1000):#manter a maquina 1 minuto ligada
        pass
    Parar()#desligar a maquina
    
    
    
def Subir_descer(vel,controle,deslocamento):
    thr2= thread2(vel,deslocamento)
    
    if(int(controle) == 1):
        subir()
    else:
        baixar()
   
    
    calcular(str(vel))
    thr2.start()
   
###Botoes
#thr3 = thread3()
#thr3.start()

Parar()       
#baixar()
#calcular(120)

        



    
    




  

  




    

        
    
    
    
