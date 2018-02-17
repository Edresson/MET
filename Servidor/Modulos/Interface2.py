# -*- coding: utf-8 -*-
import sys 

from PyQt4 import QtCore, QtGui
import time
from matplotlib.figure import Figure
from  PyQt4 import QtTest
from threading import  Thread
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import threading
import matplotlib.pyplot as plt 


##### imports celula e motor####

#import Motor
from Modulos import celula
from Modulos import Motor
from Modulos import celula


### PDF Imports ###

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm, inch, pica
import os.path
from datetime import datetime
import matplotlib.pyplot as plt
from reportlab.lib.utils import ImageReader
from io import BytesIO
from PIL import Image



from reportlab.pdfbase.pdfmetrics import stringWidth

#variaveis testes em lotes
testes = []
contando = 0
fig = plt.figure()




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
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)






class Ui_MainWindow(object):

    def __init__(self):
        self.result= QtGui.QMessageBox()
        self.result.setText("Você deseja fazer mais um teste nesse lote?")
        
        self.result.addButton(QtGui.QMessageBox.Yes)
        self.result.addButton(QtGui.QMessageBox.No)
        
        

    
        self.u = []
        self.thread3 = ServerThread()
        #self.Thread2 =ThreadGrafic()
        self.Index=0
        self.Index22 =0
        self.text= str()
        self.A = []
        self.Linhas=[]
        #self.runing = 0
        
        self.Grafic = QtGui.QWidget()
        self.Grafic.setObjectName(_fromUtf8("Grafic"))
        
        self.verticalLayoutWidget = QtGui.QWidget(self.Grafic)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 80, 871, 411))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.frame = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.frame.setObjectName(_fromUtf8("verticalLayout_2"))
        self.t=1

        # myFigCanvas = CustomFigCanvas()

        #self.frame.addWidget(myFigCanvas.canvas)
        #self.frame.addWidget(myFigCanvas)
        
        self.fig = Figure(figsize=(5,5), dpi=100)
        self.ax1f1 = self.fig.add_subplot(111,xlabel='Deslocamento(mm)', ylabel='Força(N)', title='')
        self.canvas = FigureCanvas(self.fig)
        self.line1, =self.ax1f1.plot([],[])#forcas)"""
        self.fig.canvas.draw()
        self.ax1f1.grid(True)
        
        #self.line1.set_xdata([100, 50,20])

                    
        #self.line1.set_ydata([1000,500,20])
        #self.ax1f1.set_ylim(0, 1000)
        #aelf.ax1f1.set_xlim(0, 800)
        
        self.canvas = FigureCanvas(self.fig)
        
        self.frame.addWidget(self.canvas)
        
        self.canvas.draw()
        
        self.toolbar = NavigationToolbar(self.canvas, 
                 self.Grafic, coordinates=True)
        
        self.frame.addWidget(self.toolbar)

    

        
        
    
        
        
        
    def selecionar(self):
        self.t = ''
        for i in self.text:
            
            if(i != ';'):
                self.t = self.t + i

            else:
                self.t =''
        #print(self.t)

        self.CALIBRA = open("Fator_Calibracao.txt","w")
        self.CALIBRA.write(self.t)
        self.CALIBRA.close()
        celula.iniciarcel(self.t)
        
        self.obs3.setGeometry(QtCore.QRect(20,190,741,41))
        self.obs3.setText(_translate("MainWindow", "Celula: "+self.text+" Selecionada, Agora a maquina Opera com esta Celula de Carga",None))
        self.obs3.show()
        

        

        

    def combo2_chosen(self, text):
        """
        Handler called when a distro is chosen from the combo box
        """
        #print(text)
        #print("1,1,2,")
        self.Index=self.combo2.currentIndex()
        
       
            
        self.Index22 = str(text)
        #print("valor"+self.Index22)
        #print("2 casa rapaz")

        """
            try:
                #print("1 casa rapaz")
                
                self.Index22 = text
                #print("valor"+str(self.Index22))
            except:
                    #print("fudeu filhão")

        """        
            
        #print(self.Index)
        #self.text = text.replace("                                               Celula de Carga Fator:",";")
        

        
    def combo_chosen(self, text):
        """
        Handler called when a distro is chosen from the combo box
        """
        ##print(text)
        self.Index=self.combo.currentIndex()
        self.text = text.replace("                                               Celula de Carga Fator:",";")
        


        
    def Excluir(self):
        self.combo.removeItem(self.Index)
        #print(self.text)
        ##print("TEXTO "+ self.text2)
        for i, valor in enumerate(self.A):
        #for i in self.A:
            
            if valor == self.text:
                #print("removendo")
                self.A.pop(i)
                #print(self.A)
                self.CALIBRA = open("conf_celulas.txt","w")
                for i in self.A:
                   self.CALIBRA.write(str(i))
                   
                self.CALIBRA.close()
        
        self.obs3.setGeometry(QtCore.QRect(20,190,741,41))
        self.obs3.setText(_translate("MainWindow", "Celula: " +self.text+ " Excluida",None))
        self.obs3.show()




        
    def ecalibrar(self):
        
        #print("Fazendo a divisão |Edt")
        self.bcal.hide()
        self.ecal.hide()
        self.obs3.setText(_translate("MainWindow", "Calibrando Celula de Carga Aguarde ! ",None))
        
        
        VALUE_SERIAL= celula.calibrar()
        B = self.pcal.value()
        Fator= (float(VALUE_SERIAL)/float(B),0)
         
                    
                
        
        
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
                #print(self.A)
                
                self.CALIBRA = open("conf_celulas.txt","w")
                for k in self.A:
                    
                   #print("valor adicionado ao arquivo = %s"%k) 
                   self.CALIBRA.write(k)
                   
                self.CALIBRA.close()
                

    
        # self.bcal2.setText(_translate("MainWindow", "Testar a Celula de Carga ",None))
        #self.bcal2.clicked.connect(self.salvar)
        self.bcal2.hide()
        self.obs3.setText(_translate("MainWindow", "Celula de Carga Calibrada agora você já pode Colocar novamente as Garras/Mordentes\n Celula: "+self.t,None))
        #self.obs4.hide()
        self.bcal.show()
        self.ecal.show()
        
        self.pcal.hide()
        
        
        
        
        
    def editCalibra(self):
        #print("iniciando Celula de Carga EDT")
        self.bcal2.hide()
        self.obs3.hide()

        celula.tare()
        
        self.pcal = QtGui.QDoubleSpinBox(self.Calibra)
        self.obs3 = QtGui.QLabel(self.Calibra)
        #print(celula.getvalue())
        
        self.bcal2 = QtGui.QPushButton(self.Calibra)
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
        self.bcal2 = QtGui.QPushButton(self.Calibra)
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

        #print("add NOVA")
        self.combo.hide()
        self.obs3.hide()
        self.bcal2 = QtGui.QPushButton(self.Calibra)
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
        self.ccal = QtGui.QPushButton(self.Calibra)
        self.ccal.setGeometry(QtCore.QRect(150,110,131,29))
        self.ccal.setObjectName(_fromUtf8("bcal"))

        self.dcal = QtGui.QPushButton(self.Calibra)
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
        #self.combo.show()
        self.combo.connect(self.combo, QtCore.SIGNAL('activated(QString)'), self.combo_chosen)
        
        
        self.CALIBRA.close()
        
        
        


        
    def resetgrafic(self):
        #print("resetando")
        deslocamentos= [0]
        forcas= [0]
        self.PlotGrafico()
        
    def PlotGrafico(self):
        #print("Atualizando Grafico")
        
        
       
        self.line1.set_data(deslocamentos, forcas)
        #self.line1.set_ydata(forcas)
        
        #self.line1.set_xdata(deslocamentos)
        self.fig.canvas.draw()
        
        
        
    def zeraf(self):
        
        self.Forca_grafic.setValue(0.00)
    
    def zerades(self):
        self.Deslocamento_grafic.setValue(0.00)
        
    def Subir(self):
        Motor.Parar()
        self.pushButton_2.setVisible(True)
        self.pushButton_3.setVisible(True)
        
        self.parar_ajuste.setVisible(True)
        
        Motor.Subir_descer(self.Vel_ajuste.value(),1,self.deslb.value())

    def Descer(self):
        Motor.Parar()
        self.pushButton_2.setVisible(True)
        self.pushButton_3.setVisible(True)
        self.parar_ajuste.setVisible(True)
        Motor.Subir_descer(self.Vel_ajuste.value(),2,self.deslb.value())

    def Parando(self):
        #print("chamou ja a função do parar ")
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
        
        
        #print("chamou ja a função do parar ( emergencia)")
        #self.runing = 0
        #self.label12.hide()
        self.pushButton.setVisible(True)
        self.pushButton_4.setVisible(False)
        self.emergrafic.setVisible(False)
        Motor.Parar()




        #parte para todas as paradas


        self.confirmar_continuacao()
        

    def confirmar_continuacao(self):
        
       
        #.,self.close()
        
        result1 = self.result.exec_()
        if result1 == QtGui.QMessageBox.Yes:
            #print("yes")
            self.Config.setCurrentWidget(self.Config)
            lotes(self.input.text(),deslocamentos,forcas)
            self.Config.setCurrentWidget(self.Config_2)
            #flag2 =0
            
            
            #Programa.comport.close()
        if result1 == QtGui.QMessageBox.No:
            self.inputl.show()
            self.input.show()
            
            lotes(self.input.text(),deslocamentos,forcas,)
            self.ax1f1.cla()
            self.ax1f1.grid(True)
            self.pushButton.hide()
            #print("No")
            #print(len(testes))
            if(len(testes) > 0):
                 pass
                 #print("ok")
            self.Linhas = []
            
            self.combo2.setGeometry(QtCore.QRect(90,20,192,30))
            self.combo2.setObjectName(_fromUtf8("p2cal"))
            self.combo2.show()
            #self.pushButton_5.hide()
            
            self.bcombo.setGeometry(QtCore.QRect(90,50,41, 31))
            self.bcombo.setText(_translate("MainWindow", "Excluir", None))
            self.bcombo.clicked.connect(self.excluirlinha_grafic)
            self.bcombo.setObjectName(_fromUtf8("p2cal"))
            self.bcombo.show()
           
        
            for i in range(0,len(testes)):
                           
                           
                self.u.append(testes[i]["nome"])
                #print(list(testes[i]["x1"]))
                #print(list(testes[i]["x1"]))
                
                self.aux, = self.ax1f1.plot(list(testes[i]["x1"]),list(testes[i]["x2"]),label='${i}$'.format(i=str(testes[i]["nome"])))
                self.Linhas.append(self.aux)
                self.ax1f1.legend(loc ='best') 
                self.fig.canvas.draw()
        
            self.combo2.addItems(self.u)
            #self.combo.show() 
            #self.combo.connect(self.combo, QtCore.SIGNAL('activated(QString)'), self.combo_chosen)
            self.combo2.connect(self.combo2, QtCore.SIGNAL('activated(QString)'), self.combo2_chosen)
            contando = 0
            self.pushButton_6.show()
            self.pushButton_7.show()
            
        
        

            

            
            pass



        
    def returnposteste(self,index):
        global testes
        #print('index:'+str(index))
        for i in range(0,len(testes)):
            #print('teste:'+str(testes[i]["nome"]))
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
        #self.line1.set_data([],[])
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
          #print ("Criado com sucesso dir ano!")
     


            


        if os.path.isdir("Ensaios/"+str(now.year)+"/"+str(now.month)): # vemos de este diretorio já existe
             pass
        else:
          os.mkdir("Ensaios/"+str(now.year)+"/"+str(now.month)) # aqui criamos o diretorio
          #print ("Criado com sucesso dir mes!")


        if os.path.isdir("Ensaios/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day)): # vemos de este diretorio já existe
             pass
        else:
          os.mkdir("Ensaios/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day)) # aqui criamos o diretorio
          #print ("Criado com sucesso dir day!")
          
        #print("Todos os diretorios criados iniciando a construção do pdf")
        Forcamaxima = forcas[-1]
        maxdeslocamento = deslocamentos[-1]
        Posicaomaxima = deslocamentos[-1]

        pdf2 = Canvas("Ensaios/"+"Ensaio_Atual.pdf", pagesize = letter) #Nome do arquivo e Tipo do papel
        #print("1")
        pdf = Canvas("Ensaios/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day)+"/"+str(self.input.text())+"Hora:"+str(now.hour)+"-"+str(now.minute)+ "-"+ str(now.second)+".pdf", pagesize = letter) #Nome do arquivo e Tipo do papel
        #print("2")

        pdf.setFont('Helvetica-Bold', 12)
        #print("3")
        pdf2.setFont('Helvetica-Bold', 12)
        #print("4")
        tupla = ('                                      Máquina de Ensaio de Tração e Compressão', '','','','','','','','', '                                                       Ensaio','', 'N° da Solicitação: _________', 'Solicitante/Setor: __________________________________','Inspetor: ___________________________________','Responsável: ___________________________________','' ,
                 'Data: ' + str(now.day)+'/'+str(now.month)+'/'+str(now.year),  'Hora: ' + str(now.hour)+":"+str(now.minute)+ ":"+ str(now.second) ,'', '', '','' ,'')
        #print("5")
        lista = pdf.beginText(inch * 1, inch * 10)
        #print("6")

        lista2 = pdf2.beginText(inch * 1, inch * 10)
        #print("7")

        
        for i in range(0,len(tupla)):
            lista.textLine(tupla[i])
            lista2.textLine(tupla[i])






        
        
        #print("9")
        ax = fig.add_subplot(111,xlabel='Deslocamento(mm)', ylabel='Força(N)', title='')
        #print("10")
        #ax.set_ylim(0, forcas[-1]+10)

        #print("11")
        ax.grid(True)
        #print("12")
        #ax.set_xlim(0, deslocamentos[-1]+10)
        #print("13")
        for i in range(0,len(testes)):
                           
                
                ax.plot(list(testes[i]["x1"]),list(testes[i]["x2"]),label='${i}$'.format(i=str(testes[i]["nome"])))
                ax.legend(loc ='best') 
                
                
        #ax.plot(deslocamentos,forcas)

        #print("antes do grafico PDF")
        imgdata = BytesIO()
        fig.savefig(imgdata, format='png')
        imgdata.seek(0)  # rewind the data

        Image = ImageReader(imgdata)
        
        pdf2.drawText(lista2)
        pdf.drawText(lista)

        pdf2.drawImage(Image ,130,50, width=400,height=350)

        pdf.drawImage(Image ,130,50, width=400,height=350)
        #pdf.drawText(lista)
        pdf2.showPage()
        pdf.showPage()
        
        
        
        for j in range(0,len(testes)):
            #print("len testes : "+str(len(testes)))
            
        
            
            
            
            
            ax2= fig.add_subplot(111,xlabel='Deslocamento(mm)', ylabel='Força(N)', title='')
            ax2.cla()
            ax2.grid(True)
            ax2.plot(list(testes[j]["x1"]),list(testes[j]["x2"]))
            X = list(testes[j]["x1"]).copy()
            Y = list(testes[j]["x2"]).copy()
            #print("X"+str(X))
            #print("Y"+str(Y))
            X.sort()
            Y.sort()
            xmax = X[-1]
            ymax = Y[-1]
            ##print("xmax"+xmax)
            ##print("ymax"+ymax)
            ##print(X,Y)
            
            
            tupla = ( '','','','','                                                 Nome Ensaio: '+str(testes[j]["nome"]),'','Tipo de ensaio: '+str(testes[j]["tipo"]) ,
                 'Formato do corpo de prova: '+str(testes[j]["formato"] ),
                 'Posição Máxima: '+str( xmax )+" mm",'Força Máxima: '+str(ymax)+'N', 'Área do corpo de prova: '+str(testes[j]["area"])+' mm²', 'Velocidadede ensaio: '+str(testes[j]["vel"])+' mm/min','Comprimento do corpo de prova: __________ mm' ,)
           
            lista3 = pdf.beginText(inch * 1, inch * 10)
           

            lista4 = pdf2.beginText(inch * 1, inch * 10)
            #print("7")

            
            for i in range(0,len(tupla)):
                lista3.textLine(tupla[i])
                lista4.textLine(tupla[i])

                      
            pdf.drawText(lista3)
            #print("j é : "+str(j))
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

        
        #pdf2.showPage()
        #pdf.showPage() 
        pdf2.save()
        self.cancelartestes()
        
        


        

        
        pdf.save()


        x = [0]
        y = [0]
        
        #print("PDF SAlVO")
        

        
        
    def excluirlinha_grafic(self):
        global testes
        self.line1.set_data([],[])
        
        self.combo2.removeItem(self.Index)
        try:
            self.idx = int(self.returnposteste(self.Index22))
        except:
            pass
        self.Linhas[self.idx].set_data([], [])
        testes.pop(self.idx)
        self.ax1f1.cla()
        self.Linhas = [] 
        for i in range(0,len(testes)):
                           
                           
                self.u.append(testes[i]["nome"])
                
                
                self.aux, = self.ax1f1.plot(list(testes[i]["x1"]),list(testes[i]["x2"]),label='${i}$'.format(i=str(testes[i]["nome"])))
                self.Linhas.append(self.aux)
                
        self.ax1f1.legend(loc ='best') 
        #self.fig.canvas.draw()
        self.ax1f1.grid(True)  
        #self.ax1f1.legend_.remove()
        #self.ax1f1.legend()
        #testes[i]["nome"]
        self.fig.canvas.draw_idle()


        
    def Parando3(self,i = None):
        global flag2
        global flag
        flag = 0
        flag2 =0
        
        self.pushButton_2.setVisible(True)
        self.pushButton_3.setVisible(True)
        self.parar_ajuste.setVisible(False)
        #print("chamou ja a função do parar 3 ")
        #self.runing = 0
        #self.label12.hide()
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
        
        #print("aquii222222")
        Motor.Parar()
        self.confirmar_continuacao()
        
    
    def Parando2(self):
        #print("chamou ja a função do parar 2 ")
        global flag2
        flag2 =0
        self.pushButton_2.setVisible(True)
        self.pushButton_3.setVisible(True)
        self.parar_ajuste.setVisible(False)
        Motor.Parar()
        #self.confirmar_continuacao()

        
    def iniciar(self):
        self.Config.setCurrentWidget(self.Grafic)
        global deslocamentos
        global forcas
        global testes
        self.inputl.hide()
        self.input.hide()
        
        arquivo = open("Fator_Calibracao.txt","r")
        fator = arquivo.readline()
        celula.iniciarcel(str(fator))
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
        #self.runing = 1
        #self.label12.setText(_translate("MainWindow", "Ensaio em Progresso", None))
        #self.label12.setGeometry(QtCore.QRect(40, 20, 151, 21))
        #self.label12.show()      
        
        if(self.checkBox.isChecked() == True):
            
            Motor.subir()
            tipodeensaio = "Tração"
        else:
            tipodeensaio = "Compressão"
            
            Motor.baixar()
            
        VelocidadeEn = self.Velocidade.value()    
        Motor.calcular( float(VelocidadeEn) )   
        
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
            
        # Programa.Parada(a,b,c)

       
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
        #time.sleep(1)

        
        self.thread3.start()
        #self.Thread2.start()
       
        QtGui.QWidget.connect(self.thread3, QtCore.SIGNAL("UP"), self.update1)
        QtGui.QWidget.connect(self.thread3, QtCore.SIGNAL("Parando"), self.Parando3)
        
        
    def update1(self,lista):
        
                        
                        
                        self.Deslocamento_grafic.setValue(lista[0])
                        self.Forca_grafic.setValue(float(lista[1])*9.8)
                        self.ax1f1.set_ylim(0, lista[2])
                        self.ax1f1.set_xlim(0, lista[3])
                        self.line1.set_data(lista[4],lista[5])
                        self.fig.canvas.draw_idle()
                        
                        
            
    def calibrar(self):
        
        celula.tare()
        #print("iniciando Celula de Carga")
        self.bcal2.hide()
        self.obs3.hide()
        self.pcal = QtGui.QDoubleSpinBox(self.Calibra)
        self.obs3 = QtGui.QLabel(self.Calibra)
        self.obs4 = QtGui.QLabel(self.Calibra)
        self.qline = QtGui.QLineEdit(self.Calibra)
        self.bcal2 = QtGui.QPushButton(self.Calibra)
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
        
        
        

            
        #VALUE_SERIAL = Programa.SolicitarDados()
        
        B = self.pcal.value()
        Fator= (float(VALUE_SERIAL)/float(B))
        
        #print("Fazendo a divisão")
        
        A = self.qline.text()
        
        self.CALIBRA = open("conf_celulas.txt","r")
        self.A = self.CALIBRA.readlines()
        
        self.CALIBRA.close()
        self.t= ''
        self.C = []
        self.posicao = 0
        for i, valor in enumerate(self.A):
        #for i in self.A:
                 
                
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
        
            
        
        # self.bcal2.setText(_translate("MainWindow", "Testar a Celula de Carga ",None))
        #self.bcal2.clicked.connect(self.salvar)
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
            
       

        
        
        
    
        



    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(924, 599)
        MainWindow.setMinimumSize(924, 599)
        MainWindow.setMaximumSize(924, 599)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.Config = QtGui.QTabWidget(self.centralwidget)
        self.Config.setGeometry(QtCore.QRect(0, 0, 961, 581))
        self.Config.setObjectName(_fromUtf8("Config"))
        self.Config_2 = QtGui.QWidget()
        self.Config_2.setObjectName(_fromUtf8("Config_2"))

        self.input = QtGui.QLineEdit(self.Config_2)
        #self.input = QtGui.QPushButton(self.Config_2)
        self.input.setGeometry(QtCore.QRect(600, 20, 151, 21))
        self.input.setObjectName(_fromUtf8("input"))
        
        self.inputl = QtGui.QLabel(self.Config_2)
        self.inputl.setGeometry(QtCore.QRect(500, 20, 151, 21))
        self.inputl.setObjectName(_fromUtf8("inputl"))
        self.inputl.setText(_translate("MainWindow", "Nome do Lote:",None))
        self.inputl.show()

        
        self.pushButton = QtGui.QPushButton(self.Config_2)
        self.pushButton.setGeometry(QtCore.QRect(40, 20, 151, 21))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.t_ensaio = QtGui.QFrame(self.Config_2)
        self.t_ensaio.setGeometry(QtCore.QRect(50, 90, 201, 201))
        self.t_ensaio.setFrameShape(QtGui.QFrame.StyledPanel)
        self.t_ensaio.setFrameShadow(QtGui.QFrame.Raised)
        self.t_ensaio.setObjectName(_fromUtf8("t_ensaio"))
        
        """self.label12 = QtGui.QLabel(self.Config_2)
        self.label12.setGeometry(QtCore.QRect(40, 20, 151, 21))
        self.label12.setObjectName(_fromUtf8("label"))"""
        

        
        self.label = QtGui.QLabel(self.t_ensaio)
        self.label.setGeometry(QtCore.QRect(50, 0, 101, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.checkBox = QtGui.QRadioButton(self.t_ensaio)
        self.checkBox.setGeometry(QtCore.QRect(20, 50, 151, 22))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox_2 = QtGui.QRadioButton(self.t_ensaio)
        self.checkBox_2.setGeometry(QtCore.QRect(20, 90, 161, 22))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.Velocidade = QtGui.QDoubleSpinBox(self.t_ensaio)
        self.Velocidade.setGeometry(QtCore.QRect(27, 160,81, 29))
        self.Velocidade.setObjectName(_fromUtf8("Velocidade"))
        self.Velocidade.setRange(8, 175 )
        self.Velocidade.setValue(10)
        
        self.label_2 = QtGui.QLabel(self.t_ensaio)
        self.label_2.setGeometry(QtCore.QRect(40, 130, 141, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.t_ensaio)
        self.label_3.setGeometry(QtCore.QRect(120, 170, 57, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.frame_2 = QtGui.QFrame(self.Config_2)
        self.frame_2.setGeometry(QtCore.QRect(270, 90, 361, 201))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.checkBox_3 = QtGui.QCheckBox(self.frame_2)
        self.checkBox_3.setGeometry(QtCore.QRect(30, 50, 161, 22))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))

        self.label_4 = QtGui.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(120, 0, 111, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.Velocidade_2 = QtGui.QDoubleSpinBox(self.frame_2)
        self.Velocidade_2.setGeometry(QtCore.QRect(200, 50, 81, 21))
        self.Velocidade_2.setObjectName(_fromUtf8("Velocidade_2"))
        self.Velocidade_2.setRange(0,99.00)
        self.Velocidade_2.setValue(99.00)
        #self.checkBox_3.setChecked(True)
        self.label_5 = QtGui.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(210, 40, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.checkBox_4 = QtGui.QCheckBox(self.frame_2)
        self.checkBox_4.setGeometry(QtCore.QRect(30, 100, 161, 22))
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.Velocidade_3 = QtGui.QDoubleSpinBox(self.frame_2)
        self.Velocidade_3.setGeometry(QtCore.QRect(200, 100, 81, 21))
        self.Velocidade_3.setObjectName(_fromUtf8("Velocidade_3"))
        self.Velocidade_3.setRange(0,10000.00)
        #self.pcal.setValue(1.00)
        self.label_6 = QtGui.QLabel(self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(210, 80, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.checkBox_5 = QtGui.QCheckBox(self.frame_2)
        self.checkBox_5.setGeometry(QtCore.QRect(30, 150, 161, 22))
        self.checkBox_5.setObjectName(_fromUtf8("checkBox_5"))
        self.Velocidade_4 = QtGui.QDoubleSpinBox(self.frame_2)
        self.Velocidade_4.setGeometry(QtCore.QRect(200, 150, 81, 21))
        self.Velocidade_4.setObjectName(_fromUtf8("Velocidade_4"))
        self.Velocidade_4.setRange(0,5000.00)
        self.label_7 = QtGui.QLabel(self.frame_2)
        self.label_7.setGeometry(QtCore.QRect(190, 130, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(280, 100, 57, 20))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.frame_2)
        self.label_9.setGeometry(QtCore.QRect(280, 160, 57, 20))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.t_ensaio_2 = QtGui.QFrame(self.Config_2)
        self.t_ensaio_2.setGeometry(QtCore.QRect(660, 90, 201, 201))
        self.t_ensaio_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.t_ensaio_2.setFrameShadow(QtGui.QFrame.Raised)
        self.t_ensaio_2.setObjectName(_fromUtf8("t_ensaio_2"))
        self.label_10 = QtGui.QLabel(self.t_ensaio_2)
        
        self.label_10.setGeometry(QtCore.QRect(40, 0, 101, 17))
        self.label_10.setObjectName(_fromUtf8("label_10"))

        self.desl = QtGui.QLabel(self.t_ensaio_2)
        
        self.desl.setGeometry(QtCore.QRect(20, 20, 141, 17))
        self.desl.setObjectName(_fromUtf8("desl"))
        self.deslb = QtGui.QDoubleSpinBox(self.t_ensaio_2)
        self.deslb.setGeometry(QtCore.QRect(27, 40, 81, 29))
        self.deslb.setObjectName(_fromUtf8("Vel_ajuste"))
        self.deslb.setRange(8, 175)
        self.deslb.setValue(30)
        self.deslm = QtGui.QLabel(self.t_ensaio_2)
        self.deslm.setGeometry(QtCore.QRect(110, 50, 57, 20))
        self.deslm.setObjectName(_fromUtf8("label_12"))
        
        self.Vel_ajuste = QtGui.QDoubleSpinBox(self.t_ensaio_2)
        self.Vel_ajuste.setGeometry(QtCore.QRect(27, 90, 81, 29))
        self.Vel_ajuste.setObjectName(_fromUtf8("Vel_ajuste"))
        self.Vel_ajuste.setRange(8, 175)
        self.Vel_ajuste.setValue(175)
        self.label_11 = QtGui.QLabel(self.t_ensaio_2)
        #1 posição lado direito
        # 2 baixo
        #
        self.label_11.setGeometry(QtCore.QRect(20, 70, 141, 17))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtGui.QLabel(self.t_ensaio_2)
        self.label_12.setGeometry(QtCore.QRect(110, 90, 57, 20))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.pushButton_2 = QtGui.QPushButton(self.t_ensaio_2)
        self.pushButton_2.setGeometry(QtCore.QRect(110, 140,  51, 31))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.t_ensaio_2)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 140, 41, 31))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.parar_ajuste = QtGui.QPushButton(self.t_ensaio_2)
        self.parar_ajuste.setGeometry(QtCore.QRect(60, 175, 80, 21))
        self.parar_ajuste.setObjectName(_fromUtf8("parar_ajuste"))
        
        self.raio_tubo = QtGui.QFrame(self.Config_2)
        self.raio_tubo.setGeometry(QtCore.QRect(210, 320, 521, 191))
        self.raio_tubo.setFrameShape(QtGui.QFrame.StyledPanel)
        self.raio_tubo.setFrameShadow(QtGui.QFrame.Raised)
        self.raio_tubo.setObjectName(_fromUtf8("raio_tubo"))
        self.label_13 = QtGui.QLabel(self.raio_tubo)
        self.label_13.setGeometry(QtCore.QRect(140, 0, 271, 17))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.checkBox_6 = QtGui.QRadioButton(self.raio_tubo)
        self.checkBox_6.setGeometry(QtCore.QRect(40, 30, 111, 22))
        self.checkBox_6.setObjectName(_fromUtf8("checkBox_6"))
        self.checkBox_7 = QtGui.QRadioButton(self.raio_tubo)
        self.checkBox_7.setGeometry(QtCore.QRect(40, 80, 101, 22))
        self.checkBox_7.setObjectName(_fromUtf8("checkBox_7"))
        self.checkBox_8 = QtGui.QRadioButton(self.raio_tubo)
        self.checkBox_8.setGeometry(QtCore.QRect(40, 130, 101, 22))
        self.checkBox_8.setObjectName(_fromUtf8("checkBox_8"))
       
        self.a_retangulo = QtGui.QDoubleSpinBox(self.raio_tubo)
        self.a_retangulo.setGeometry(QtCore.QRect(180, 30, 81, 21))
        self.a_retangulo.setObjectName(_fromUtf8("a_retangulo"))
        self.a_retangulo.setRange(0,1000.00)
        #self.pcal.setValue(1.00)
        self.b_retangulo = QtGui.QDoubleSpinBox(self.raio_tubo)
        self.b_retangulo.setGeometry(QtCore.QRect(260, 30, 81, 21))
        self.b_retangulo.setObjectName(_fromUtf8("b_retangulo"))
        self.b_retangulo.setRange(0,1000.00)
        #self.pcal.setValue(1.00)
        self.label_15 = QtGui.QLabel(self.raio_tubo)
        self.label_15.setGeometry(QtCore.QRect(190, 15, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_15.setFont(font)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_16 = QtGui.QLabel(self.raio_tubo)
        self.label_16.setGeometry(QtCore.QRect(280, 10, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_16.setFont(font)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.Velocidade_8 = QtGui.QDoubleSpinBox(self.raio_tubo)
        self.Velocidade_8.setGeometry(QtCore.QRect(180, 80, 81, 21))
        self.Velocidade_8.setObjectName(_fromUtf8("Velocidade_8"))
        self.Velocidade_8.setRange(0,1000.00)
        #self.pcal.setValue(1.00)
        self.d_retangulo = QtGui.QDoubleSpinBox(self.raio_tubo)
        self.d_retangulo.setGeometry(QtCore.QRect(260, 80, 81, 21))
        self.d_retangulo.setObjectName(_fromUtf8("d_retangulo"))
        self.d_retangulo.setRange(0,1000.00)
        #self.pcal.setValue(1.00)
        self.label_17 = QtGui.QLabel(self.raio_tubo)
        self.label_17.setGeometry(QtCore.QRect(190, 66, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_17.setFont(font)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.label_18 = QtGui.QLabel(self.raio_tubo)
        self.label_18.setGeometry(QtCore.QRect(280, 70, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_18.setFont(font)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.D_cilimdro = QtGui.QDoubleSpinBox(self.raio_tubo)
        self.D_cilimdro.setGeometry(QtCore.QRect(180, 130, 81, 21))
        self.D_cilimdro.setObjectName(_fromUtf8("D_cilimdro"))
        self.D_cilimdro.setRange(0,1000.00)
        #self.pcal.setValue(1.00)
        self.H_cilindro = QtGui.QDoubleSpinBox(self.raio_tubo)
        self.H_cilindro.setGeometry(QtCore.QRect(260, 130, 81, 21))
        self.H_cilindro.setObjectName(_fromUtf8("H_cilindro"))
        self.H_cilindro.setRange(0,1000.00)
        #self.pcal.setValue(1.00)
        self.label_19 = QtGui.QLabel(self.raio_tubo)
        self.label_19.setGeometry(QtCore.QRect(190, 120, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_19.setFont(font)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.label_20 = QtGui.QLabel(self.raio_tubo)
        self.label_20.setGeometry(QtCore.QRect(280, 120, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_20.setFont(font)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        

       
        

        
        self.pushButton_4 = QtGui.QPushButton(self.Config_2)
        self.pushButton_4.setGeometry(QtCore.QRect(240, 20, 101, 21))
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))



        self.emergrafic = QtGui.QPushButton(self.Grafic)
        self.emergrafic.setGeometry(QtCore.QRect(750, 20, 101, 21))
        self.emergrafic.setSizePolicy(sizePolicy)
        self.emergrafic.setObjectName(_fromUtf8("pushButton_4"))


        
        self.Config.addTab(self.Config_2, _fromUtf8(""))
       


        
        
        """self.frame = QtGui.QVBoxLayout(self.Grafic)#QtGui.QFrame
        self.frame.setGeometry(QtCore.QRect(30, 150, 841, 381))
        #self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        #self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))"""

        self.Deslocamento_grafic = QtGui.QDoubleSpinBox(self.Grafic)
        self.Deslocamento_grafic.setGeometry(QtCore.QRect(170, 90, 131, 31))
        self.Deslocamento_grafic.setObjectName(_fromUtf8("Deslocamento_grafic"))
        self.Deslocamento_grafic.setRange(0,900)
        self.Forca_grafic = QtGui.QDoubleSpinBox(self.Grafic)
        self.Forca_grafic.setGeometry(QtCore.QRect(540, 90, 121, 31))
        self.Forca_grafic.setObjectName(_fromUtf8("Forca_grafic"))
        self.Forca_grafic.setRange(0,10000)
        self.label_21 = QtGui.QLabel(self.Grafic)
        self.label_21.setGeometry(QtCore.QRect(180, 70, 111, 17))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.label_22 = QtGui.QLabel(self.Grafic)
        self.label_22.setGeometry(QtCore.QRect(570, 70, 111, 17))
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.label_23 = QtGui.QLabel(self.Grafic)
        self.label_23.setGeometry(QtCore.QRect(310, 100, 111, 17))
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.label_24 = QtGui.QLabel(self.Grafic)
        self.label_24.setGeometry(QtCore.QRect(670, 100, 111, 20))
        self.label_24.setObjectName(_fromUtf8("label_24"))
        
        self.pushButton_5 = QtGui.QPushButton(self.Grafic)
        self.pushButton_5.setGeometry(QtCore.QRect(110, 20, 87, 29))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_6 = QtGui.QPushButton(self.Grafic)
        self.pushButton_6.setGeometry(QtCore.QRect(560, 20, 87, 29))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_7 = QtGui.QPushButton(self.Grafic)
        self.pushButton_7.setGeometry(QtCore.QRect(320, 20, 131, 29))
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.Config.addTab(self.Grafic, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        # grafico confgs


        self.fig_dict = {}

        #fig = Figure()
        # self.addmpl(fig)
        """fig1 = Figure()
        ax1f1 = fig1.add_subplot(111)
        ax1f1.plot([5,6,7,8],[0,5,7,1])
        self.addmpl(fig1)"""
        
        #definiçaõ Celula de Carga
        self.Calibra = QtGui.QWidget()
        self.Calibra.setObjectName(_fromUtf8("Celula de Carga"))
        self.obs = QtGui.QLabel(self.Calibra)
        self.obs.setGeometry(QtCore.QRect(20,50,841,21))
        self.obs.setObjectName(_fromUtf8("obs"))
        self.bcal = QtGui.QPushButton(self.Calibra)
        self.bcal.setGeometry(QtCore.QRect(150,110,131,29))
        self.bcal.setObjectName(_fromUtf8("bcal"))
        
        self.obs3 = QtGui.QLabel(self.Calibra)
        
        self.ecal = QtGui.QPushButton(self.Calibra)
        self.ecal.setGeometry(QtCore.QRect(530,110,151,29))
        self.ecal.setObjectName(_fromUtf8("ecal"))

        self.scal = QtGui.QPushButton(self.Calibra)
        self.scal.setGeometry(QtCore.QRect(330,110,161,29))
        self.scal.setObjectName(_fromUtf8("scal"))
        
        self.combo = QtGui.QComboBox(self.Calibra)
        
        
        self.Config.addTab(self.Calibra, _fromUtf8(""))

        self.combo2 = QtGui.QComboBox(self.Grafic)
        self.bcombo = QtGui.QPushButton(self.Grafic)

        
        
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 924, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)


        self.statusbar = QtGui.QStatusBar(MainWindow)
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
        #self.input.hide()
        
       

       
        

        

        
    def retranslateUi(self, MainWindow):

        
        MainWindow.setWindowTitle(_translate("MainWindow", "MET", None))
        self.pushButton.setText(_translate("MainWindow", "Iniciar Ensaio", None))
        self.pushButton.setStyleSheet('color: Blue')
        self.pushButton.clicked.connect(self.iniciar)
        
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
        #self.checkBox_3.clicked.connect( self.check3)
        
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
        self.label_15.setText(_translate("MainWindow", "A", None))
        self.label_16.setText(_translate("MainWindow", "B", None))
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

    """def UpdateGrafic(self):
        global flag2
        
        while(flag2 == 1):
            
         # #print(Programa.flag2)
         
         
          
          if(flag == 0):
            
            time.sleep(1)
            
        
            if(#self.runing == 1):
                    global flag
                    global qforca
                    global maxforca
                    global maxdeslocamento
                    flag =1
                    #print("flag1")
                    
                    
                    
                    Programa.comport.write(b'd')#enviando a letra d para o arduino mandar  os dados
                    VALUE_SERIAL=Programa.comport.readline()
                    #VALUE_SERIAL = Programa.SolicitarDados()
                    #print(VALUE_SERIAL)
                    VALUE_SERIAL=str(VALUE_SERIAL)
                    
                    VALUE_SERIAL= VALUE_SERIAL.replace("\\r\\n'",'')
                    VALUE_SERIAL= VALUE_SERIAL.replace("b'",'')
                    
                    if(VALUE_SERIAL == 't'):
                        #self.runing =0
                        Programa.CriarPDF()
                        flag =0
                        #print("flag0 (leu)")
                        #print("recebeu t")
                        return 0
                    
                    if(VALUE_SERIAL[0] == 'd'):
                        VALUE_SERIAL= VALUE_SERIAL.replace("d:",'')
                        #print(VALUE_SERIAL)
                    
                        A,B=VALUE_SERIAL.split(';')
                        
                        forcaanterior = forcas[-1]
                        Programa.Updatexy(A,B)
                        self.Deslocamento_grafic.setValue(float(deslocamento))
                        self.Forca_grafic.setValue(float(Forca))
                        
                        self.ax1f1.set_ylim(0, forcas[-1]+10)
                        self.ax1f1.set_xlim(0, deslocamentos[-1]+10)
                        self.line1.set_data(deslocamentos,forcas)
                        self.fig.canvas.draw()
                        
                        if(maxdeslocamento != None and float(maxdeslocamento) != 0 and float(deslocamento) >= float(maxdeslocamento)):
                            #print("entrou Maxdeslocamento alcançado ")
                            
                            #self.runing =0
                            #Programa.CriarPDF()
                            self.emit(QtCore.SIGNAL("Parando"), 1)
                            flag =0
                            #print("Terminou Maxdeslocamento alcançado ")
                            
                            
                        if(maxforca != None and float(maxforca) != 0 and float(Forca) >= float(maxforca)):
                            #self.runing =0
                            
                            Programa.CriarPDF()
                            flag =0
                            #print("max Força atingido")
                            self.emit(QtCore.SIGNAL("Parando"), 1)
                            

                        if(qforca != None and float(qforca) != 0 and (float(Forca) + (float(Forca)*float(qforca))/100)<= forcaanterior ):
                            #print(float(Forca))
                            #print(float(forcaanterior))
                            #print( (float(Forca)*float(qforca))/100 )
                            #self.runing =0
                            self.emit(QtCore.SIGNAL("Parando"), 1)
                            Programa.CriarPDF()
                            flag =0
                            #print("porcentagem de força")
                            
                            
                        flag =0
                        #print("flag0 (leu)")
                        """



class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def closeEvent(self,event):
        result = QtGui.QMessageBox.question(self,
                      "Confirmar Fechamento do Programa...",
                      "Você deseja realmente sair do programa ?",
                      QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)
        event.ignore()
        if result == QtGui.QMessageBox.Yes:
            flag2 =0
            
            Motor.Parar()
            #Programa.comport.close()
            event.accept() 
        

    
    
        

                    

class ServerThread(QtCore.QThread):
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
        #print(maxforca)
        while(flag2 == 1):
                    #global flag2
          # #print(Programa.flag2)
         
         
           
            
                    #time.sleep(0.3)
                    QtTest.QTest.qWait(100)
              
            
        
            
                    
                    
                    flag =1
                    ##print("flag1")
                    
                    
                   
                    
                    
                    
                    
                       
                        
                        
                        
                    Forca = celula.getvalue()
                    
                    tempodecorrido = (time.time() - tempinicioteste)/60
                    deslocamento = (float(VelocidadeEn))*float(tempodecorrido)
                    deslocamentos.append(deslocamento)
                    forcas.append((float(Forca)*9.8))
                    forcaanterior = forcas[-1]
                    maiorvalor = forcas.copy()
                    maiorvalor.sort()
                    ##print(maiorvalor[-1])

                    ##print(Forca)
                    
                    if( time.time()- tempo > 0.8):
                        
                        lista = [float(deslocamento),float(Forca),float(maiorvalor[-1])+30,float(deslocamentos[-1])+30,deslocamentos,forcas]
                        self.emit(QtCore.SIGNAL("UP"), lista)
                        tempo = time.time()


                        
                        
                    if( flag2 == 1 and maxdeslocamento != None and float(maxdeslocamento) != 0 and float(deslocamento) >= float(maxdeslocamento)):
                            
                            #print("entrou Maxdeslocamento alcançado ")
                            flag2 =0
                            
                            self.emit(QtCore.SIGNAL("Parando"), 1)
                            
                            
                            #print("Terminou Maxdeslocamento alcançado ")
                            lista = [float(deslocamento),float(Forca),maiorvalor[-1]+10,deslocamentos[-1]+10,deslocamentos,forcas]
                            self.emit(QtCore.SIGNAL("UP"), lista)
                            
                            
                    if(flag2 == 1 and maxforca != None and float(maxforca) != 0 and float(Forca) >= float(maxforca)):
                            
                            #print("entrou Maxforca alcançado ")


                                
                            
                            self.emit(QtCore.SIGNAL("Parando"), 1)
                            
                            flag2 =0
                            #print("max Força atingido")
                            self.emit(QtCore.SIGNAL("Parando"), 1)
                            lista = [float(deslocamento),float(Forca),maiorvalor[-1]+10,deslocamentos[-1]+10,deslocamentos,forcas]
                            self.emit(QtCore.SIGNAL("UP"), lista)

                    #if(qforca != None and float(qforca) != 0 and (float(Forca) + (float(Forca)*float(qforca))/++100)<= forcaanterior ):
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
                                        
                                    
                                        
                                    
                            self.emit(QtCore.SIGNAL("Parando"), 1)
                                    
                            lista = [float(deslocamento),float(Forca),maiorvalor[-1]+10,deslocamentos[-1]+10,deslocamentos,forcas]
                            self.emit(QtCore.SIGNAL("UP"), lista)
        

                            
                            
                            
                            
                            
                    flag =0
                    
            
            

    def run(self):
        self.start_server()
            
            
def CriarPDF():
    global VelocidadeEn
    global forcas
    global deslocamentos
    global FormatoCorpoProva
    global fig
   
    now = datetime.now()
    #print ("Iniciando o PDF")


    if os.path.isdir("Ensaios/"+str(now.year)): # vemos de este diretorio já existe
         pass
    else:
      os.mkdir("Ensaios/"+str(now.year)) # aqui criamos o diretorio
      #print ("Criado com sucesso dir ano!")
 


        


    if os.path.isdir("Ensaios/"+str(now.year)+"/"+str(now.month)): # vemos de este diretorio já existe
         pass
    else:
      os.mkdir("Ensaios/"+str(now.year)+"/"+str(now.month)) # aqui criamos o diretorio
      #print ("Criado com sucesso dir mes!")


    if os.path.isdir("Ensaios/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day)): # vemos de este diretorio já existe
         pass
    else:
      os.mkdir("Ensaios/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day)) # aqui criamos o diretorio
      #print ("Criado com sucesso dir day!")
      
    #print("Todos os diretorios criados iniciando a construção do pdf")
    Forcamaxima = forcas[-1]
    maxdeslocamento = deslocamentos[-1]
    Posicaomaxima = deslocamentos[-1]

    pdf2 = Canvas("Ensaios/"+"Ensaio_Atual.pdf", pagesize = letter) #Nome do arquivo e Tipo do papel
    #print("1")
    pdf = Canvas("Ensaios/"+str(now.year)+"/"+str(now.month)+"/"+str(now.day)+"/"+"Hora:"+str(now.hour)+"-"+str(now.minute)+ "-"+ str(now.second)+".pdf", pagesize = letter) #Nome do arquivo e Tipo do papel
    #print("2")

    pdf.setFont('Helvetica-Bold', 12)
    #print("3")
    pdf2.setFont('Helvetica-Bold', 12)
    #print("4")
    tupla = ('                                      Máquina de Ensaio de Tração e Compressão', '','','','','','','','', '                                                       Ensaio','', 'N° da Solicitação: _________', 'Solicitante/Setor: __________________________________','Inspetor: ___________________________________','Responsável: ___________________________________','Tipo de ensaio: '+tipodeensaio ,
             'Formato do corpo de prova: '+str(FormatoCorpoProva), 'Posição Máxima: '+str(Posicaomaxima)+" mm",'Força Máxima: '+str(Forcamaxima)+'N', 'Área do corpo de prova: '+str(AreaCorpoProva)+' mm²', 'Velocidadede ensaio: '+str(VelocidadeEn)+' mm/min','Comprimento do corpo de prova: __________ mm' ,'Data: ' + str(now.day)+'/'+str(now.month)+'/'+str(now.year), 'Hora: ' + str(now.hour)+":"+str(now.minute)+ ":"+ str(now.second))
    #print("5")
    lista = pdf.beginText(inch * 1, inch * 10)
    #print("6")

    lista2 = pdf2.beginText(inch * 1, inch * 10)
    #print("7")

    
    for i in range(0,len(tupla)):
        lista.textLine(tupla[i])
        lista2.textLine(tupla[i])






    
    
    #print("9")
    ax = fig.add_subplot(111,xlabel='Deslocamento(mm)', ylabel='Força(N)', title='')
    #print("10")
    ax.set_ylim(0, forcas[-1]+10)

    #print("11")
    ax.grid(True)
    #print("12")
    ax.set_xlim(0, deslocamentos[-1]+10)
    #print("13")
    ax.plot(deslocamentos,forcas)

    #print("antes do grafico PDF")
    imgdata = BytesIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)  # rewind the data

    Image = ImageReader(imgdata)
    
    pdf2.drawText(lista2)
    

    pdf2.drawImage(Image ,130,50, width=400,height=350)
    pdf2.showPage()
    
    
    pdf.drawText(lista)


    pdf.drawImage(Image ,130,50, width=400,height=350)

    pdf.showPage()

    
    

    
    
    pdf2.save()
    pdf.save()


    x = [0]
    y = [0]
    
    #print("PDF SAlVO")            
        

def Area(Retangulo_A,Retangulo_B,Tubo_L,Tubo_D,Cilindro_D,Cilindro_H):
    global AreaCorpoProva
    global FormatoCorpoProva
    FormatoCorpoProva = ""
    AreaCorpoProva = 0.0
    if(Retangulo_A  != None and Retangulo_B != None):
        
        #calcular area
        AreaCorpoProva = float(Retangulo_A) * float(Retangulo_B)
        
        #print(Retangulo_A,Retangulo_B)
        

    if(Tubo_L  != None and Tubo_D != None):
        

        AreaCorpoProva = math.pi * float(Tubo_L)* float(Tubo_D)
                                                     
        FormatoCorpoProva = "Tubo"
        
    if(Cilindro_D  != None and Cilindro_H != None):
       
        AreaCorpoProva = 2*(math.pi*((Cilindro_D*Cilindro_D)/4))+ (math.pi*(Cilindro_D*Cilindro_H)) 
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
    
    
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    
    
    
    sys.exit(app.exec_())

