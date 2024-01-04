# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_bordero_prest.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import threading
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem,QCheckBox, QMessageBox
import time
from loop_busca import Ui_Form
import easygui as g
import pandas as pd
import vglobal
import bd

if vglobal.host == '192.168.100.10/WINT':
    vglobal.vambiente = 'PRODUÇÃO'
else:
    vglobal.vambiente = 'HOMOLOGACAO'
class MyThread(QThread):
    new_prest_signal = pyqtSignal(int,str,str)
    def run(self):
        vglobal.vtotal_para_processar
        while vglobal.vprocessa_ativo_bordero:
            contador_processo = 0
            for x in range(0,1):
              df2 = pd.DataFrame(vglobal.dados)
              print("entrou aqui")
              for index, row in df2[df2['Situacao'] == 'ENCONTRADO'].iterrows():
                    contador_processo = contador_processo + 1
                    #print(row['prest'])
                    #print(row['numtransvenda'])
                    #print("CHEGOU AQUI")
                    #print(f"{str(row['numtransvenda'])} vai entrar no bordero :=  {str(vglobal.vnumbordero_prest)}")
                    self.new_prest_signal.emit((contador_processo),str(row['prest']),str(row['numtransvenda']))
                    print(f"linha {x} para  o {vglobal.vtotal_para_processar}")
                    try:
                       con = bd.conexao.conectar()
                       cursor = con.cursor()
                       sql = """
                            update PCPREST
        set
          DTULTALTER = TRUNC(SYSDATE),
          CODFUNCULTALTER = NVL(ags_func_log(),3),
          TIPOPORTADOR = 'R',
          CODPORTADOR = 1,
          NUMBORDERO = :NUMBORDERO,
          DTBORDERO = TRUNC(SYSDATE),
          CODFUNCBORDERO = NVL(ags_func_log(),3)
          where PREST = :prest
          AND NUMTRANSVENDA = :numtransvenda
                            """
                       valores_update = {'prest': str(row['prest']),
                                          'numtransvenda': int(row['numtransvenda']),
                                          'NUMBORDERO': int(vglobal.vnumbordero_prest)
                                          }
                       #print((sql,valores_update))
                       cursor.execute(sql,valores_update)
                       con.commit()
                    except Exception as E:
                     self.popup = QMessageBox()
                     self.popup.setWindowTitle("ERRO")
                     self.popup.setText("ERRO : " + str(E))
                     self.popup.exec()
     
                    finally:
                        con.close()
                        #if (int(index)) == int(vglobal.vtotal_para_processar):
                        #    break
                    if int(vglobal.vtotal_para_processar) == int(contador_processo):
                        
                        vglobal.vprocessa_ativo_bordero = False
                        #print(str(vglobal.vprocessa_ativo_bordero))
                        break
                    time.sleep(0.3)

              break
            
            break



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #"Montagem de Bordero v1.1.0" + vglobal.vambiente
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(839, 800)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/soui/sou.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fundo = QtWidgets.QFrame(self.centralwidget)
        self.fundo.setEnabled(True)
        self.fundo.setMinimumSize(QtCore.QSize(800, 800))
        self.fundo.setStyleSheet("QFrame#fundo{\n"
"\n"
"background-image: url(:/fundo/fundo.png);\n"
"}")
        self.fundo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fundo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.fundo.setObjectName("fundo")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.fundo)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.filtro = QtWidgets.QFrame(self.fundo)
        self.filtro.setMaximumSize(QtCore.QSize(16777215, 100))
        self.filtro.setStyleSheet("QFrame#filtro{\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 8px;\n"
"     border: 1px solid black;\n"
"}")
        self.filtro.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.filtro.setFrameShadow(QtWidgets.QFrame.Raised)
        self.filtro.setObjectName("filtro")
        self.layoutWidget = QtWidgets.QWidget(self.filtro)
        self.layoutWidget.setGeometry(QtCore.QRect(310, 44, 252, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.bt_importar_excel = QtWidgets.QPushButton(self.layoutWidget)
        self.bt_importar_excel.setMinimumSize(QtCore.QSize(0, 20))
        self.bt_importar_excel.setStyleSheet("QPushButton{\n"
"padding: 25%;\n"
"    background-color: rgb(218, 218, 218);\n"
"Border: 1px solid black;\n"
"border-radius: 3px;\n"
" }\n"
"QPushButton::hover{\n"
"background-color: rgb(200, 200, 200);\n"
"color:white;\n"
"}")
        self.bt_importar_excel.setObjectName("bt_importar_excel")
        self.gridLayout_2.addWidget(self.bt_importar_excel, 0, 0, 1, 1)
        self.bt_importar = QtWidgets.QPushButton(self.layoutWidget)
        self.bt_importar.setEnabled(True)
        self.bt_importar.setMinimumSize(QtCore.QSize(0, 20))
        self.bt_importar.setStyleSheet("QPushButton{\n"
"padding: 25%;\n"
"    background-color: rgb(218, 218, 218);\n"
"Border: 1px solid black;\n"
"border-radius: 3px;\n"
" }\n"
"QPushButton::hover{\n"
"background-color: rgb(200, 200, 200);\n"
"color:white;\n"
"}")
        self.bt_importar.setObjectName("bt_importar")
        self.gridLayout_2.addWidget(self.bt_importar, 0, 1, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(self.filtro)
        self.layoutWidget1.setGeometry(QtCore.QRect(50, 10, 251, 71))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.LINE_CAMINHO_EXCEL = QtWidgets.QLineEdit(self.layoutWidget1)
        self.LINE_CAMINHO_EXCEL.setEnabled(True)
        self.LINE_CAMINHO_EXCEL.setMinimumSize(QtCore.QSize(0, 20))
        self.LINE_CAMINHO_EXCEL.setMaximumSize(QtCore.QSize(300, 30))
        self.LINE_CAMINHO_EXCEL.setStyleSheet("QLineEdit{\n"
"Border: 1px solid black;\n"
"border-radius: 3px;\n"
" }")
        self.LINE_CAMINHO_EXCEL.setObjectName("LINE_CAMINHO_EXCEL")
        self.gridLayout.addWidget(self.LINE_CAMINHO_EXCEL, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.filtro)
        self.busca = QtWidgets.QFrame(self.fundo)
        self.busca.setMaximumSize(QtCore.QSize(16777215, 40))
        self.busca.setStyleSheet("QFrame#busca{\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 8px;\n"
"    border: 1px solid black;\n"
"}")
        self.busca.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.busca.setFrameShadow(QtWidgets.QFrame.Raised)
        self.busca.setObjectName("busca")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.busca)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.busca)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(300, 0))
        self.lineEdit_2.setFrame(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.label = QtWidgets.QLabel(self.busca)
        self.label.setMinimumSize(QtCore.QSize(0, 20))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.LINE_NSU_BUSCA = QtWidgets.QLineEdit(self.busca)
        self.LINE_NSU_BUSCA.setMinimumSize(QtCore.QSize(0, 22))
        self.LINE_NSU_BUSCA.setMaximumSize(QtCore.QSize(100, 16777215))
        self.LINE_NSU_BUSCA.setStyleSheet("QLineEdit{\n"
"Border: 1px solid black;\n"
"border-radius: 3px;\n"
" }")
        self.LINE_NSU_BUSCA.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.LINE_NSU_BUSCA.setObjectName("LINE_NSU_BUSCA")
        self.horizontalLayout.addWidget(self.LINE_NSU_BUSCA)
        self.bt_buscar = QtWidgets.QPushButton(self.busca)
        self.bt_buscar.setEnabled(True)
        self.bt_buscar.setMinimumSize(QtCore.QSize(0, 20))
        self.bt_buscar.setStyleSheet("QPushButton{\n"
"padding: 25%;\n"
"    background-color: rgb(218, 218, 218);\n"
"Border: 1px solid black;\n"
"border-radius: 3px;\n"
" }\n"
"QPushButton::hover{\n"
"background-color: rgb(200, 200, 200);\n"
"color:white;\n"
"}")
        self.bt_buscar.setObjectName("bt_buscar")
        self.horizontalLayout.addWidget(self.bt_buscar)
        self.verticalLayout_2.addWidget(self.busca)
        self.tabela = QtWidgets.QFrame(self.fundo)
        self.tabela.setStyleSheet("QFrame#tabela{\n"
"    \n"
"    background-color: rgb(229, 207, 255);\n"
"    border-radius: 8px;\n"
"     border: 1px solid black;\n"
"}")
        self.tabela.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tabela.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tabela.setObjectName("tabela")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabela)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.recebe_tabela = QtWidgets.QFrame(self.tabela)
        self.recebe_tabela.setStyleSheet("QFrame#recebe_tabela{\n"
"    background-color: rgb(255, 255, 255);\n"
"    \n"
"}")
        self.recebe_tabela.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.recebe_tabela.setFrameShadow(QtWidgets.QFrame.Raised)
        self.recebe_tabela.setObjectName("recebe_tabela")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.recebe_tabela)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tableWidget = QtWidgets.QTableWidget(self.recebe_tabela)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMaximumSize(QtCore.QSize(16000, 16777215))
        self.tableWidget.setStyleSheet("QTableWidget{\n"
"   border: none;\n"
"}")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.verticalLayout_4.addWidget(self.tableWidget)
        self.verticalLayout_3.addWidget(self.recebe_tabela)
        self.footer_tabela = QtWidgets.QFrame(self.tabela)
        self.footer_tabela.setMaximumSize(QtCore.QSize(16777215, 40))
        self.footer_tabela.setStyleSheet("QFrame#footer_tabela{\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 8px;\n"
"}")
        self.footer_tabela.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.footer_tabela.setFrameShadow(QtWidgets.QFrame.Raised)
        self.footer_tabela.setObjectName("footer_tabela")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.footer_tabela)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.bt_exportar_excel = QtWidgets.QPushButton(self.footer_tabela)
        self.bt_exportar_excel.setMinimumSize(QtCore.QSize(0, 25))
        self.bt_exportar_excel.setStyleSheet("QPushButton#bt_exportar_excel{\n"
"padding: 25%;\n"
"    \n"
"Border: 1px solid black;\n"
"border-radius: 3px;\n"
" }\n"
"QPushButton::hover{\n"
"background-color: rgb(200, 200, 200);\n"
"color:white;\n"
"}")
        self.bt_exportar_excel.setObjectName("bt_exportar_excel")
        self.horizontalLayout_3.addWidget(self.bt_exportar_excel)
        self.lineEdit = QtWidgets.QLineEdit(self.footer_tabela)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setFrame(False)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.bt_remover_prest = QtWidgets.QPushButton(self.footer_tabela)
        self.bt_remover_prest.setMinimumSize(QtCore.QSize(0, 25))
        self.bt_remover_prest.setStyleSheet("QPushButton#bt_remover_prest{\n"
"padding: 25%;\n"
"    \n"
"    background-color: rgb(255, 51, 0);\n"
"Border: 1px solid black;\n"
"border-radius: 3px;\n"
" }\n"
"QPushButton::hover{\n"
"background-color: rgb(200, 200, 200);\n"
"color:white;\n"
"}")
        self.bt_remover_prest.setObjectName("bt_remover_prest")
        self.horizontalLayout_3.addWidget(self.bt_remover_prest)
        self.bt_adicionar_prest = QtWidgets.QPushButton(self.footer_tabela)
        self.bt_adicionar_prest.setEnabled(True)
        self.bt_adicionar_prest.setMinimumSize(QtCore.QSize(0, 25))
        self.bt_adicionar_prest.setStyleSheet("QPushButton#bt_adicionar_prest{\n"
"padding: 25%;\n"
"    \n"
"    background-color: rgb(21, 122, 255);\n"
"Border: 1px solid black;\n"
"border-radius: 3px;\n"
" }\n"
"QPushButton::hover{\n"
"    \n"
"color:white;\n"
"}")
        self.bt_adicionar_prest.setObjectName("bt_adicionar_prest")
        self.horizontalLayout_3.addWidget(self.bt_adicionar_prest)
        self.verticalLayout_3.addWidget(self.footer_tabela)
        self.verticalLayout_2.addWidget(self.tabela)
        self.rodape = QtWidgets.QFrame(self.fundo)
        self.rodape.setMaximumSize(QtCore.QSize(16777215, 50))
        self.rodape.setStyleSheet("QFrame#rodape{\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-radius: 8px;\n"
"     border: 1px solid black;\n"
"}")
        self.rodape.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.rodape.setFrameShadow(QtWidgets.QFrame.Raised)
        self.rodape.setObjectName("rodape")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.rodape)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.progressBar = QtWidgets.QProgressBar(self.rodape)
        self.progressBar.setEnabled(False)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setVisible(False)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.bt_montar = QtWidgets.QPushButton(self.rodape)
        self.bt_montar.setMinimumSize(QtCore.QSize(0, 20))
        self.bt_montar.setStyleSheet("QPushButton#bt_montar{\n"
"padding: 25%;\n"
"    background-color: rgb(0, 255, 0);\n"
"Border: 1px solid black;\n"
"border-radius: 3px;\n"
" }\n"
"QPushButton::hover{\n"
"background-color: rgb(200, 200, 200);\n"
"color:white;\n"
"}")
        self.bt_montar.setObjectName("bt_montar")
        self.horizontalLayout_2.addWidget(self.bt_montar)
        self.verticalLayout_2.addWidget(self.rodape)
        self.verticalLayout.addWidget(self.fundo)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow"," Montagem de Bordero v1.1.0 - " + vglobal.vambiente))
        self.bt_importar_excel.setText(_translate("MainWindow", "Importar Excel"))
        self.bt_importar.setText(_translate("MainWindow", "Processar"))
        self.label_2.setText(_translate("MainWindow", "Caminho:"))
        self.label.setText(_translate("MainWindow", "NSU:"))
        self.LINE_NSU_BUSCA.setInputMask(_translate("MainWindow", "00000000000000000000"))

        #ocultar botão de buscar para entrar o de mostrar para atualizar o qtable

        self.bt_buscar.setText(_translate("MainWindow", vglobal.vtitulo_qtable))
        self.LINE_NSU_BUSCA.setVisible(False)
        self.label.setVisible(False)


        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Nf"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Vlb. da parcela att"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Nsu"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "%"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Bandeira"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Numtransvenda"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Cliente"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Status"))
        self.bt_exportar_excel.setText(_translate("MainWindow", vglobal.vexportar))
        self.bt_remover_prest.setText(_translate("MainWindow", "Remover Título"))
        self.bt_adicionar_prest.setText(_translate("MainWindow", "Adicionar Título"))
        self.bt_montar.setText(_translate("MainWindow", "Montar Bordero"))
        self.bt_importar_excel.clicked.connect(self.importexcel)
        self.LINE_CAMINHO_EXCEL.setEnabled(False)
        self.bt_importar.setEnabled(False)
        self.bt_importar.clicked.connect(self.processar_excel)
        self.bt_buscar.clicked.connect(self.atualizar_tela)
        self.bt_montar.clicked.connect(self.montar_bordero_ativar)
        self.thread = MyThread()
        self.thread.new_prest_signal.connect(self.montar_bordero)
        self.bt_exportar_excel.clicked.connect(self.exportar_excel)

        #BOTÕES OCULTOS PARA DESENVOLVIMENTO
        self.bt_remover_prest.setVisible(False)
        self.bt_adicionar_prest.setVisible(False)

