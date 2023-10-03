import sys
import time 
import os
import json
import csv
import pandas
from loginscreen import Ui_MainWindow
from mainscreen import Main_Ui_Class
from gamescreen import Game_Ui_Class
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class Login(QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        self.login_screen = Ui_MainWindow()
        self.login_screen.setupUi(self)
        self.convert_data()
        self.login_screen.login_btn_signup.clicked.connect(self.SignUp)
        self.login_screen.login_btn_login.clicked.connect(self.Login)
       ########################
        self.s = 0
        self.user=""
        
        #######################
       
    def convert_data(self):
        #This function converts .xlsx file to .csv file by using pandas.
        xlsLocation = os.getcwd()
        read_file = pandas.read_excel(xlsLocation)
        read_file.to_csv ("words_list.csv",index = None, header=True)
        #The function determines Key values. For first column "Dutch" and for second column "English" 
        with open("words_list.csv")as csvfile:
            key = ("Dutch","English")
            reader = csv.DictReader( csvfile,key)
            out = json.dumps([ row for row in reader ],indent=1)
        # After converting files, creates a new json file and loads all datas as dictionary type. 
        with open("data_w.json","w",encoding="utf-8")as jsonfile:
            jsonfile.write(out)
        pass
            
    def go_main(self):
        main_s = Main(self.user)
        widget.addWidget(main_s)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def Login(self):
        self.user = self.login_screen.login_edt_username.text()
        fileLocation = os.getcwd()
        user_l=[]
        if self.user == "" :
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.messagebox=QtWidgets.QMessageBox()
            self.messagebox.critical(self,'WARNING','Please Enter Username')
            self.messagebox.setWindowIcon(icon)
        else:
            with os.scandir(fileLocation) as place:
                # self.go_main()
                
                for nameList in place:
                    user_l.append(nameList.name)
                    
                if f"{self.user}.json" in user_l:
                    with open(f"{self.user}.json", encoding="utf-8") as file:
                        print("Successful")
                    self.go_main()
                    
                else:
                    user_dic={"username":self.user,"level":"1"}
                    with open(f"{self.user}.json", "w", encoding="utf-8") as file:
                        json.dump(user_dic, file)
                    
                    self.go_main() 

    def SignUp(self):
        user_list=[]
        self.user = self.login_screen.login_edt_username.text()
        fileLocation = os.getcwd()
        if self.user == "" :
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.messagebox=QtWidgets.QMessageBox()
            self.messagebox.critical(self,'WARNING','Please Enter Username')
            self.messagebox.setWindowIcon(icon)
        else:
            with os.scandir(fileLocation) as place:
                for nameList in place:
                  
                    user_list.append(nameList.name)
               
            if f"{self.user}.json" in user_list:
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.messagebox=QtWidgets.QMessageBox()
                self.messagebox.critical(self,'WARNING','This username is not available. \n\nCreate new username! ')
                self.messagebox.setWindowIcon(icon)
            
            else:
                user_dic={"username":self.user,"level":"1"}
                with open(f"{self.user}.json", "w", encoding="utf-8") as file:
                    json.dump(user_dic, file)
                self.go_main()        
        user_list=[]
        
class Main(QMainWindow):
    def __init__(self,user):
        super(Main,self).__init__()
        self.user = user
        self.main_screen = Main_Ui_Class()
        self.main_screen.setupUi(self)
        self.main_screen.main_btn_play.clicked.connect(self.go_game)
        self.main_screen.main_btn_quit.clicked.connect(self.Quit)
        self.main_screen.main_txt_player.setText("Player : "+self.user)

        with open(f"{self.user}.json", encoding="utf-8") as file:
            veri = json.load(file)
            file.close()
        userlevel=veri["level"]
        
        self.main_screen.progressBar.setProperty("value", int(userlevel))
        self.main_screen.main_txt_level.setText(userlevel+"/20")
        
    def go_game(self):
        game_s = Game(self.user)
        widget.addWidget(game_s)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def Quit(self):
        
        sys.exit(app.exec())

class Game(QMainWindow):
    def __init__(self,user):
        super(Game,self).__init__()
        self.user = user
        self.game_screen = Game_Ui_Class()
        self.game_screen.setupUi(self)
        
        self.game_screen.game_btn_back.clicked.connect(self.go_main)
        
        with open(f"{self.user}.json", encoding="utf-8") as file:
            veri = json.load(file)
            file.close()
        userlevel=veri["level"]
        
        self.level=int(userlevel)
        
        self.s = (self.level-1)*20
        self.word = True
        self.wordCounter=0
        self.totalCounter=20
        self.levelCounter=0
        self.game_screen.game_btn_yes.setEnabled(False)
        self.game_screen.game_btn_no.setEnabled(False)
        self.DutchWord()
        self.wrong_list = {}
        self.game_screen.game_btn_yes.clicked.connect(self.PressTrue)
        self.game_screen.game_btn_no.clicked.connect(self.PressFalse)

        self.timer_begin_second=1
        
####################### TIMER ###########################################        
        self.count = self.timer_begin_second
        self.start = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)
        self.game_screen.game_time_txt.setText(str(self.count))
    def showTime(self):
        if self.start==True:
            self.count -= 1
            if self.count < 0:
                self.start = False
                self.count = self.timer_begin_second
  
        if self.start==True:
            self.game_screen.game_time_txt.setText(str(self.count)) # label a sayac ı yaz
    
        if str(self.count) == "0":  # sayac 0 olursa english word yazdır
           
            self.game_screen.game_btn_yes.setEnabled(True)
            self.game_screen.game_btn_no.setEnabled(True)
            self.game_screen.game_txt_language.setText("English")
            
            if self.levelCounter >= 20:
                if len(self.wrong_list) != 0:
                    self.game_screen.game_txt_word.setText(f"{self.eng_y}")
            else:    
                self.EngWord()
                
            self.game_screen.verticalFrame.setStyleSheet("#verticalFrame{\n"
    "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(168, 255, 120, 255), stop:1 rgba(120, 255, 214, 255));\n"
    "\n"
    "border-radius: 25px;\n"
    "}") 
