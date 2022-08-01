# Blibiotecas
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QToolButton, QLineEdit, QMessageBox, QFileDialog, QPlainTextEdit, QComboBox, QCheckBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QLine, QUrl, QSize, qInf
from PyQt5.QtGui import QIcon, QPixmap, qPixelFormatAlpha
import threading

from distutils.log import error
import subprocess
import qrcode
import random
import platform
import os
from qrcode.image.styledpil import StyledPilImage


application = QApplication([])

# Redimencionando a Janela Princial
mainWindow = QMainWindow()
mainWindow.setGeometry(0, 0, 650, 900)
mainWindow.setMinimumHeight(900)
mainWindow.setMaximumHeight(900)
mainWindow.setMinimumWidth(650)
mainWindow.setMaximumWidth(650)

# Custimização da Janela
mainWindow.setWindowTitle("Senhas Salvas")
mainWindow.setStyleSheet("background-color: rgb(255,255,255);")
mainWindow_icon = QIcon()
mainWindow_icon.addPixmap(QPixmap("./src/icones/senhas.ico"))
mainWindow.setWindowIcon(mainWindow_icon)

background = QLabel(mainWindow)
background.setStyleSheet("background-color: rgb(255,255,255);")
background.resize(650, 900)
background.move(0, 0)
background.setPixmap(QPixmap('./src/icones/background.png'))

# TextArea
listas_text = QPlainTextEdit(mainWindow)
listas_text.setStyleSheet("font-size : 20px;")
listas_text.resize(510, 215)
listas_text.move(70, 105)

# RUN
play_button = QToolButton(mainWindow)
play_button.setGeometry(300, 330, 50, 50)
play_button_icon = QIcon()
play_button_icon.addPixmap(QPixmap("./src/icones/play.png"))
play_button.setIcon(play_button_icon)
play_button.setStyleSheet("background-color: transparent;")
play_button.setIconSize(QSize(50, 50))

# Botão de Barra de Pesquisa
go_line = QLineEdit(mainWindow)
go_line.setGeometry(75, 400, 500, 45)
go_line.setStyleSheet("background-color: rgb(255,255,255); font-size: 20px;")

# Botão de Pesquisa
go_button = QToolButton(mainWindow)
go_button.setGeometry(-70, -70, 50, 50)
go_button_icon = QIcon()
go_button_icon.addPixmap(QPixmap("./src/icones/go.png"))
go_button.setIcon(go_button_icon)
go_button.setStyleSheet("background-color: transparent;")
go_button.setIconSize(QSize(40, 40))

# Lista Type
type_text = QLabel(mainWindow)
type_text.setStyleSheet("background-color : transparent; font-size : 20px;")
type_text.resize(50, 30)
type_text.setText("Tipo: ")
type_text.move(98, 460)

type_check = QComboBox(mainWindow)
type_check.setGeometry(150, 460, 125, 30)
type_list = ["WPA", "WEP", "nopass"]
type_check.addItems(type_list)

# Lista Hidden
hidden_text = QLabel(mainWindow)
hidden_text.setStyleSheet("background-color : transparent; font-size : 20px;")
hidden_text.resize(65, 30)
hidden_text.setText("Status: ")
hidden_text.move(310, 460)

hidden_check = QComboBox(mainWindow)
hidden_check.setGeometry(375, 460, 125, 30)
hidden_list = ["False", "True"]
hidden_check.addItems(hidden_list)

# Icon Center
icon_text = QLabel(mainWindow)
icon_text.setStyleSheet("background-color : transparent; font-size : 20px;")
icon_text.resize(55, 30)
icon_text.setText("Icone: ")
icon_text.move(192, 500)

icon_check = QComboBox(mainWindow)
icon_check.setGeometry(250, 500, 150, 30)
icon_list = ["False", "True"]
icon_check.addItems(icon_list)

# QRCODE
qrcode_img = QLabel(mainWindow)
qrcode_img.setStyleSheet("background-color: rgb(255,255,255);")
qrcode_img.resize(250, 250)
qrcode_img.move(200, 550)
qrcode_img.setPixmap(QPixmap("./src/imagem/exemple.png").scaled(250, 250))

# Save
save_button = QToolButton(mainWindow)
save_button.setGeometry(-70, -70, 50, 50)
save_button_icon = QIcon()
save_button_icon.addPixmap(QPixmap("./src/icones/save.png"))
save_button.setIcon(save_button_icon)
save_button.setStyleSheet("background-color: transparent;")
save_button.setIconSize(QSize(50, 50))

# Funcoes

global profiles
global senha_profiles
global img
global wifi_a

def Scan():
    global profiles
    global senha_profiles
    lista_wifi = subprocess.check_output(['netsh', 'wlan', 'show', 'profile']).decode(
        'utf-8', errors="ignore").split('\n')
    profiles = [i.split(":")[1][1:-1]
                for i in lista_wifi if "Todos os Perfis de Usurios" in i]
    senha_profiles = []

    for i in profiles:
        try:
            senha = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', f"name={i}", 'KEY=clear']).decode(
                'utf-8', errors="ignore").split('\n')
            senha = [x.split(":")[1][1:-1]
                     for x in senha if "Contedo da Chave" in x]
            senha_profiles.append(senha[0])

        except:
            senha_profiles.append("Não foi encontrada")

    return profiles, senha_profiles


def Print(profiles, senha_profiles):
    listas_text.clear()
    for i in range(0, len(profiles)):
        listas_text.insertPlainText(
            f"WIFI = {profiles[i]} | KEY = {senha_profiles[i]}\n\n")
    go_button.setGeometry(575, 400, 50, 50)

def RUN():
    profiles, senha_profiles = Scan()
    Print(profiles, senha_profiles)

def Play(mainWindow):
    threading.Thread(target=RUN).start()

def QRCODE(wifi, senha):
    global img
    global wifi_a
    profile = wifi
    profile_senha = senha
    wifi_a = "NULL"
    senha_a = "NULL"

    wifi = go_line.text()
    for i in range(0, len(profile)):
        if profile[i] == wifi:
            wifi_a = profile[i]
            senha_a = profile_senha[i]

    if(wifi_a != "NULL"):
        type = type_check.currentText()
        hidden = hidden_check.currentText()
        icon = icon_check.currentText()
        qr = qrcode.QRCode(version=3, error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(f"WIFI:T:{type};S:{wifi_a};P:{senha_a};H:{hidden};;")
        
        if(icon == "True"):
            img = qr.make_image(image_factory=StyledPilImage, embeded_image_path="./src/imagem/signal.png")
        else:
            img = qr.make_image()

        img.save(f"./src/imagem/{wifi_a}.png")
        qrcode_img.setPixmap(QPixmap(f"./src/imagem/{wifi_a}.png").scaled(250, 250))
        os.remove(f"./src/imagem/{wifi_a}.png")
        save_button.setGeometry(300, 815, 50, 50)
    
def Create(mainWindow):
    global profiles
    Profiles = profiles
    global senha_profiles
    Senha_profiles = senha_profiles
    QRCODE(Profiles, Senha_profiles)

def Save(mainWindow):
    global img
    global wifi_a
    path = QFileDialog.getSaveFileName(None, "Salvar Aonde?", f"{wifi_a}.png")
    img.save(path[0])


# Connects
play_button.clicked.connect(Play)
go_button.clicked.connect(Create)
save_button.clicked.connect(Save)

# Exibir
mainWindow.show()
application.exec_()
