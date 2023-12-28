# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loop_busca.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import vglobal
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem,QCheckBox, QMessageBox
import easygui as g
import pandas as pd
import time
import bd
class MyThread(QThread):
    new_prest_signal = pyqtSignal(str,str,str,str,int,int,str)

    def run(self):
        while vglobal.vprocessa_ativo:
            status = 'NÃO ENCONTRADO'
            try:
               file_path = vglobal.vcaminho
               if file_path:
                print(file_path)
                # Ler o arquivo Excel e obter os dados em um DataFrame
                df = pd.read_excel(file_path,sheet_name='planilha',engine='openpyxl') 
                tot = len(df)             
                # intera sobre as linhas do DataFrame e executar as inserções
                for index, row in df.iterrows():
                    if vglobal.vprocessa_ativo == False:
                        break
                    Nf = row['NF']
                    BANDEIRA = row['bandeira']
                    NSU = row['NSU/CV']
                    print(NSU)
                    vl_parcela_att= row['valor bruto da parcela atualizada']
                    try:
                            con = bd.conexao.conectar()
                            cursor = con.cursor()
                            sql = f"""
                            SELECT OBS2,min(PREST),numtransvenda,'ENCONTRADO' as status FROM PCPREST C 
        WHERE duplic = {Nf} 
        AND VALOR <= {vl_parcela_att} + 0.10
        AND VALOR >={vl_parcela_att} - 0.10
        AND NSUTEF = {NSU} 
        AND CODCOB NOT IN ('DESD','CANC','DEVT','BNFT','ESTR')
        AND NVL(VPAGO,0) = 0
        AND EXISTS(SELECT 1 FROM PCCOB WHERE (NVL(PCCOB.CARTAO,'N') = 'S' OR PCCOB.CODCOB = 'CARC') AND PCCOB.CODCOB = C.CODCOB)
AND NVL(NUMTRANS,0) = 0
AND DTBAIXA IS NULL
group by OBS2,numtransvenda

        
                            """
                            print(sql)
                            cursor.execute(sql)
                            
                            result = cursor.fetchall()
                            if len(result) > 0:
                               vglobal.dados.append({"Nf": str(Nf),"vl_prest": vl_parcela_att,'nsu': NSU,"%": "100","bandeira" : BANDEIRA,
                                                     "numtransvenda": str(result[0][2]),"Cliente" : str(result[0][0]),
                                                     "prest" : str(result[0][1]),"Situacao": str(result[0][3])})
                               self.new_prest_signal.emit(str(Nf),str(NSU),str(result[0][2]),str(str(index+1)+"/"+str(tot)),tot,int(index+1),str(result[0][3]))
                            else: 
                                vglobal.dados.append({"Nf": str(Nf),"vl_prest": vl_parcela_att,'nsu': NSU,"%": "100","bandeira" : BANDEIRA,
                                                     "numtransvenda": "000000","Cliente" : "Não encontrado",
                                                     "prest" : "0","Situacao": status})
                                self.new_prest_signal.emit(str(Nf),str(NSU),"000000",str(str(index+1)+"/"+str(tot)),tot,int(index+1),status)
                            time.sleep(0.1)
                
                    except Exception as e:
                        self.popup = QMessageBox()
                        self.popup.setWindowTitle("Cancelando Processo")
                        self.popup.setText("1 erro foi encontrado \n" + e)
                        self.popup.exec()
                    finally:
                        cursor.close()
                        con.close()
                    
            
                   
            except Exception as F:
              print(f"erro :{F}")
            time.sleep(20)
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(500, 400))
        Form.setMaximumSize(QtCore.QSize(500, 400))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/soui/sou.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fundo_loop = QtWidgets.QFrame(Form)
        self.fundo_loop.setStyleSheet("QFrame#fundo_loop{\n"
"    background-image: url(:/fundo/fundo.png);\n"
"}")
        self.fundo_loop.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fundo_loop.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fundo_loop.setObjectName("fundo_loop")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.fundo_loop)
        self.verticalLayout_2.setContentsMargins(15, 15, 15, 15)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dados_busca = QtWidgets.QFrame(self.fundo_loop)
        self.dados_busca.setStyleSheet("QFrame#dados_busca{\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 8px;\n"
"}")
        self.dados_busca.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dados_busca.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dados_busca.setObjectName("dados_busca")
        self.line = QtWidgets.QFrame(self.dados_busca)
        self.line.setGeometry(QtCore.QRect(0, 229, 471, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.dados_busca)
        self.line_2.setGeometry(QtCore.QRect(0, 320, 471, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.layoutWidget = QtWidgets.QWidget(self.dados_busca)
        self.layoutWidget.setGeometry(QtCore.QRect(189, 338, 171, 23))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)
        self.var_encontrado = QtWidgets.QLabel(self.layoutWidget)
        self.var_encontrado.setObjectName("var_encontrado")
        self.gridLayout_3.addWidget(self.var_encontrado, 0, 1, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(self.dados_busca)
        self.layoutWidget1.setGeometry(QtCore.QRect(11, 338, 131, 23))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)
        self.var_total = QtWidgets.QLabel(self.layoutWidget1)
        self.var_total.setObjectName("var_total")
        self.gridLayout_2.addWidget(self.var_total, 0, 1, 1, 1)
        self.frame_loop = QtWidgets.QFrame(self.dados_busca)
        self.frame_loop.setGeometry(QtCore.QRect(0, 0, 471, 241))
        self.frame_loop.setStyleSheet("")
        self.frame_loop.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_loop.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_loop.setObjectName("frame_loop")
        self.layoutWidget2 = QtWidgets.QWidget(self.frame_loop)
        self.layoutWidget2.setGeometry(QtCore.QRect(259, 60, 201, 161))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.var_processando = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.var_processando.setFont(font)
        self.var_processando.setAlignment(QtCore.Qt.AlignCenter)
        self.var_processando.setObjectName("var_processando")
        self.gridLayout.addWidget(self.var_processando, 0, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_7.setMaximumSize(QtCore.QSize(110, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_5.setMaximumSize(QtCore.QSize(110, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_8.addWidget(self.label_5, 0, 0, 1, 1)
        self.var_status = QtWidgets.QLabel(self.layoutWidget2)
        self.var_status.setMinimumSize(QtCore.QSize(60, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.var_status.setFont(font)
        self.var_status.setStyleSheet("QLabel#var_status{\n"
"color:green;\n"
"}")
        self.var_status.setAlignment(QtCore.Qt.AlignCenter)
        self.var_status.setObjectName("var_status")
        self.gridLayout_8.addWidget(self.var_status, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_8, 0, 0, 1, 1)
        self.layoutWidget3 = QtWidgets.QWidget(self.frame_loop)
        self.layoutWidget3.setGeometry(QtCore.QRect(12, 74, 221, 101))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.layoutWidget3)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_2.setMaximumSize(QtCore.QSize(40, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 0, 0, 1, 1)
        self.var_nf = QtWidgets.QLabel(self.layoutWidget3)
        self.var_nf.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.var_nf.setObjectName("var_nf")
        self.gridLayout_5.addWidget(self.var_nf, 0, 1, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_3.setMaximumSize(QtCore.QSize(40, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_6.addWidget(self.label_3, 0, 0, 1, 1)
        self.var_nsu = QtWidgets.QLabel(self.layoutWidget3)
        self.var_nsu.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.var_nsu.setObjectName("var_nsu")
        self.gridLayout_6.addWidget(self.var_nsu, 0, 1, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_6, 1, 0, 1, 1)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_7.addWidget(self.label_4, 0, 0, 1, 1)
        self.var_numtransvenda = QtWidgets.QLabel(self.layoutWidget3)
        self.var_numtransvenda.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.var_numtransvenda.setObjectName("var_numtransvenda")
        self.gridLayout_7.addWidget(self.var_numtransvenda, 0, 1, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_7, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frame_loop)
        self.label.setGeometry(QtCore.QRect(166, 10, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.line_3 = QtWidgets.QFrame(self.frame_loop)
        self.line_3.setGeometry(QtCore.QRect(0, 40, 470, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.frame_loop)
        self.line_4.setGeometry(QtCore.QRect(234, 50, 17, 184))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self.frame_loop)
        self.line_5.setGeometry(QtCore.QRect(262, 140, 190, 3))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.pushButton = QtWidgets.QPushButton(self.dados_busca)
        self.pushButton.setGeometry(QtCore.QRect(369, 333, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.progressBar = QtWidgets.QProgressBar(self.dados_busca)
        self.progressBar.setGeometry(QtCore.QRect(8, 259, 451, 51))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.label_9 = QtWidgets.QLabel(self.dados_busca)
        self.label_9.setGeometry(QtCore.QRect(201, 277, 81, 16))
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.dados_busca)
        self.verticalLayout.addWidget(self.fundo_loop)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Buscando títulos"))
        self.label_8.setText(_translate("Form", "Encontrado :"))
        self.var_encontrado.setText(_translate("Form", "0/0"))
        self.label_6.setText(_translate("Form", "Total :"))
        self.var_total.setText(_translate("Form", "0"))
        self.var_processando.setText(_translate("Form", "0/0"))
        self.label_7.setText(_translate("Form", "Processando:"))
        self.label_5.setText(_translate("Form", "Status:"))
        self.var_status.setText(_translate("Form", ""))
        self.label_2.setText(_translate("Form", "Nf :"))
        self.var_nf.setText(_translate("Form", ""))
        self.label_3.setText(_translate("Form", "Nsu"))
        self.var_nsu.setText(_translate("Form", ""))
        self.label_4.setText(_translate("Form", "Numtransvenda:"))
        self.var_numtransvenda.setText(_translate("Form", ""))
        self.label.setText(_translate("Form", "Buscando"))
        self.pushButton.setText(_translate("Form", vglobal.vtitulo))
        self.label_9.setText(_translate("Form", "Processando"))
        #inicia já chamando a função para ir carregando a tela
        vglobal.vprocessa_ativo = True
        self.thread = MyThread()
        self.thread.new_prest_signal.connect(self.processar_carregamento)
        self.thread.start()
        self.pushButton.clicked.connect(lambda: self.cancelar(Form))
    def cancelar(self,Form):
        if vglobal.vtitulo == "voltar":
             vglobal.vprocessa_ativo = False
             
             Form.close()
        else:
             vglobal.vprocessa_ativo = False
             self.popup = QMessageBox()
             self.popup.setWindowTitle("Cancelando Processo")
             self.popup.setText("Processo de importação de títulos cancelado!")
             self.popup.exec()
             Form.close()

    def processar_carregamento(self,Nf,NSU,Numtransvend,processando,tot,inde,status):
         print("entrou")
         try:
                #definindo valores na tela a medida em que processar
                self.var_nf.setText(str(Nf))
                self.var_nsu.setText(str(NSU))
                self.var_numtransvenda.setText(str(Numtransvend))
                self.var_processando.setText(str(processando))
                self.progressBar.setProperty("value", int((int(inde)*100)/int(tot)))
                self.var_total.setText(str(tot))
                print(status)
                if status == 'ENCONTRADO':
                  self.var_status.setStyleSheet("QLabel#var_status{\n"
"color:green;\n"
"}")
                  self.var_status.setText("Encontrado")
                  vglobal.vtotal_achado = vglobal.vtotal_achado + 1
                else:
                    self.var_status.setStyleSheet("QLabel#var_status{\n"
"color:red;\n"
"}")
                    self.var_status.setText("Não Encontrado")
                self.var_encontrado.setText( str(vglobal.vtotal_achado) + "/" + str(tot))
                if int((int(inde)*100)/int(tot)) == 100 :
                    vglobal.vprocessa_ativo = False
                    self.popup = QMessageBox()
                    self.popup.setWindowTitle("Processo Concluido")
                    self.popup.setText("Processo de importação de títulos Concluído!")
                    self.popup.exec()
                    self.pushButton.setStyleSheet("QPushButton#pushButton{\n"
"padding: 25%;\n"
"    background-color: rgb(0, 255, 0);\n"
"Border: 1px solid black;\n"
"border-radius: 3px;\n"
" }\n"
"QPushButton::hover{\n"
"background-color: rgb(200, 200, 200);\n"
"color:white;\n"
"}")
                    vglobal.vtitulo = "voltar"
                    self.pushButton.setText("voltar")
                    
                    
               

            
            #self.tb_consulta.setColumnCount(df.shape[1])
            #excit[Nf,Dtvenda,Valorvenda,Parcela,Bandeira,Nsu] = [Nf,DTVENDA,VALORVENDA,PARCELA,BANDEIRA,NSU] 
            
              
         except Exception as e:
            # Mostrar uma mensagem de erro na tela
            print('erro ao importar',e)
        


import fundo
import loop_carrega
import soui


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