####################### TIMER ###########################################
    def level_up(self):
        user_dic={"username":self.user,"level":f"{self.level}"}
        with open(f"{self.user}.json", "w", encoding="utf-8") as file:
                    json.dump(user_dic, file)
                    #self.login_screen.login_btn_login.clicked.connect(self.go_main)
                    
            
    def PressTrue(self):
        self.game_screen.game_txt_language.setText("Dutch")
        self.game_screen.game_btn_yes.setEnabled(False)
        self.game_screen.game_btn_no.setEnabled(False)
        self.game_screen.verticalFrame.setStyleSheet("#verticalFrame{\n"
    "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.423, y2:0.570652, stop:0 rgba(0, 255, 255, 255), stop:1 rgba(170, 255, 255, 255));\n"
"\n"
    "border-radius: 25px;\n"
    "}")
        self.count = self.timer_begin_second+1
        self.start = True
        self.showTime()
        
        self.s += 1
        self.levelCounter+=1
        
        self.game_screen.game_txt_skor.setText(f"{self.wordCounter + 1}/{self.totalCounter}")
        self.wordCounter += 1
        self.game_screen.game_progres_bar.setProperty("value", f"{self.wordCounter}")
        
        if self.wordCounter == self.totalCounter:
        # if self.wordCounter == 1:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.messagebox=QtWidgets.QMessageBox()
            result=self.messagebox.question(self,'WARNINIG','Do you want to go next level ?',
                                        self.messagebox.Yes|self.messagebox.No)
            
            if result==QMessageBox.Yes:
                self.level+=1
                self.s = (self.level-1)*20
                self.s -= 1
                self.levelCounter=-1
                if self.wordCounter == self.totalCounter:
                    self.wordCounter=0
                    self.game_screen.game_txt_skor.setText(f"{self.wordCounter}/{self.totalCounter}")
                    self.game_screen.game_progres_bar.setProperty("value", 0)
                    self.wordCounter=-1
                self.wrong_list.clear()
                self.level_up()
                self.PressTrue()

            if result == QMessageBox.No:
                main_s = Main(self.user)
                widget.addWidget(main_s)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            
            self.wordCounter = 0
            self.totalCounter = 20
        
        # TODO Liste kontrolu ve silme
        
        if self.levelCounter >= self.totalCounter:
            
            if len(self.wrong_list) == 0:             
                self.levelCounter = 1
                self.totalCounter = 20
            else:
                self.s -= 1
                if self.levelCounter > 20:
                    self.wrong_list.pop(self.dutch_x)
                    
                for x,y in self.wrong_list.items():
                    self.dutch_x=x
                    self.eng_y=y
                    self.game_screen.game_txt_word.setText(f"{self.dutch_x}")
                    break

        else:        
            self.DutchWord()
               

    def PressFalse(self):
        self.game_screen.game_txt_language.setText("Dutch")
        # self.DutchWord()
        
        self.game_screen.game_btn_yes.setEnabled(False)
        self.game_screen.game_btn_no.setEnabled(False)
        self.game_screen.verticalFrame.setStyleSheet("#verticalFrame{\n"
    "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.423, y2:0.570652, stop:0 rgba(0, 255, 255, 255), stop:1 rgba(170, 255, 255, 255));\n"
"\n"
    "border-radius: 25px;\n"
    "}")
        self.count = self.timer_begin_second+1
        self.start = True
        self.showTime()
        self.s += 1
        self.levelCounter+=1
        
        if self.levelCounter >= 20:
            
            pass
            
        else:
            self.wrong_list.update({self.dataDutch : self.dataEng })
  

        
        if self.levelCounter >= self.totalCounter:
            if len(self.wrong_list) == 0:            
                self.levelCounter = 1
                self.totalCounter = 20
            else:
                self.s -= 1
                self.wrong_list.pop(self.dutch_x)
                self.wrong_list.update({self.dutch_x : self.eng_y})
                for x,y in self.wrong_list.items():
                    self.dutch_x=x
                    self.eng_y=y
                    self.game_screen.game_txt_word.setText(f"{self.dutch_x}")
                    break
                self.wrong_list.pop(self.dutch_x)
            self.wrong_list.update({self.dutch_x : self.eng_y})
                    
        else:        
            self.DutchWord()
  
    def go_main(self):
        main_s = Main(self.user)
        widget.addWidget(main_s)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def DutchWord(self):
        with open('data_w.json') as f:
            data = json.load(f)[self.s]
            self.dataDutch = data["Dutch"]
            self.game_screen.game_txt_word.setText(f"{self.dataDutch}")
           
    def EngWord(self):
        with open('data_w.json') as f:
            data = json.load(f)[self.s]
            self.dataEng = data["English"]
            self.game_screen.game_txt_word.setText(f"{self.dataEng}")        
       ######################################################################################################################################################################## 

app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setWindowTitle("FLASHCARDS")
icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
widget.setWindowIcon(icon)
widget.setFixedHeight(600)
widget.setFixedWidth(1000)
widget.show()
sys.exit(app.exec())