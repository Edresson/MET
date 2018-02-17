# -*- coding: utf-8 -*-
import pygame
import sys 
import os
#from qtpy import QtCore, QtGui

from PyQt5 import QtCore, QtGui, QtWidgets,QtTest
import time
from matplotlib.figure import Figure
#from  qtpy import QtTest
from threading import  Thread
#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import threading
import matplotlib.pyplot as plt 
import math
import pickle
##### imports celula e motor####
#from Modulos import celula
from Modulos import clientMotor
Motor = clientMotor

from Modulos import clientCelula
celula = clientCelula

from Modulos import  webcam

#from Modulos import celula
#
#from Modulos import celula


### PDF Imports ###

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm, inch, pica
import os.path
from datetime import datetime
from reportlab.lib.utils import ImageReader
from io import BytesIO
from PIL import Image
from reportlab.pdfbase.pdfmetrics import stringWidth


webc = webcam.Webcam()

celping = celula.ping()
motping= Motor.ping()


log_file=open('MET_Logs.log', 'w')


if  celping[0] == 0:
                        
     print("Aparentemente  o Raspberry Pi não está  connectado no Roteador, ou aconteceu algo de errado com o mesmo,Verifique se o mesmo está com o IP:",celping[1]," Se ele está connectado no mesmo roteador que  o Notebook , ou ainda se a Porta UDP :",celping[2]," não está em uso por outro serviço nesta rede \n \n",file=log_file)
     
    #nao está pingando
else:
    print(" Ping Ok ! Raspberry Pi está configurado corretamente \n",file=log_file)
    

if  motping[0] == 0:
     print("Aparentemente  o Raspberry Pi não está  connectado no Roteador, ou aconteceu algo de errado com o mesmo,Verifique se o mesmo está com o IP:",motping[1]," Se ele está connectado no mesmo roteador que  o Notebook , ou ainda se a Porta UDP :",motping[2]," não está em uso por outro serviço nesta rede\n \n",file=log_file)
     
    #nao está pingando
else:
    print(" Ping Ok ! Raspberry Pi está configurado corretamente \n"," Caso não seja altere no arquivo IP-Raspberry.txt ",file=log_file)


if motping[0] == 1 and celping[0] == 0 :
     
     print(" Aparentemente o Problema está com a port UDP: ",celping[2]," Você pode ter aberto 2 instancias do software ao mesmo tempo , reinicie o Notebook, se persistir reiniciei também o RaspBerry Pi",file=log_file)
     sys.exit()
elif motping[0] == 0 and celping[0] == 1 :  
     print(" Aparentemente o Problema está com a port UDP:",motping[2]," Caso não seja altere no arquivo IP-Raspberry.txt ",file=log_file)
     sys.exit()
    
elif motping[0] == 0 and celping[0] == 0:
    print(" Aparentemente o Problema está  no Raspberry Pi, Verifique se o ip dele é mesmo:",motping[1],file=log_file)
    sys.exit()

Motor.start_thread()    
testes = []
contando = 0
fig = plt.figure(figsize=(9,9))





tipodeensaio = 0 
FormatoCorpoProva = 0
AreaCorpoProva = 0
deslocamentos = []
forcas = [] 
flag = 0 
flag2 =0      
tempinicioteste = 0
qforca = None
maxforca = None
maxdeslocamento = None
VelocidadeEn = 0
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)





