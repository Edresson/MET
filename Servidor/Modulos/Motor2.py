from threading import  Thread
import RPi.GPIO as GPIO
from PyQt4 import QtTest

#from time import sleep
from time import time

CP = 18 #CLOCK PULSE
CW = 27 #CLOCK WISE
EN = 22 #ENABLE
delayligado = 0
parou = 0
flag = 0
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(CP, GPIO.OUT)
GPIO.setup(CW, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)
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
        

#duas funçoes substitutas do sentido do arduino
#GPIO.output(CP, GPIO.LOW);
class thread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global delayligado
        ligar(delayligado);
    




def subir():
    GPIO.output(EN, GPIO.LOW)
    QtTest.QTest.qWait(100)
    #sleep(1)
    GPIO.output(CW, GPIO.HIGH)
    QtTest.QTest.qWait(100)
    #sleep(1)
    GPIO.output(EN, GPIO.HIGH)

                
def baixar():
    GPIO.output(EN, GPIO.LOW)
    QtTest.QTest.qWait(100)
    #sleep(1)
    GPIO.output(CW, GPIO.LOW)
    QtTest.QTest.qWait(100)
    #sleep(1)
    GPIO.output(EN, GPIO.HIGH)

    
def ligar(tempo):
    a = time()
    
    global parou
    global flag
    parou = 0
    print(tempo,parou)
    pwm=GPIO.PWM(CP,float(tempo)*0.96)


    
    while(parou == 0):
        """if(time() -a  >59):
            parou = 1
            Parar()"""
            
        pwm.start(1)
    print("saiu thread")
        
       


        
        

        
    
def Parar():
    global parou
    parou = 1 
    GPIO.output(EN, GPIO.LOW)
    


def calcular(valor) :
 
 global delayligado
 thr= thread()
 valor = float(valor)
 velocidadei = valor;
 if (valor >= 8 and valor <= 14) :
    #fator escolhido 256
    # menor que 0.6 a maquina não roda...
    delayligado =  4.166666666666667*valor  + 16.666666666666664;
    #Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()
    
 if (valor > 14  and valor <= 16) :
    #fator escolhido 256
    # menor que 0.6 a maquina não roda...
    delayligado =  12.5*valor  - 100;
    #Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()
 if (valor > 16  and valor <= 21) :
    #fator escolhido 256
    # menor que 0.6 a maquina não roda...
    delayligado =  5*valor  + 20;
    #Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()
 if (valor > 21  and valor <= 26) :
    #fator escolhido 256
    # menor que 0.6 a maquina não roda...
    delayligado =  5*valor  + 20;
    #Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()
 if (valor > 26  and valor <= 33) :
    #fator escolhido 256
    # menor que 0.6 a maquina não  roda...
    delayligado =  7.142857142857143*valor  - 35.71428571428572;
    #Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()
    
 if (valor > 33  and valor <= 45) :
    #fator escolhido 256
    # menor que 0.6 a maquina não roda...
    delayligado =  4.166666666666667*valor  + 62.5;
    #Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()



  
 elif(valor > 45 and valor <= 49 ) :
    delayligado = 12.5*valor -312.5;
    #Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()

    #Fator escolhido é o 128
  
 elif(valor > 49 and valor <= 58) :
    #fator escolhido é o 64
    delayligado =  5.555555555555555*valor  + 27.77777777777777

    #Serial.println(delayligado);

    #ligar(delayligado);
    thr.start()
  
 elif(valor > 58 and valor <=  67) :#ta ruim

    #fator escolhido é o 50
    delayligado =  5.555555555555555*valor + 27.77777777777777;
    # Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()
  
 elif(valor > 67 and valor <= 73) :
    #fator escolhido é o 40
    delayligado = 8.333333333333334 *valor -158.33333333333337;
    # Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()
  
 elif(valor > 73 and valor <= 83) :
    #fator escolhido é o 32
    delayligado =  5 *valor  + 85

    #Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()
  
 elif(valor > 83 and valor <= 87) :
    #fator escolhido é o 32
    delayligado = 10*valor -330;

    #Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()
  
 elif(valor > 87 and valor <= 97) :
    #fator escolhido é o 32
    delayligado = 6*valor+18;

    #Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()
  
 elif(valor > 97 and valor <= 106) : #aqui
    #fator escolhido é o 32
    delayligado =  5.555555555555555*valor +61.111111111111086

    #Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()
  
 elif(valor > 106 and valor <= 113) :
    #fator escolhido é o 32
    delayligado =7.142857142857143 *valor -107.14285714285722

    #Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()
  
 elif(valor > 113 and valor <= 119) :
    #fator escolhido é o 32
    delayligado =8.333333333333334*valor -241.66666666666674

    #Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()
  
 elif(valor > 119 and valor <= 126) :
    #fator escolhido é o 32
    delayligado =  7.142857142857143*valor- 100;

    #Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()
  
 elif(valor > 126 and valor <= 133) :
    #fator escolhido é o 32
    delayligado = 7.142857142857143*valor - 100

    #Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()
  
 elif(valor > 133 and valor <=  141) :
    #fator escolhido é o 32
    delayligado = 4.545454545454546*valor + 245.45454545454538

    #Serial.println(delayligado);
    #ligar(delayligado);
    thr.start()
 elif(valor > 141 and valor <=  175) :
     delayligado = 6.323529411764706* valor +8.382352941176464
     thr.start()
     

    
def Subir_descer(vel,controle,deslocamento):
    thr2= thread2(vel,deslocamento)
    
    if(int(controle) == 1):
        subir()
    else:
        baixar()
   
    
    calcular(str(vel))
    thr2.start()
    """tempo = time()
    while( ((time() - tempo)/60)*float(vel) <= deslocamento):
        print(((time() - tempo)/60)*float(vel))
        print("no while")
        pass


    Parar()"""

    


        


        


"""
while(True):
        
        print(flag) 
        if(flag == 0):
            print("aqui")
            GPIO.output(CP, GPIO.HIGH)
            sleep(0.000000045)
            #sleep(0.45)
            flag = 1
        elif(flag ==1):
            flag = 0
            print("ta 1")
            GPIO.output(CP, GPIO.LOW)
            sleep(0.000000045)
            #sleep(0.45)
            flag = 0"""
# pwm=GPIO.PWM(CP,(1/(625.0/1000000)))
#A= calcular(87) Problema
"""GPIO.output(EN, GPIO.HIGH)

pwm=GPIO.PWM(CP,7)


a = time()
subir()
pwm.start(1)
while(True):
    print("A")
    if( time()-a > 59):
        
        GPIO.output(EN, GPIO.LOW)

        
    pwm.start(1)"""
    
    




  

  




    

        
    
    
    