#AQUI INICIA AS FUNÇÕES DA ROTINA
    def exportar_excel(self):
        if vglobal.vexportar == "GERAR MODELO":
            dados = {'NF': [1],
                     'bandeira': "MCRE",
                         'NSU/CV': [4],
                         'valor bruto da parcela atualizada': 1.00}
                         
            df_modelo = pd.DataFrame(dados)            
            # Criar um arquivo Excel com uma planilha chamada 'planilha1'
            title = 'Escolher caminho do Excel'
            file_path = g.diropenbox(title)
            caminho_arquivo = file_path+'\modelo_importacao_bordero.xlsx'
            with pd.ExcelWriter(caminho_arquivo, engine='openpyxl') as writer:
                df_modelo.to_excel(writer, sheet_name='planilha', index=False)
        else:
            title = 'Escolher caminho do Excel'
            file_path = g.diropenbox(title)
            df_exportar = pd.DataFrame(vglobal.dados)
            caminho_arquivo_exportar = file_path+'\EXCEL_BORDERO_MONTADO.xlsx'
            df_exportar.to_excel(caminho_arquivo_exportar, sheet_name='planilha1', index=False)
        self.popup = QMessageBox()
        self.popup.setWindowTitle("Sucesso")
        self.popup.setText("arquivo exportado com sucesso")
        self.popup.exec()
    def numero_bordero(self):
                  try:
                          con = bd.conexao.conectar()
                          cursor = con.cursor() 
                          sql = f"""
                              SELECT NVL(PROXNUMBORDEROCR,1) PROXNUMBORDEROCR FROM PCCONSUM
                          """
                          
                          cursor.execute(sql)
                          
                          result = cursor.fetchone()
                          if len(result) > 0:
                              vglobal.vnumbordero_prest = result[0]
                              sql = f"""
                              SELECT NVL(PROXNUMBORDEROCR,1) PROXNUMBORDEROCR FROM PCCONSUM FOR UPDATE
                          """
                              
                              cursor.execute("UPDATE PCCONSUM SET PROXNUMBORDEROCR=(NVL(PROXNUMBORDEROCR,1)+1) WHERE ROWNUM = 1")
                              
                              
                              #
         
                  except Exception as e:
                      self.popup = QMessageBox()
                      self.popup.setWindowTitle("Cancelando Processo")
                      self.popup.setText("1 erro foi encontrado \n" + e)
                      self.popup.exec()
                  finally:
                      con.commit()
                      cursor.close()
                      con.close()
    def atualizar_tela(self):
        df1 = pd.DataFrame(vglobal.dados)
        file_path = self.LINE_CAMINHO_EXCEL.text()
        if file_path:
         try:
            #print(file_path)
            # Ler o arquivo Excel e obter os dados em um DataFrame
            #df = pd.read_excel(file_path,sheet_name='planilha',engine='openpyxl') 
            
            # Conectar ao banco de dados Oracle
            #self.tableWidget.setRowCount(df1.shape[0])
            
            total_encontrado = (df1['Situacao'] == 'ENCONTRADO').sum()
            
            self.tableWidget.setRowCount(total_encontrado)
            # intera sobre as linhas do DataFrame e executar as inserções
            row_id = 0
            for index, row in df1[df1['Situacao'] == 'ENCONTRADO'].iterrows():
                  
                Nf = row['Nf']
                BANDEIRA = row['bandeira']
                NSU = row['nsu']
                vl_parcela_att= row['vl_prest']
                Numtransvenda = row['numtransvenda']
                Cliente= row['Cliente']
                Situacao = row['Situacao']
                if Situacao == "ENCONTRADO":
                    self.tableWidget.setItem(row_id, 0, QtWidgets.QTableWidgetItem(str(Nf)))
                    self.tableWidget.setItem(row_id, 1, QtWidgets.QTableWidgetItem(str(vl_parcela_att)))
                    self.tableWidget.setItem(row_id, 2, QtWidgets.QTableWidgetItem(str(NSU)))
                    self.tableWidget.setItem(row_id, 3, QtWidgets.QTableWidgetItem(str('100')))
                    self.tableWidget.setItem(row_id, 4, QtWidgets.QTableWidgetItem(str(BANDEIRA)))
                    self.tableWidget.setItem(row_id, 5, QtWidgets.QTableWidgetItem(str(Numtransvenda)))
                    self.tableWidget.setItem(row_id, 6, QtWidgets.QTableWidgetItem(str(Cliente)))
                    self.tableWidget.setItem(row_id, 7, QtWidgets.QTableWidgetItem(str(Situacao)))

                    row_id += 1
                    vglobal.vtotal_para_processar = row_id
            
            #self.tb_consulta.setColumnCount(df.shape[1])
            #excit[Nf,Dtvenda,Valorvenda,Parcela,Bandeira,Nsu] = [Nf,DTVENDA,VALORVENDA,PARCELA,BANDEIRA,NSU] 
            
            self.bt_buscar.setText("Buscar")
            self.LINE_NSU_BUSCA.setVisible(True)
            self.label.setVisible(True)     
         except Exception as e:
            # Mostrar uma mensagem de erro na tela
            print('erro ao importar',e)

    def importexcel(self):
       # print('teste')
      #connection_info = read_connection_info()
       # Abrir a janela de diálogo para selecionar o arquivo Excel
      #  file_path = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx')])
        title = 'Escolher caminho do Excel'
        file_path = g.fileopenbox( title )
        vglobal.vcaminho = file_path
        try:
            file = open( file_path )
            self.LINE_CAMINHO_EXCEL.setText(file_path)
            self.bt_importar.setEnabled(True)
        except:
            self.LINE_CAMINHO_EXCEL.setText("")
            self.bt_importar.setEnabled(False)
            self.popup = QMessageBox()
            self.popup.setWindowTitle("AVISO")
            self.popup.setText("SELECIONE 1 ARQUIVO")
            self.popup.exec_()
            print('Nenhum arquivo selecionado')
    def processar_excel(self):
        self.bt_buscar.setText(vglobal.vtitulo_qtable)
        self.LINE_NSU_BUSCA.setVisible(False)
        self.label.setVisible(False)
        vglobal.vtitulo = "Cancelar"
        self.Form = QtWidgets.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.Form)
        self.Form.show()
        file_path = self.LINE_CAMINHO_EXCEL.text()
        vglobal.vcaminho = file_path
        vglobal.vexportar = "EXPORTAR"
        self.bt_exportar_excel.setText(vglobal.vexportar)
        vglobal.vcomecar_bordero = 0
    def montar_bordero_ativar(self):
        if vglobal.vtotal_para_processar == 0:
            self.popup = QMessageBox()
            self.popup.setWindowTitle("Aviso")
            self.popup.setText("Nenhuma prestação para montar bordero, importe 1 arquivo")
            self.popup.exec()
            return
        self.numero_bordero()
        if vglobal.vcomecar_bordero == 0:
            vglobal.vprocessa_ativo_bordero = True
            self.bt_montar.setVisible(False)
            self.progressBar.setVisible(True)
            self.thread.start()
            vglobal.vcomecar_bordero = 1

        
        #self.bt_montar.setVisible(True)
        #self.progressBar.setVisible(False)
    def pop_upsucesso(self):
        try:
                con = bd.conexao.conectar()
                cursor = con.cursor()
                sql = " insert into ags_log (data,aplicacao,codigo,json) values(sysdate,:aplicacao,:codigo,:json)"
                valores_insert ={
                    'aplicacao': 'BORDERO_PREST',
                    'codigo': int(vglobal.vnumbordero_prest),
                    'json': str(vglobal.dados)
                }
                cursor.execute(sql,valores_insert)
                
                self.popup = QMessageBox()
                self.popup.setWindowTitle("Sucesso")
                self.popup.setText("Bordero a receber montado com : " + str(vglobal.vtotal_para_processar)+ " títulos \nNúmero Bordero :" + str(vglobal.vnumbordero_prest) +"\n\n#Exporte os dados para válidar os títulos que foram adicionados ou não! ")
                self.popup.exec()

        except Exception as erro:
            self.bt_montar.setVisible(True)
            self.progressBar.setVisible(False)
            self.progressBar.setProperty("value", 0)
            self.popup = QMessageBox()
            self.popup.setWindowTitle("Erro")
            self.popup.setText("Erro ao Salvar log : " + str(erro))
            self.popup.exec()
        finally:
                con.commit()
                cursor.close()
                con.close()
    def montar_bordero(self,valor,prest,numtrasnvenda):
        vglobal.vprocessa_ativo_bordero = True
        try:
           perc = ((int(valor))*100) / int(vglobal.vtotal_para_processar)
           MainWindow.setEnabled(False)
           self.atualizar_perc(perc)
              

        except Exception as E:
            MainWindow.setEnabled(True)
            self.popup = QMessageBox()
            self.popup.setWindowTitle("Cancelando Processo")
            self.popup.setText("1 erro foi encontrado " + str(E))
            self.popup.exec()
        #print(str(vglobal.vtotal_para_processar) + "total que tem que processar  e esse é o valor" + str(valor))
        
        
            
# Mostrar uma mensagem de sucesso na tela

    def atualizar_perc(self,perc):
        self.progressBar.setProperty("value", (perc))
        if (perc) == 100:
            MainWindow.setEnabled(True)
            vglobal.vprocessa_ativo_bordero = False
            self.bt_montar.setVisible(True)
            self.progressBar.setVisible(False)
            self.progressBar.setProperty("value", 0)
            time.sleep(2)
            self.pop_upsucesso()


            vglobal.vtotal_para_processar = 0
            vglobal.dados.clear()
            vglobal.vtotal_achado = 0

import fundo
import soui


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