class Ui_MainWindow():

    def __init__(self):
        self.result= QtWidgets.QMessageBox()
        

             
        self.result.setText("Você deseja fazer mais um teste nesse lote?")
        
        self.result.addButton(QtWidgets.QMessageBox.Yes)
        self.result.addButton(QtWidgets.QMessageBox.No)

        self.webcam_fim= QtWidgets.QMessageBox()
        

             
        self.webcam_fim.setText("Você deseja tirar uma foto do objeto?")
        
        self.webcam_fim.addButton(QtWidgets.QMessageBox.Yes)
        self.webcam_fim.addButton(QtWidgets.QMessageBox.No)

        
        self.ensaiologin = False
        self.filedir = 0
        

    
        self.u = []
        self.thread3 = ServerThread()
        
        self.Index=0
        self.Index22 =0
        self.text= str()
        self.A = []
        self.Linhas=[]
        
        
        self.Grafic = QtWidgets.QWidget()
        self.Grafic.setObjectName(_fromUtf8("Grafic"))
        
        self.verticalLayoutWidget = QtWidgets.QWidget(self.Grafic)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 80, 871, 411))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.frame = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.frame.setObjectName(_fromUtf8("verticalLayout_2"))
        self.t=1

       
        
        self.fig = Figure(figsize=(5,5), dpi=100)
        self.ax1f1 = self.fig.add_subplot(111,xlabel='Deslocamento(mm)', ylabel='Força(N)', title='')
        self.canvas = FigureCanvas(self.fig)
        self.line1, =self.ax1f1.plot([],[])
        self.fig.canvas.draw()
        self.ax1f1.grid(True)
        
        
        
        self.canvas = FigureCanvas(self.fig)
        
        self.frame.addWidget(self.canvas)
        
        self.canvas.draw()
        
        self.toolbar = NavigationToolbar(self.canvas, 
                 self.Grafic, coordinates=True)
        
        self.frame.addWidget(self.toolbar)

    

        
        
    
        
        
        
    def selecionar(self):

        text = self.combo.currentText()
        self.text = text.replace("                                               Celula de Carga Fator:",";")


        
        self.t = ''
        for i in self.text:
            
            if(i != ';'):
                self.t = self.t + i

            else:
                self.t =''
        
        #print(self.text,self.t)
        self.CALIBRA = open("Fator_Calibracao.txt","w")
        self.CALIBRA.write(self.t)
        self.CALIBRA.close()
        celula.iniciarcel(self.t)
        self.updateCelulaInterface()
        self.obs3.setGeometry(QtCore.QRect(20,190,741,41))
        self.obs3.setText(_translate("MainWindow", "Celula: "+self.text+" Selecionada, Agora a maquina Opera com esta Celula de Carga",None))
        self.obs3.show()
        

        

        

    def combo2_chosen(self, text=0):

        text = self.combo2.currentText()
        self.Index=self.combo2.currentIndex()
        
       
            
        self.Index22 = str(text)
       
        

        
    def combo_chosen(self, text=0):
       
        text = self.combo.currentText()
        self.Index=self.combo.currentIndex()
        self.text = text.replace("                                               Celula de Carga Fator:",";")
        


        
    def Excluir(self):
        self.combo.removeItem(self.Index)
        
        for i, valor in enumerate(self.A):
        
            
            if valor == self.text:
                
                self.A.pop(i)
                
                self.CALIBRA = open("conf_celulas.txt","w")
                for i in self.A:
                   self.CALIBRA.write(str(i))
                   
                self.CALIBRA.close()
        
        self.obs3.setGeometry(QtCore.QRect(20,190,741,41))
        self.obs3.setText(_translate("MainWindow", "Celula: " +self.text+ " Excluida",None))
        self.obs3.show()




        
    def ecalibrar(self):
        
        
        self.bcal.hide()
        self.ecal.hide()
        self.obs3.setText(_translate("MainWindow", "Calibrando Celula de Carga Aguarde ! ",None))
        
        
        VALUE_SERIAL= celula.calibrar()
        B = self.pcal.value()
        Fator= (float(VALUE_SERIAL)/float(B))
        print(Fator,B,VALUE_SERIAL)
        
         
                    
                
       
        
        self.combo.clear()
       
        self.t = str()
        for i, valor in enumerate(self.A):
        
            if valor == self.text:
                self.posicao = i
                
                self.p = 0
                self.j =0
                while(self.p == 0):
                    
                    if(self.A[i][self.j] != ';'):
                        self.t= self.t + self.A[i][self.j]
                        self.j += 1
                        

                        
                    else:
                        self.p =1
                        
                
        
                

                self.A.pop(i)
                self.A.append(self.t+";"+str(Fator)+"\n")
                
                
                self.CALIBRA = open("conf_celulas.txt","w")
                for k in self.A:
                    
                    
                   self.CALIBRA.write(k)
                   
                self.CALIBRA.close()
                

    
        
        self.bcal2.hide()
        self.obs3.setText(_translate("MainWindow", "Celula de Carga Calibrada agora você já pode Colocar novamente as Garras/Mordentes\n Celula: "+self.t,None))
        
        self.bcal.show()
        self.ecal.show()
        
        self.pcal.hide()
        
        
        
        
        
    def editCalibra(self):
        
        self.bcal2.hide()
        self.obs3.hide()

        celula.tare()
        
        self.pcal = QtWidgets.QDoubleSpinBox(self.Calibra)
        self.obs3 = QtWidgets.QLabel(self.Calibra)
        
        
        self.bcal2 = QtWidgets.QPushButton(self.Calibra)
        self.bcal.hide()
        self.ecal.hide()
        self.pcal.setGeometry(QtCore.QRect(210,240,81,29))
        self.pcal.setObjectName(_fromUtf8("pcal"))
        self.pcal.setRange(0,10000.00)
        self.pcal.setValue(1.00)
        
        self.pcal.show()

        
        self.obs3.setGeometry(QtCore.QRect(20,190,741,71))
        self.obs3.setObjectName(_fromUtf8("obs"))
        self.obs3.setText(_translate("MainWindow", "Informe o Valor do Peso Padrão (EM KG), após coloque o mesmo na celula de Carga e Clique em continuar.",None))
        self.obs3.show()
                

        
       
        self.bcal2.setGeometry(QtCore.QRect(190,340,151,21))
        self.bcal2.setObjectName(_fromUtf8("bcal"))
        self.bcal2.setText(_translate("MainWindow", "Continuar",None))
        self.bcal2.show()
        self.bcal2.clicked.connect(self.ecalibrar)
        
        
    

        
    def editcalib(self):
        
        self.combo.hide()
        self.bcal2 = QtWidgets.QPushButton(self.Calibra)
        self.bcal2.setGeometry(QtCore.QRect(190,340,151,21))
        self.bcal2.setObjectName(_fromUtf8("bcal"))
        self.bcal2.setText(_translate("MainWindow", "Continuar",None))
        self.bcal2.clicked.connect(self.editCalibra)

        self.bcal2.show()
        self.bcal.hide()
        self.ecal.hide()
        self.ccal.hide()
        self.dcal.hide()
        self.scal.hide()
        
        
        
        self.obs3.setGeometry(QtCore.QRect(20,190,741,41))
        self.obs3.setObjectName(_fromUtf8("obs"))
        self.obs3.setText(_translate("MainWindow", "OBS: Retire as Garras/Mordentes da Celula de Carga, Não deixe nada apenas a Celula de Carga, após Clique em Continuar.",None))
        self.obs3.show()
        


        
    
        
        
    def add_nova(self):

       
        self.combo.hide()
        self.obs3.hide()
        self.bcal2 = QtWidgets.QPushButton(self.Calibra)
        self.bcal2.setGeometry(QtCore.QRect(190,340,151,21))
        self.bcal2.setObjectName(_fromUtf8("bcal"))
        self.bcal2.setText(_translate("MainWindow", "Continuar",None))
        self.bcal2.clicked.connect(self.calibrar)

        self.bcal2.show()
        self.bcal.hide()
        self.ecal.hide()
        self.scal.hide()
        
        
        
        self.obs3.setGeometry(QtCore.QRect(20,190,741,41))
        self.obs3.setObjectName(_fromUtf8("obs"))
        self.obs3.setText(_translate("MainWindow", "OBS: Retire as Garras/Mordentes da Celula de Carga, Não deixe nada apenas a Celula de Carga, após Clique em Continuar.",None))
        self.obs3.show()
        

    def Editar(self):
        self.scal.show()
        self.obs3.hide()
        self.ecal.hide()
        self.bcal.hide()
        self.ccal = QtWidgets.QPushButton(self.Calibra)
        self.ccal.setGeometry(QtCore.QRect(150,110,131,29))
        self.ccal.setObjectName(_fromUtf8("bcal"))

        self.dcal = QtWidgets.QPushButton(self.Calibra)
        self.dcal.setGeometry(QtCore.QRect(530,110,151,29))
        self.dcal.setObjectName(_fromUtf8("bcal"))

        
        self.combo.setGeometry(QtCore.QRect(290,20,192,40))
        self.combo.setObjectName(_fromUtf8("pcal"))
        self.combo.show()
        self.dcal.setText(_translate("MainWindow", "Excluir",None))
        self.ccal.setText(_translate("MainWindow", "Calibrar",None))
        self.dcal.clicked.connect(self.Excluir)
        self.ccal.clicked.connect(self.editcalib)
        self.ccal.show()
        self.dcal.show()

        self.CALIBRA = open("conf_celulas.txt","r")
        self.A = self.CALIBRA.readlines()
        self.CALIBRA.close()
        self.CALIBRA = open("conf_celulas.txt","a")
        
        self.b=[]
        
        for i in range(len(self.A)):
            self.b.append(self.A[i].replace(";","                                               Celula de Carga Fator:"))
        
        self.combo.addItems(self.b)
        
        #self.combo.connect(self.combo, QtCore.SIGNAL('activated(QString)'), self.combo_chosen)
        self.combo.activated.connect(self.combo_chosen)
        
        self.CALIBRA.close()
        
        
        


        
    def resetgrafic(self):
        
        deslocamentos= [0]
        forcas= [0]
        self.PlotGrafico()
        
    def PlotGrafico(self):
        
        
        
       
        self.line1.set_data(deslocamentos, forcas)
        
        self.fig.canvas.draw()
        
        
        
    def zeraf(self):
        
        self.Forca_grafic.setValue(0.00)
    
    def zerades(self):
        self.Deslocamento_grafic.setValue(0.00)
        
    def Subir(self):
        self.pushButton_3.setDisabled(True)
        self.pushButton_2.setVisible(True)
        self.pushButton_3.setVisible(True)
        
        self.parar_ajuste.setVisible(True)
        
        Motor.Subir_descer(self.Vel_ajuste.value(),1,self.deslb.value())
        self.pushButton_3.setDisabled(False)

    def Descer(self):
        self.pushButton_2.setVisible(True)
        self.pushButton_3.setVisible(True)
        self.parar_ajuste.setVisible(True)
        Motor.Subir_descer(self.Vel_ajuste.value(),2,self.deslb.value())

    def Parando(self):
       
        global flag
        flag =0
        global flag2
        global deslocamentos
        global forcas
        global testes
        self.u = []
        flag2 =0
        
        self.pushButton_2.setVisible(True)
        self.pushButton_3.setVisible(True)
        self.parar_ajuste.setVisible(True)
        
        
        
        self.pushButton.setVisible(True)
        self.pushButton_4.setVisible(False)
        self.emergrafic.setVisible(False)
        Motor.Parar()




        


        self.confirmar_continuacao()
        

    def confirmar_continuacao(self):
        
        result_webcam_fim = self.webcam_fim.exec_()
       
        if result_webcam_fim == QtWidgets.QMessageBox.No:
            pass

            
        if result_webcam_fim== QtWidgets.QMessageBox.Yes:
            self.webcamcapture_final()
     

            
        
        
        result1 = self.result.exec_()
        if result1 == QtWidgets.QMessageBox.Yes:
            
            self.Config.setCurrentWidget(self.Config)
            lotes(self.input.text(),deslocamentos,forcas)
            self.Config.setCurrentWidget(self.Config_2)
            
            
            
            
        if result1 == QtWidgets.QMessageBox.No:
            
            self.inputl.show()
            self.input.show()
            self.botaobrowser.show()
            lotes(self.input.text(),deslocamentos,forcas,)
            self.ax1f1.cla()
            self.ax1f1.grid(True)
            self.pushButton.hide()
            
            
            if(len(testes) > 0):
                 pass
                 
            self.Linhas = []
            
            self.combo2.setGeometry(QtCore.QRect(90,20,192,30))
            self.combo2.setObjectName(_fromUtf8("p2cal"))
            self.combo2.show()
            
            
            self.bcombo.setGeometry(QtCore.QRect(90,50,61, 31))
            self.bcombo.setText(_translate("MainWindow", "Excluir", None))
            self.bcombo.clicked.connect(self.excluirlinha_grafic)
            self.bcombo.setObjectName(_fromUtf8("p2cal"))
            self.bcombo.show()
           
        
            for i in range(0,len(testes)):
                           
                           
                self.u.append(testes[i]["nome"])
               
                
                self.aux, = self.ax1f1.plot(list(testes[i]["x1"]),list(testes[i]["x2"]),label='${i}$'.format(i=str(testes[i]["nome"])))
                self.Linhas.append(self.aux)
                self.ax1f1.legend(loc ='best') 
                self.fig.canvas.draw()
        
            self.combo2.addItems(self.u)
            
            #self.combo2.connect(self.combo2, QtCore.SIGNAL('activated(QString)'), self.combo2_chosen)
            self.combo2.activated.connect(self.combo2_chosen)
            
            
            contando = 0
            self.pushButton_6.show()
            self.pushButton_7.show()
            
        
        

            

            
            pass



        
    def returnposteste(self,index):
        global testes
        
        for i in range(0,len(testes)):
            
            if(str(testes[i]["nome"]) == str(index)):
                return i
            
    def cancelartestes(self) :
        global testes
        global contando
        contando = 0
        testes = []
        self.bcombo.hide()
        self.combo2.clear()
        self.pushButton_6.hide()
        self.pushButton_7.hide()
        self.combo2.hide()
        self.ax1f1.cla()
        self.ax1f1.grid(True)
        self.line1, = self.ax1f1.plot([],[])
        
        self.fig.canvas.draw_idle()
        self.pushButton.show()
    
        
        
        
    
    def gerarpdf(self):
        
        global testes
        self.bcombo.hide()
        self.pushButton_6.hide()
        self.pushButton_7.hide()
        global VelocidadeEn
        global forcas
        global deslocamentos
        global FormatoCorpoProva
        global fig
        fig2 = []
        Image2 = []
        imgdata2 = []
        
       
        now = datetime.now()
        


        if os.path.isdir("Ensaios/"+str(now.year)): # vemos de este diretorio já existe
             pass
        else:
          os.mkdir("Ensaios/"+str(now.year)) # aqui criamos o diretorio
          
     


            


        if os.path.isdir("Ensaios/"+str(now.year)+"/"+str(now.month)): # vemos de este diretorio já existe
             pass
        else:
          os.mkdir("Ensaios/"+str(now.year)+"/"+str(now.month)) # aqui criamos o diretorio
          


        if os.path.isdir("Ensaios/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day)): # vemos de este diretorio já existe
             pass
        else:
          os.mkdir("Ensaios/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day)) # aqui criamos o diretorio
          
        if os.path.isdir("Ensaios/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day)+"/"+str(self.input.text())+"Hora"+str(now.hour)+"-"+str(now.minute)+ "-"+ str(now.second)): # vemos de este diretorio já existe
             pass
        else:
          os.mkdir("Ensaios/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day)+"/"+str(self.input.text())+"Hora"+str(now.hour)+"-"+str(now.minute)+ "-"+ str(now.second)) # aqui criamos o diretorio
        listdir1 = os.listdir('TempImagens/')
        print(os.listdir('TempImagens/'))
        for i in listdir1:
               
               os.system('mv '+'TempImagens/'+i+" Ensaios/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day)+"/"+str(self.input.text())+"Hora"+str(now.hour)+"-"+str(now.minute)+ "-"+ str(now.second)+"/"+str(i))



        Forcamaxima = forcas[-1]
        maxdeslocamento = deslocamentos[-1]
        Posicaomaxima = deslocamentos[-1]


        



        pdf2 = Canvas("Ensaios/"+"Ensaio_Atual.pdf", pagesize = letter) #Nome do arquivo e Tipo do papel
        
        pdf = Canvas("Ensaios/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day)+"/"+str(self.input.text())+"Hora"+str(now.hour)+"-"+str(now.minute)+ "-"+ str(now.second)+"/"+str(self.input.text())+"Hora:"+str(now.hour)+"-"+str(now.minute)+ "-"+ str(now.second)+".pdf", pagesize = letter) #Nome do arquivo e Tipo do papel
        

        pdf.setFont('Helvetica-Bold', 12)
        
        pdf2.setFont('Helvetica-Bold', 12)
        
        tupla = ('                                      Máquina de Ensaio de Tração e Compressão', '','','','','','','','', '                                                       Ensaio','', 'N° da Solicitação: _________', 'Solicitante/Setor: __________________________________','Inspetor: ___________________________________','Responsável: ___________________________________','' ,
                 'Data: ' + str(now.day)+'/'+str(now.month)+'/'+str(now.year),  'Hora: ' + str(now.hour)+":"+str(now.minute)+ ":"+ str(now.second) ,'', '', '','' ,'')
        
        lista = pdf.beginText(inch * 1, inch * 10)
        

        lista2 = pdf2.beginText(inch * 1, inch * 10)
        

        
        for i in range(0,len(tupla)):
            lista.textLine(tupla[i])
            lista2.textLine(tupla[i])






        
        
        fig.clf()
        ax = fig.add_subplot(111,xlabel='Deslocamento(mm)', ylabel='Força(N)', title='')
       
        ax.grid(True)
        
        for i in range(0,len(testes)):
                           
                
                ax.plot(list(testes[i]["x1"]),list(testes[i]["x2"]),label='${i}$'.format(i=str(testes[i]["nome"])))
                ax.legend(loc ='best') 
                
                
       

        with open("Ensaios/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day)+"/"+str(self.input.text())+"Hora"+str(now.hour)+"-"+str(now.minute)+ "-"+ str(now.second)+"/"+"save.txt","wb") as fp:
            pickle.dump(testes,fp)
            
        """CALIBRA.write(str(testes)+"\n")
            
        CALIBRA.close()"""
        
        imgdata = BytesIO()
        fig.savefig(imgdata, format='png')
        imgdata.seek(0)  # rewind the data

        Image = ImageReader(imgdata)
        
        pdf2.drawText(lista2)
        pdf.drawText(lista)

        pdf2.drawImage(Image ,130,50, width=400,height=350)

        pdf.drawImage(Image ,130,50, width=400,height=350)
       
        pdf2.showPage()
        pdf.showPage()
        
        
        
        for j in range(0,len(testes)):
            
            
        
            
            
            
            fig.clf()
            ax2= fig.add_subplot(111,xlabel='Deslocamento(mm)', ylabel='Força(N)', title='')
            #ax2.cla()
            

            ax2.grid(True)
            ax2.plot(list(testes[j]["x1"]),list(testes[j]["x2"]))
            X = list(testes[j]["x1"]).copy()
            Y = list(testes[j]["x2"]).copy()
          
            X.sort()
            Y.sort()
            xmax = X[-1]
            ymax = Y[-1]
          
            
            if testes[j]["area"] == 0.0:
                 testes[j]["area"] = '_______'
                 
            tupla = ( '','','','','                                                 Nome Ensaio: '+str(testes[j]["nome"]),'','Tipo de ensaio: '+str(testes[j]["tipo"]) ,
                 'Formato do corpo de prova: '+str(testes[j]["formato"] ),
                 'Posição Máxima: '+str( xmax )+" mm",'Força Máxima: '+str(ymax)+'N', 'Área do corpo de prova: '+str(testes[j]["area"])+' mm²', 'Velocidadede ensaio: '+str(testes[j]["vel"])+' mm/min','Comprimento do corpo de prova: __________ mm' ,)
           
            lista3 = pdf.beginText(inch * 1, inch * 10)
           

            lista4 = pdf2.beginText(inch * 1, inch * 10)
            

            
            for i in range(0,len(tupla)):
                lista3.textLine(tupla[i])
                lista4.textLine(tupla[i])

                      
            pdf.drawText(lista3)
            
            imgdata2 = BytesIO()
            fig.savefig(imgdata2 , format='png')
            imgdata2.seek(0)  #  rewind the data

            Image2 = ImageReader(imgdata2)
            
            pdf2.drawText(lista3)
            pdf.drawText(lista4)

            pdf2.drawImage(Image2 ,130,50, width=400,height=350)

            pdf.drawImage(Image2 ,130,50, width=400,height=350)
        
            pdf2.showPage()
            pdf.showPage()

        
         
        pdf2.save()
        self.cancelartestes()
        
        


        

        
        pdf.save()


        x = [0]
        y = [0]
        
       
        

        
        
    def excluirlinha_grafic(self):
        global testes
        self.line1.set_data([],[])
        
        self.combo2.removeItem(self.Index)
        
        try:
            self.idx = int(self.returnposteste(self.Index22))
        except:
            pass
        
        try:
            self.Linhas[self.idx].set_data([], [])
            
        except:
            pass
        
        testes.pop(self.idx)
        self.ax1f1.cla()
        self.Linhas = []
        for i in range(0,len(testes)):
                           
                           
                self.u.append(testes[i]["nome"])
                
                
                self.aux, = self.ax1f1.plot(list(testes[i]["x1"]),list(testes[i]["x2"]),label='${i}$'.format(i=str(testes[i]["nome"])))
                self.Linhas.append(self.aux)
                
        self.ax1f1.legend(loc ='best') 
        
        self.ax1f1.grid(True)  
        
        self.fig.canvas.draw_idle()


        
    def Parando3(self,i = None):
        global flag2
        global flag
        flag = 0
        flag2 =0
        
        self.pushButton_2.setVisible(True)
        self.pushButton_3.setVisible(True)
        self.parar_ajuste.setVisible(False)
        
        self.pushButton.setVisible(True)
        self.pushButton_4.setVisible(False)
        self.emergrafic.setVisible(False)
        """deslocamentos = [0]
        forcas = [0]
        self.Deslocamento_grafic.setValue(float(0.00))
        self.Forca_grafic.setValue(float(0.00))
        self.ax1f1.set_ylim(0, forcas[-1]+10)
        self.ax1f1.set_xlim(0, deslocamentos[-1]+10)
        self.line1.set_data(deslocamentos,forcas)
        self.fig.canvas.draw()"""           
        
        
        Motor.Parar()
        self.confirmar_continuacao()
        
    
    def Parando2(self):
        
        global flag2
        flag2 =0
        self.pushButton_2.setVisible(True)
        self.pushButton_3.setVisible(True)
        self.parar_ajuste.setVisible(True)
        Motor.Parar()
        

    def verificar_Browser_Ensaio(self):
            try:
                 with open(str(self.filedir[0]),"rb") as fp:
                     testes = pickle.load(fp)
                 return 1    
               
            except:
                 self.ensaiologin = False
                 self.res= QtWidgets.QMessageBox()
        
             
                 self.res.setText("Aparentemente você selecionou o arquivo de Browser Ensaio incorretamente, você deve selecionar o arquivo save.txt, você deseja tentar novamente e tentar continuar um antigo teste?")
        
                 self.res.addButton(QtWidgets.QMessageBox.Yes)
                 self.res.addButton(QtWidgets.QMessageBox.No)
                 result1 = self.res.exec_()
                 if result1 == QtWidgets.QMessageBox.Yes:
                       self.func_browser()
                       return self.verificar_Browser_Ensaio()
                    
                 
            
            
                 if result1 == QtWidgets.QMessageBox.No:
                     return 0
               
                    
         
    def iniciar(self):
        
        global deslocamentos
        global forcas
        global testes
        global contando 
        self.inputl.hide()
        self.input.hide()
        self.botaobrowser.hide()
        if(self.ensaiologin == True and self.ensaiologin != None ):
             resul= self.verificar_Browser_Ensaio()
             if resul == 1:
                 with open(str(self.filedir[0]),"rb") as fp:
                     testes = pickle.load(fp)
                 contando = len(testes)
                 self.ensaiologin = False
             else:
                 self.ensaiologin = False
          
             
                     
            
        try:    
             arquivo = open("Fator_Calibracao.txt","r")
             fator = arquivo.readline()
             celula.iniciarcel(str(fator))
        except:
             print("O Arquivo Fator_Calibracao.txt, está corrompido ou foi excluido você não pode iniciar  o ensaio sem este arquivo, solução: vá até a interface ,selecione a aba celula de carga e escolha novamente a celula de carga isso irá criar o arquivo novamente. \n",file=log_file)
             sys.exit()
             
             

        self.Config.setCurrentWidget(self.Grafic)
        
        deslocamentos = [0]
        forcas = [0]

        self.Linhas = []

                        
        self.pushButton_2.setVisible(False)
        self.pushButton_3.setVisible(False)
        
        self.parar_ajuste.setVisible(False)
        
        
        self.pushButton.setVisible(False)
        self.pushButton_4.setVisible(True)
        self.emergrafic.setVisible(True)
        global flag2
        global qforca
        global maxforca
        global maxdeslocamento
        global tempinicioteste
        global VelocidadeEn
        global tipodeensaio
            
        
        if(self.checkBox.isChecked() == True):
            
            #Motor.subir()
            Motor.Subir_descer(self.Velocidade.value(),1,0)
            tipodeensaio = "Tração"
        else:
            Motor.Subir_descer(self.Velocidade.value(),0,0)
            tipodeensaio = "Compressão"
            
            #Motor.baixar()
            
        VelocidadeEn = self.Velocidade.value()    
        #Motor.calcular( float(VelocidadeEn) )   
        
        tempinicioteste = time.time()
        
        if(self.checkBox_3.checkState() == 2):
            qforca = self.Velocidade_2.value()
        else:
            qforca = None
        if(self.checkBox_4.checkState() == 2):
    
            
            max_forca= self.Velocidade_3.value()
        else:
            
            max_forca = None
        if (self.checkBox_5.checkState() == 2):
            maxdeslocamento= self.Velocidade_4.value()
        else:
            
            maxdeslocamento= None 
            
       

       
        if(self.checkBox_6.isChecked() == True):
            
            a = self.a_retangulo.value()
            b = self.b_retangulo.value()
            
        else:
            a =None
            b = None
        if(self.checkBox_7.isChecked() == True):
            c = self.Velocidade_8.value()
            d = self.d_retangulo.value()
            
        else:
            c =None
            d = None
        if(self.checkBox_8.isChecked() == True):
            e = self.D_cilimdro.value()
            f = self.H_cilindro.value()
        else:
            e =None 
            f = None
        Area(a,b,c,d,e,f)
        
        flag2 =1
        

        
        self.thread3.start()
        self.thread3.UPsig.connect(self.update1)
        self.thread3.Stopsig.connect(self.Parando3)
        
        
        
        
        #QtWidgets.QWidget.connect(self.thread3, QtCore.SIGNAL("UP"), self.update1)
        #QtWidgets.QWidget.connect(self.thread3, QtCore.SIGNAL("Parando"), self.Parando3)
        
        
    def update1(self,lista):
        
                        
                        
                        self.Deslocamento_grafic.setValue(lista[0])
                        self.Forca_grafic.setValue(float(lista[1])*9.8)
                        self.ax1f1.set_ylim(0, lista[2])
                        self.ax1f1.set_xlim(0, lista[3])
                        self.line1.set_data(lista[4],lista[5])
                        self.fig.canvas.draw_idle()
                        
                        
            
    def calibrar(self):
        
        celula.tare()
        
        self.bcal2.hide()
        self.obs3.hide()
        self.pcal = QtWidgets.QDoubleSpinBox(self.Calibra)
        self.obs3 = QtWidgets.QLabel(self.Calibra)
        self.obs4 = QtWidgets.QLabel(self.Calibra)
        self.qline = QtWidgets.QLineEdit(self.Calibra)
        self.bcal2 = QtWidgets.QPushButton(self.Calibra)
        self.bcal.hide()
        self.ecal.hide()
        self.pcal.setGeometry(QtCore.QRect(210,240,81,29))
        self.pcal.setObjectName(_fromUtf8("pcal"))
        self.pcal.setRange(0,3000.00)
        self.pcal.setValue(1.00)
        
        self.pcal.show()

        
        self.obs3.setGeometry(QtCore.QRect(20,190,741,41))
        self.obs3.setObjectName(_fromUtf8("obs"))
        self.obs3.setText(_translate("MainWindow", "Informe o Valor do Peso Padrão (EM KG), após coloque o mesmo na celula de Carga , de um nome para a nova celula e Clique em continuar.",None))
        self.obs3.show()

        
        self.qline.setGeometry(QtCore.QRect(180,300,151,21))
        self.qline.show()
        
        

        self.obs4.setGeometry(QtCore.QRect(180,280,151,21))
        self.obs4.setObjectName(_fromUtf8("obs"))
        self.obs4.setText(_translate("MainWindow", "Nome da Celula:",None))
        self.obs4.show()
                

        
       
        self.bcal2.setGeometry(QtCore.QRect(190,340,151,21))
        self.bcal2.setObjectName(_fromUtf8("bcal"))
        self.bcal2.setText(_translate("MainWindow", "Continuar",None))
        self.bcal2.show()
        self.bcal2.clicked.connect(self.Ccalibrar)
    
        
        
       
        
            

    
        
    def Ccalibrar(self):
        self.bcal.hide()
        self.ecal.hide()
        self.obs3.setText(_translate("MainWindow", "Calibrando Celula de Carga Aguarde ! ",None))
        
        
        VALUE_SERIAL=celula.calibrar()
        
        
        

            
        
        
        B = self.pcal.value()
        Fator= (float(VALUE_SERIAL)/float(B))
        
        
        
        A = self.qline.text()
        
        self.CALIBRA = open("conf_celulas.txt","r")
        self.A = self.CALIBRA.readlines()
        
        self.CALIBRA.close()
        self.t= ''
        self.C = []
        self.posicao = 0
        for i, valor in enumerate(self.A):
        
                 
                
                self.p = 0
                self.j =0
                while(self.p == 0):
                    
                    if(self.A[i][self.j] != ';'):
                        self.t= self.t + self.A[i][self.j]
                        self.j += 1
                        

                        
                    else:
                        self.p =1
                        self.C.append(self.t.replace("\n",""))
                        self.t =''
                        if(self.t.replace("\n","") == A):
                            self.posicao = i
                        
                        
                        
                        
                
        

        
        if(A != self.C[self.posicao]):
            CALIBRA = open("conf_celulas.txt","a")
            CALIBRA.write(str(A)+";")
            CALIBRA.write(str(Fator)+"\n")
        
            CALIBRA.close()
        
            
        
        
            self.bcal2.hide()
            self.obs3.setText(_translate("MainWindow", "Celula de Carga calibrada agora você já pode Colocar novamente as Garras/Mordentes\n Celula:"+str(A),None))
            self.obs4.hide()
            self.obs3.hide()
            self.pcal.hide()
            self.qline.hide()
            self.bcal2.hide()
            self.bcal.show()
            self.ecal.show()
            self.bcal2.hide()

        else:
            self.bcal2.hide()
            self.obs3.setText(_translate("MainWindow", "Não foi Adicionado a Nova Celula, pois a celula com o nome:"+str(A)+"já existe vá em editar para recalibra-la",None))
            self.obs4.hide()
            self.pcal.hide()
            self.qline.hide()
            self.bcal2.hide()
            self.bcal.show()
            self.ecal.show()
            self.bcal2.hide()
            
       

        
        
        
    
        



    def updateCelulaInterface(self):
        try: 
             CALIBRA = open("conf_celulas.txt","r")
        except:
             print("O Arquivo conf_celulas.txt, está corrompido ou foi excluido você não pode iniciar  o ensaio sem este arquivo, solução: Adicione uma versao antiga do arquivo, se não tiver crie o arquivo e adicione a seguinte linha: celulatest;100000   \n Após você deve ir na aba celula de carga no software e adicionar novamente suas celulas de cargas pois os cadastros anteriores foram perdidas\n",file=log_file)
             sys.exit()

             

        try:    
             arquivo = open("Fator_Calibracao.txt","r")
             fator = arquivo.readline()
        except:
             print("O Arquivo Fator_Calibracao.txt, está corrompido ou foi excluido você não pode iniciar  o ensaio sem este arquivo, solução: vá até a interface ,selecione a aba celula de carga e escolha novamente a celula de carga isso irá criar o arquivo novamente. \n",file=log_file)
             sys.exit()

             
        A =CALIBRA.readlines()
                
        CALIBRA.close()
        t= ''
        C = []
        posicao = 0
        for i, valor in enumerate(A):
            for j, text in enumerate(valor):
                if(text == ';'):
                    posicao = j+1
                    if(valor[posicao::] == fator):
                        posicao = posicao-1
                        self.input2.setText(_translate("MainWindow", "Celula de Carga: "+str(valor[:posicao]) ,None))
                        self.input2.show()
                        


        arquivo.close()
        CALIBRA.close()
        
                 
                
               



    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(924, 599)
        MainWindow.setMinimumSize(924, 599)
        MainWindow.setMaximumSize(924, 599)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.Config = QtWidgets.QTabWidget(self.centralwidget)
        self.Config.setGeometry(QtCore.QRect(0, 0, 961, 581))
        self.Config.setObjectName(_fromUtf8("Config"))
        self.Config_2 = QtWidgets.QWidget()
        self.Config_2.setObjectName(_fromUtf8("Config_2"))

        self.input = QtWidgets.QLineEdit(self.Config_2)
        
        self.input.setGeometry(QtCore.QRect(600, 20, 151, 21))
        self.input.setObjectName(_fromUtf8("input"))
        
        self.inputl = QtWidgets.QLabel(self.Config_2)
        self.inputl.setGeometry(QtCore.QRect(500, 20, 100, 21))
        self.inputl.setObjectName(_fromUtf8("inputl"))
        self.inputl.setText(_translate("MainWindow", "Nome do Lote:",None))
        self.inputl.show()
        self.input2 = QtWidgets.QLabel(self.Config_2)
        self.input2.setGeometry(QtCore.QRect(500, 50,210,21))
        self.input2.setObjectName(_fromUtf8("inputl"))
        #self.input2.setText(_translate("MainWindow", "Celula de Carga:",None))
        self.updateCelulaInterface()
        #self.input2.show()
        
        self.pushButton = QtWidgets.QPushButton(self.Config_2)
        self.pushButton.setGeometry(QtCore.QRect(40, 20, 151, 21))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        
        self.button_webcam = QtWidgets.QPushButton(self.Config_2)
        self.button_webcam.setGeometry(QtCore.QRect(250, 20, 151, 21))
        self.button_webcam.setObjectName(_fromUtf8("button_webcam"))

        self.combo_webcam = QtWidgets.QComboBox(self.Config_2)
        
        self.combo_webcam.setGeometry(QtCore.QRect(250, 60, 151, 21))
        self.combo_webcam.setObjectName(_fromUtf8("combo_webcam"))
        self.combo_webcam.show()
       
        clist = webc.cameralist()
        clist = clist[::-1]
        self.combo_webcam.addItems(clist)   
        

        
        self.t_ensaio = QtWidgets.QFrame(self.Config_2)
        self.t_ensaio.setGeometry(QtCore.QRect(50, 90, 201, 201))
        self.t_ensaio.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.t_ensaio.setFrameShadow(QtWidgets.QFrame.Raised)
        self.t_ensaio.setObjectName(_fromUtf8("t_ensaio"))
        
       
        

        
        self.label = QtWidgets.QLabel(self.t_ensaio)
        self.label.setGeometry(QtCore.QRect(50, 0, 101, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.checkBox = QtWidgets.QRadioButton(self.t_ensaio)
        self.checkBox.setGeometry(QtCore.QRect(20, 50, 151, 22))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox_2 = QtWidgets.QRadioButton(self.t_ensaio)
        self.checkBox_2.setGeometry(QtCore.QRect(20, 90, 161, 22))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.Velocidade = QtWidgets.QDoubleSpinBox(self.t_ensaio)
        self.Velocidade.setGeometry(QtCore.QRect(27, 160,81, 29))
        self.Velocidade.setObjectName(_fromUtf8("Velocidade"))
        self.Velocidade.setRange(8, 175 )
        self.Velocidade.setValue(10)
        
        self.label_2 = QtWidgets.QLabel(self.t_ensaio)
        self.label_2.setGeometry(QtCore.QRect(40, 130, 141, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtWidgets.QLabel(self.t_ensaio)
        self.label_3.setGeometry(QtCore.QRect(120, 170, 57, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.frame_2 = QtWidgets.QFrame(self.Config_2)
        self.frame_2.setGeometry(QtCore.QRect(270, 90, 361, 201))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.checkBox_3 = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_3.setGeometry(QtCore.QRect(30, 50, 161, 22))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))

        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(120, 0, 111, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.Velocidade_2 = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.Velocidade_2.setGeometry(QtCore.QRect(200, 50, 81, 21))
        self.Velocidade_2.setObjectName(_fromUtf8("Velocidade_2"))
        self.Velocidade_2.setRange(0,99.00)
        self.Velocidade_2.setValue(99.00)
        
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(210, 40, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.checkBox_4 = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_4.setGeometry(QtCore.QRect(30, 100, 161, 22))
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.Velocidade_3 = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.Velocidade_3.setGeometry(QtCore.QRect(200, 100, 81, 21))
        self.Velocidade_3.setObjectName(_fromUtf8("Velocidade_3"))
        self.Velocidade_3.setRange(0,10000.00)
       
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(210, 80, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.checkBox_5 = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_5.setGeometry(QtCore.QRect(30, 150, 161, 22))
        self.checkBox_5.setObjectName(_fromUtf8("checkBox_5"))
        self.Velocidade_4 = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.Velocidade_4.setGeometry(QtCore.QRect(200, 150, 81, 21))
        self.Velocidade_4.setObjectName(_fromUtf8("Velocidade_4"))
        self.Velocidade_4.setRange(0,5000.00)
        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setGeometry(QtCore.QRect(190, 130, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(280, 100, 57, 20))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtWidgets.QLabel(self.frame_2)
        self.label_9.setGeometry(QtCore.QRect(280, 160, 57, 20))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.t_ensaio_2 = QtWidgets.QFrame(self.Config_2)
        self.t_ensaio_2.setGeometry(QtCore.QRect(660, 90, 201, 201))
        self.t_ensaio_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.t_ensaio_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.t_ensaio_2.setObjectName(_fromUtf8("t_ensaio_2"))
        self.label_10 = QtWidgets.QLabel(self.t_ensaio_2)
        
        self.label_10.setGeometry(QtCore.QRect(40, 0, 101, 17))
        self.label_10.setObjectName(_fromUtf8("label_10"))

        self.desl = QtWidgets.QLabel(self.t_ensaio_2)
        
        self.desl.setGeometry(QtCore.QRect(20, 20, 141, 17))
        self.desl.setObjectName(_fromUtf8("desl"))
        self.deslb = QtWidgets.QDoubleSpinBox(self.t_ensaio_2)
        self.deslb.setGeometry(QtCore.QRect(27, 40, 81, 29))
        self.deslb.setObjectName(_fromUtf8("Vel_ajuste"))
        self.deslb.setRange(8, 175)
        self.deslb.setValue(30)
        self.deslm = QtWidgets.QLabel(self.t_ensaio_2)
        self.deslm.setGeometry(QtCore.QRect(110, 50, 57, 20))
        self.deslm.setObjectName(_fromUtf8("label_12"))
        
        self.Vel_ajuste = QtWidgets.QDoubleSpinBox(self.t_ensaio_2)
        self.Vel_ajuste.setGeometry(QtCore.QRect(27, 90, 81, 29))
        self.Vel_ajuste.setObjectName(_fromUtf8("Vel_ajuste"))
        self.Vel_ajuste.setRange(8, 175)
        self.Vel_ajuste.setValue(120)
        self.label_11 = QtWidgets.QLabel(self.t_ensaio_2)
       
        self.label_11.setGeometry(QtCore.QRect(20, 70, 141, 17))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtWidgets.QLabel(self.t_ensaio_2)
        self.label_12.setGeometry(QtCore.QRect(110, 90, 57, 20))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.pushButton_2 = QtWidgets.QPushButton(self.t_ensaio_2)
        self.pushButton_2.setGeometry(QtCore.QRect(110, 140,  51, 31))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.botaodiretorio = QtWidgets.QPushButton(self.Config_2)
       
        self.botaodiretorio.setGeometry(QtCore.QRect(800, 50, 100, 21))
        self.botaodiretorio.setObjectName(_fromUtf8("pushButton_2"))

        self.botaobrowser = QtWidgets.QPushButton(self.Config_2)
        self.botaobrowser.setGeometry(QtCore.QRect(800, 20, 120, 21))
        self.botaobrowser.setObjectName(_fromUtf8("pushButton_2"))
        
        self.pushButton_3 = QtWidgets.QPushButton(self.t_ensaio_2)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 140, 41, 31))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.parar_ajuste = QtWidgets.QPushButton(self.t_ensaio_2)
        self.parar_ajuste.setGeometry(QtCore.QRect(60, 175, 80, 21))
        self.parar_ajuste.setObjectName(_fromUtf8("parar_ajuste"))
        
        self.raio_tubo = QtWidgets.QFrame(self.Config_2)
        self.raio_tubo.setGeometry(QtCore.QRect(210, 320, 521, 191))
        self.raio_tubo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.raio_tubo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.raio_tubo.setObjectName(_fromUtf8("raio_tubo"))
        self.label_13 = QtWidgets.QLabel(self.raio_tubo)
        
        self.label_13.setGeometry(QtCore.QRect(140, 0, 271, 17))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.checkBox_6 = QtWidgets.QRadioButton(self.raio_tubo)
        self.checkBox_6.setGeometry(QtCore.QRect(40, 30, 111, 22))
        self.checkBox_6.setObjectName(_fromUtf8("checkBox_6"))
        self.checkBox_7 = QtWidgets.QRadioButton(self.raio_tubo)
        self.checkBox_7.setGeometry(QtCore.QRect(40, 80, 101, 22))
        self.checkBox_7.setObjectName(_fromUtf8("checkBox_7"))
        self.checkBox_8 = QtWidgets.QRadioButton(self.raio_tubo)
        self.checkBox_8.setGeometry(QtCore.QRect(40, 130, 101, 22))
        self.checkBox_8.setObjectName(_fromUtf8("checkBox_8"))
       
        self.a_retangulo = QtWidgets.QDoubleSpinBox(self.raio_tubo)
        self.a_retangulo.setGeometry(QtCore.QRect(180, 30, 81, 21))
        self.a_retangulo.setObjectName(_fromUtf8("a_retangulo"))
        self.a_retangulo.setRange(0,1000.00)
        
        self.b_retangulo = QtWidgets.QDoubleSpinBox(self.raio_tubo)
        self.b_retangulo.setGeometry(QtCore.QRect(260, 30, 81, 21))
        self.b_retangulo.setObjectName(_fromUtf8("b_retangulo"))
        self.b_retangulo.setRange(0,1000.00)
        
        self.retanguloima = QtWidgets.QLabel(self.raio_tubo)
            #,posicaoesquerdadireita,posicaoparabaixoaumentar,largura,altura 
        self.retanguloima.setGeometry(QtCore.QRect(350, 10, 120, 60))
        self.retanguloima.setObjectName(_fromUtf8("retangulo"))
        self.pixmap1 = QtGui.QPixmap('Imagens/retangulo1.png')
        self.pixmap1= self.pixmap1.scaledToWidth(60)
        #self.pixmap1= self.pixmap1.scaledToHeight(150)
        self.retanguloima.setPixmap(self.pixmap1)

        self.tuboima = QtWidgets.QLabel(self.raio_tubo)
            #,posicaoesquerdadireita,posicaoparabaixoaumentar,largura,altura 
        self.tuboima.setGeometry(QtCore.QRect(350, 37, 120, 100))
        self.tuboima.setObjectName(_fromUtf8("tubo"))
        self.pixmap2 = QtGui.QPixmap('Imagens/tubo1.png')
        self.pixmap2= self.pixmap2.scaledToWidth(80)
        #self.pixmap1= self.pixmap1.scaledToHeight(150)
        self.tuboima.setPixmap(self.pixmap2)

        self.ciliima = QtWidgets.QLabel(self.raio_tubo) 
            #,posicaoesquerdadireita,posicaoparabaixoaumentar,largura,altura 
        self.ciliima.setGeometry(QtCore.QRect(400, 100, 120, 100))
        self.ciliima.setObjectName(_fromUtf8("tubo"))
        self.pixmap3 = QtGui.QPixmap('Imagens/cilindro.png')
        self.pixmap3= self.pixmap3.scaledToWidth(70)
        #self.pixmap1= self.pixmap1.scaledToHeight(150)
        self.ciliima.setPixmap(self.pixmap3)
        
        
        self.label_15 = QtWidgets.QLabel(self.raio_tubo)
        self.label_15.setGeometry(QtCore.QRect(190, 15, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_15.setFont(font)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_16 = QtWidgets.QLabel(self.raio_tubo)
        self.label_16.setGeometry(QtCore.QRect(280, 10, 61, 31))

        
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_16.setFont(font)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.Velocidade_8 = QtWidgets.QDoubleSpinBox(self.raio_tubo)
        self.Velocidade_8.setGeometry(QtCore.QRect(180, 80, 81, 21))
        self.Velocidade_8.setObjectName(_fromUtf8("Velocidade_8"))
        self.Velocidade_8.setRange(0,1000.00)
        
        self.d_retangulo = QtWidgets.QDoubleSpinBox(self.raio_tubo)
        self.d_retangulo.setGeometry(QtCore.QRect(260, 80, 81, 21))
        self.d_retangulo.setObjectName(_fromUtf8("d_retangulo"))
        self.d_retangulo.setRange(0,1000.00)
        
        self.label_17 = QtWidgets.QLabel(self.raio_tubo)
        self.label_17.setGeometry(QtCore.QRect(190, 66, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_17.setFont(font)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.label_18 = QtWidgets.QLabel(self.raio_tubo)
        self.label_18.setGeometry(QtCore.QRect(280, 70, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_18.setFont(font)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.D_cilimdro = QtWidgets.QDoubleSpinBox(self.raio_tubo)
        self.D_cilimdro.setGeometry(QtCore.QRect(180, 130, 81, 21))
        self.D_cilimdro.setObjectName(_fromUtf8("D_cilimdro"))
        self.D_cilimdro.setRange(0,1000.00)
        
        self.H_cilindro = QtWidgets.QDoubleSpinBox(self.raio_tubo)
        self.H_cilindro.setGeometry(QtCore.QRect(260, 130, 81, 21))
        self.H_cilindro.setObjectName(_fromUtf8("H_cilindro"))
        self.H_cilindro.setRange(0,1000.00)
        
        self.label_19 = QtWidgets.QLabel(self.raio_tubo)
        self.label_19.setGeometry(QtCore.QRect(190, 120, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_19.setFont(font)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.label_20 = QtWidgets.QLabel(self.raio_tubo)
        self.label_20.setGeometry(QtCore.QRect(280, 120, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_20.setFont(font)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        

       
        

        
        self.pushButton_4 = QtWidgets.QPushButton(self.Config_2)
        self.pushButton_4.setGeometry(QtCore.QRect(240, 20, 101, 21))
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))



        self.emergrafic = QtWidgets.QPushButton(self.Grafic)
        self.emergrafic.setGeometry(QtCore.QRect(750, 20, 101, 21))
        self.emergrafic.setSizePolicy(sizePolicy)
        self.emergrafic.setObjectName(_fromUtf8("pushButton_4"))


        
        self.Config.addTab(self.Config_2, _fromUtf8(""))
       


        
        
        

        self.Deslocamento_grafic = QtWidgets.QDoubleSpinBox(self.Grafic)
        self.Deslocamento_grafic.setGeometry(QtCore.QRect(170, 90, 131, 31))
        self.Deslocamento_grafic.setObjectName(_fromUtf8("Deslocamento_grafic"))
        self.Deslocamento_grafic.setRange(0,900)
        self.Forca_grafic = QtWidgets.QDoubleSpinBox(self.Grafic)
        self.Forca_grafic.setGeometry(QtCore.QRect(540, 90, 121, 31))
        self.Forca_grafic.setObjectName(_fromUtf8("Forca_grafic"))
        self.Forca_grafic.setRange(0,10000)
        self.label_21 = QtWidgets.QLabel(self.Grafic)
        self.label_21.setGeometry(QtCore.QRect(180, 70, 111, 17))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.label_22 = QtWidgets.QLabel(self.Grafic)
        self.label_22.setGeometry(QtCore.QRect(570, 70, 111, 17))
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.label_23 = QtWidgets.QLabel(self.Grafic)
        self.label_23.setGeometry(QtCore.QRect(310, 100, 111, 17))
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.label_24 = QtWidgets.QLabel(self.Grafic)
        self.label_24.setGeometry(QtCore.QRect(670, 100, 111, 20))
        self.label_24.setObjectName(_fromUtf8("label_24"))
        
        self.pushButton_5 = QtWidgets.QPushButton(self.Grafic)
        self.pushButton_5.setGeometry(QtCore.QRect(110, 20, 110, 29))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_6 = QtWidgets.QPushButton(self.Grafic)
        self.pushButton_6.setGeometry(QtCore.QRect(560, 20,131 , 29))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_7 = QtWidgets.QPushButton(self.Grafic)
        self.pushButton_7.setGeometry(QtCore.QRect(320, 20, 131, 29))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.Config.addTab(self.Grafic, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        


        self.fig_dict = {}

        
        
        #definiçaõ Celula de Carga
        self.Calibra = QtWidgets.QWidget()
        self.Calibra.setObjectName(_fromUtf8("Celula de Carga"))
        self.obs = QtWidgets.QLabel(self.Calibra)
        self.obs.setGeometry(QtCore.QRect(20,50,841,21))
        self.obs.setObjectName(_fromUtf8("obs"))
        self.bcal = QtWidgets.QPushButton(self.Calibra)
        self.bcal.setGeometry(QtCore.QRect(150,110,131,29))
        self.bcal.setObjectName(_fromUtf8("bcal"))
        
        self.obs3 = QtWidgets.QLabel(self.Calibra)
        
        self.ecal = QtWidgets.QPushButton(self.Calibra)
        self.ecal.setGeometry(QtCore.QRect(530,110,151,29))
        self.ecal.setObjectName(_fromUtf8("ecal"))

        self.scal = QtWidgets.QPushButton(self.Calibra)
        self.scal.setGeometry(QtCore.QRect(330,110,161,29))
        self.scal.setObjectName(_fromUtf8("scal"))
        
        self.combo = QtWidgets.QComboBox(self.Calibra)
        
        
        self.Config.addTab(self.Calibra, _fromUtf8(""))

        self.combo2 = QtWidgets.QComboBox(self.Grafic)
        self.bcombo = QtWidgets.QPushButton(self.Grafic)

        
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 924, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)


        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.Config.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.obs.hide()
        self.combo.hide()
        self.combo2.hide()
        self.scal.hide()
      
        self.bcombo.hide()
        
       

       
        

    def func_browser(self):
        file = QtWidgets.QFileDialog()
        
        self.filedir = file.getOpenFileName()
        #print (self.filedir)
        self.ensaiologin = True
        
    def relatorios(self):

        os.system('rm -rf /home/laboratorio/Desktop/Ensaios')
         
        os.system('cp -R /opt/MET-Master/Ensaios/ /home/laboratorio/Desktop/Ensaios/')
        os.system('chmod 777 /home/laboratorio/Desktop/Ensaios/ -R')    



        os.system("nautilus /home/laboratorio/Desktop/Ensaios/")
        #os.system("exo-open --launch FileManager Ensaios/")
        
    def webcamcapture_final(self):
         global contando
         escolhido = self.combo.currentText()
         
         self.combo.clear()
         cameras = webc.cameralist()
         cameras = cameras[::-1]
         
         self.combo.addItems(cameras)
         #print(self.combo.currentText(),cameras[0])
         imagesavedir = 'TempImagens/'+self.input.text()+str(contando)+'-final.png'
         ind=0
         for i in range(len(cameras)):
              if str(cameras[i]) ==  escolhido:
                   ind = i
          
                   
         webc.main(imagesavedir,cameras[ind])    
    def webcamcapture(self):
         global contando
         escolhido = self.combo.currentText()
         
         self.combo.clear()
         cameras = webc.cameralist()
         cameras = cameras[::-1]
         
         self.combo.addItems(cameras)
         #print(self.combo.currentText(),cameras[0])
         imagesavedir = 'TempImagens/'+self.input.text()+str(contando)+'-inicial.png'
         ind=0
         for i in range(len(cameras)):
              if str(cameras[i]) ==  escolhido:
                   ind = i
          
                   
         webc.main(imagesavedir,cameras[ind])


         
    def retranslateUi(self, MainWindow):

        
        MainWindow.setWindowTitle(_translate("MainWindow", "MET", None))
        self.pushButton.setText(_translate("MainWindow", "Iniciar Ensaio", None))
        self.pushButton.setStyleSheet('color: Blue')
        self.pushButton.clicked.connect(self.iniciar)

        self.button_webcam.setText(_translate("MainWindow", "Imagem capture", None))
        self.button_webcam.clicked.connect(self.webcamcapture)

        
        
        self.bcal.setText(_translate("MainWindow", "Adicionar Nova", None))
        self.bcal.clicked.connect(self.add_nova)
        
        self.scal.setText(_translate("MainWindow", "Selecionar Celula", None))
        self.scal.clicked.connect(self.selecionar)
        
        self.ecal.setText(_translate("MainWindow", "Editar/Calibrar", None))
        self.ecal.clicked.connect(self.Editar)
        
        
        self.label.setText(_translate("MainWindow", "Tipo de ensaio:", None))
        self.checkBox.setText(_translate("MainWindow", "Ensaio de tração", None))
        self.checkBox.setChecked(True) 
        self.checkBox_2.setText(_translate("MainWindow", "Ensaio de compressão", None))
        self.label_2.setText(_translate("MainWindow", "Velocidade de ensaio", None))
        self.label_3.setText(_translate("MainWindow", "mm/min", None))
        
        
        self.checkBox_3.setText(_translate("MainWindow", "Parada queda de Força ",None))
        self.label_4.setText(_translate("MainWindow", "Parada automatica", None))
        self.label_5.setText(_translate("MainWindow", "% de Força", None))
        self.checkBox_4.setText(_translate("MainWindow", "Parada de Força  maxima", None))
        self.label_6.setText(_translate("MainWindow", "Força maxima", None))
        self.checkBox_5.setText(_translate("MainWindow", "Parada deslocamento", None))
        self.label_7.setText(_translate("MainWindow", "Deslocamento Máximo", None))
        self.label_8.setText(_translate("MainWindow", "N", None))
        self.label_9.setText(_translate("MainWindow", "mm", None))
        self.label_10.setText(_translate("MainWindow", "Ajustes Manuais", None))
        self.desl.setText(_translate("MainWindow", "deslocamento", None))
        self.label_11.setText(_translate("MainWindow", "Velocidade do ajuste", None))
        self.label_12.setText(_translate("MainWindow", "mm/min", None))
        self.deslm.setText(_translate("MainWindow", "mm", None))
        
        self.botaodiretorio.setText(_translate("MainWindow", "Relatórios", None))
        self.botaodiretorio.clicked.connect(self.relatorios)
        self.botaodiretorio.show()
        
        self.botaobrowser.setText(_translate("MainWindow", "Browser Ensaio", None))
        self.botaobrowser.clicked.connect(self.func_browser)
        self.botaobrowser.show()
        
        self.pushButton_2.setText(_translate("MainWindow", "Descer", None))
        self.pushButton_2.clicked.connect(self.Descer)
        self.pushButton_3.setText(_translate("MainWindow", "Subir", None))
        self.pushButton_3.clicked.connect(self.Subir)
        self.parar_ajuste.setText(_translate("MainWindow", "Parar", None))
        self.parar_ajuste.clicked.connect(self.Parando2)
        self.label_13.setText(_translate("MainWindow", "Àrea de Seção do Corpo de Prova", None))
        self.checkBox_6.setText(_translate("MainWindow", "Retangular", None))
        self.checkBox_7.setText(_translate("MainWindow", "Tubo", None))
        self.checkBox_8.setText(_translate("MainWindow", "Cilíndrico", None))
        self.label_15.setText(_translate("MainWindow", "L", None))
        self.label_16.setText(_translate("MainWindow", "l", None))
        self.label_17.setText(_translate("MainWindow", "L", None))
        self.label_18.setText(_translate("MainWindow", "D", None))
        self.label_19.setText(_translate("MainWindow", "D", None))
        self.label_20.setText(_translate("MainWindow", "H", None))
        self.pushButton_4.setText(_translate("MainWindow", "Emergência", None))
        self.pushButton_4.setStyleSheet('color: red')
        self.pushButton_4.clicked.connect(self.Parando)


        self.emergrafic.setText(_translate("MainWindow", "Emergência", None))
        self.emergrafic.setStyleSheet('color: red')
        self.emergrafic.clicked.connect(self.Parando) 
        self.Config.setTabText(self.Config.indexOf(self.Config_2), _translate("MainWindow", "Configurações", None))
        self.label_21.setText(_translate("MainWindow", "Deslocamento", None))
        self.label_22.setText(_translate("MainWindow", "Força", None))
        self.label_23.setText(_translate("MainWindow", "mm", None))
        self.label_24.setText(_translate("MainWindow", "N", None))
        self.pushButton_5.setText(_translate("MainWindow", "Reset Gráfico", None))
        self.pushButton_5.clicked.connect(self.resetgrafic)
        
        
        self.pushButton_6.setText(_translate("MainWindow", "Cancelar Test", None))
        self.pushButton_6.clicked.connect(self.cancelartestes)
        self.pushButton_7.setText(_translate("MainWindow", "Gerar Relátorio", None))
        self.pushButton_7.clicked.connect(self.gerarpdf)
        self.Config.setTabText(self.Config.indexOf(self.Grafic), _translate("MainWindow", "Gráfico", None))
        self.Config.setTabText(self.Config.indexOf(self.Calibra), _translate("MainWindow", "Celula de Carga", None))
        self.pushButton_6.hide()
        self.pushButton_7.hide()
        

        
        #Celula de Carga
        self.obs.setText(_translate("MainWindow", "OBS: Retire as Garras/Mordentes da Celula de Carga, Não deixe nada apenas a Celula de Carga, Clique em Iniciar.", None))
        
        
        self.combo.hide()
        self.pushButton_4.setVisible(False)
        self.emergrafic.setVisible(False)
        self.combo.hide()
        #self.label12.hide()





class MyForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def closeEvent(self,event):
        result = QtWidgets.QMessageBox.question(self,
                      "Confirmar Fechamento do Programa...",
                      "Você deseja realmente sair do programa ?",
                      QtWidgets.QMessageBox.Yes| QtWidgets.QMessageBox.No)
        event.ignore()
        if result == QtWidgets.QMessageBox.Yes:
            flag2 =0
            
            Motor.Parar()
            event.accept() 
        

    
    
        

                    

class ServerThread(QtCore.QThread):
    UPsig = QtCore.pyqtSignal(list)
    Stopsig =QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self)

    def start_server(self):
        
        
    
     global flag
     global VelocidadeEn
     global qforca
     global maxforca
     global maxdeslocamento
     global tempinicioteste
     global forcas
     global deslocamentos
     tempo = time.time()
     if(flag == 0):
        
        global flag2
       
        while(flag2 == 1):
                    
         
         
           
            
                    
                    QtTest.QTest.qWait(500)
              
            
        
            
                    
                    
                    flag =1
                    
                    
                    
                   
                    
                    
                    
                    
                       
                        
                        
                        
                    Forca = celula.getvalue()

                    if Forca == None:
                        Forca = 0 
                        pass
                        '''self.aviso= QtWidgets.QMessageBox()
                        self.aviso.setText("Por Favor verifique o HX711, aparentemente o mesmo encontra-se desconnectado !")
        
                        self.aviso.addButton(QtWidgets.QMessageBox.Yes)
                        result1 = self.aviso.exec_()'''
                    else:
                        
                        
                        tempodecorrido = (time.time() - tempinicioteste)/60
                        deslocamento = (float(VelocidadeEn))*float(tempodecorrido)
                        deslocamentos.append(deslocamento)
                        forcas.append((float(Forca)*9.8))
                        forcaanterior = forcas[-1]
                        maiorvalor = forcas.copy()
                        maiorvalor.sort()
                   
                    
                        if( time.time()- tempo > 0.8):
                             
                             lista = [float(deslocamento),float(Forca),float(maiorvalor[-1])+30,float(deslocamentos[-1])+30,deslocamentos,forcas]
                             #self.emit(QtCore.SIGNAL("UP"), lista)
                             self.UPsig.emit(lista)
                             tempo = time.time()


                        
                        
                    if( flag2 == 1 and maxdeslocamento != None and float(maxdeslocamento) != 0 and float(deslocamento) >= float(maxdeslocamento)):
                            
                            
                            flag2 =0
                            
                            #self.emit(QtCore.SIGNAL("Parando"), 1)
                            self.Stopsig.emit(1)
                            
                            
                            lista = [float(deslocamento),float(Forca),maiorvalor[-1]+10,deslocamentos[-1]+10,deslocamentos,forcas]
                            #self.emit(QtCore.SIGNAL("UP"), lista)
                            self.UPsig.emit(lista)
                            
                    if(flag2 == 1 and maxforca != None and float(maxforca) != 0 and float(Forca) >= float(maxforca)):
                            
                            


                                
                            
                            #self.emit(QtCore.SIGNAL("Parando"), 1)
                            self.Stopsig.emit(1)
                            
                            flag2 =0
                            
                            #self.emit(QtCore.SIGNAL("Parando"), 1)
                            self.Stopsig.emit(1)

                            lista = [float(deslocamento),float(Forca),maiorvalor[-1]+10,deslocamentos[-1]+10,deslocamentos,forcas]
                            self.UPsig.emit(lista)
                            #self.emit(QtCore.SIGNAL("UP"), lista)

                    
                    if(flag2 == 1 and  qforca != None and float(qforca) != 0 and   (float(forcaanterior)*(1 - (float(qforca)/100))) > Forca ):
                            
                            flag2 =0
                            for i in range(0,10):
                                    
                                        
                                        QtTest.QTest.qWait(20)

                                        Forca = celula.getvalue()
                            
                                        tempodecorrido = (time.time() - tempinicioteste)/60
                                        deslocamento = (float(VelocidadeEn))*float(tempodecorrido)
                                        deslocamentos.append(deslocamento)
                                        forcas.append((float(Forca)*9.8))
                                        forcaanterior = forcas[-1]
                                        maiorvalor = forcas.copy()
                                        maiorvalor.sort()
                                        
                                    
                                        
                                    
                            #self.emit(QtCore.SIGNAL("Parando"), 1)
                            self.Stopsig.emit(1)
                                    
                            lista = [float(deslocamento),float(Forca),maiorvalor[-1]+10,deslocamentos[-1]+10,deslocamentos,forcas]
                            self.UPsig.emit(lista)
                            #self.emit(QtCore.SIGNAL("UP"), lista)
        

                            
                            
                            
                            
                            
                    flag =0
                    
            
            

    def run(self):
        self.start_server()
            
            

    
               
        

def Area(Retangulo_A,Retangulo_B,Tubo_L,Tubo_D,Cilindro_D,Cilindro_H):
    global AreaCorpoProva
    global FormatoCorpoProva
    FormatoCorpoProva = ""
    AreaCorpoProva = 0.0
    if(Retangulo_A  != None and Retangulo_B != None):
        
        #calcular area
        AreaCorpoProva = float(Retangulo_A) * float(Retangulo_B)
        
       
        

    if(Tubo_L  != None and Tubo_D != None):
        

        AreaCorpoProva = math.pi * float(Tubo_L)* float(Tubo_D)
                                                     
        FormatoCorpoProva = "Tubo"
        
    if(Cilindro_D  != None and Cilindro_H != None):
       
        AreaCorpoProva = (math.pi*((float(Cilindro_D)*float(Cilindro_H))))+ 2*(math.pi*(float(Cilindro_D)*float(Cilindro_D))/4) 
        FormatoCorpoProva = "Cilíndrico"
        


def lotes(nome,x1,x2):
    global contando 
    global testes
    global AreaCorpoProva
    global VelocidadeEn
    global tipodeensaio
    global FormatoCorpoProva
    
    
    testes.append({})
    
    nome=nome+str(contando)                  
    testes[contando]["nome"] = nome
    testes[contando]["area"] = AreaCorpoProva
    testes[contando]["vel"] = VelocidadeEn
    testes[contando]["formato"] = FormatoCorpoProva
    testes[contando]["tipo"] =tipodeensaio
    testes[contando]["cont"] = contando
    testes[contando]["x1"] = x1
    testes[contando]["x2"] = x2
    
    
    
    contando+=1
    
        
if __name__ == "__main__":
    
    
    app =QtWidgets.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    
    
    
    sys.exit(app.exec_())

