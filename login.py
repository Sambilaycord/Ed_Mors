from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDateEdit
from PyQt6.QtGui import QPixmap, QColor, QPalette
import hashlib
import psycopg2 
from config import config

class Ui_MainWindow(object):
    def verify_password(self, username, password):
        try:
            connection = psycopg2.connect(**config())
            cursor = connection.cursor()

            cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result:
                hashed_password_from_db = result[0]
                
                # Check if the entered password matches the hashed password from the database
                salted_password = password + "Edmore"
                hashed_password_input = hashlib.sha256(salted_password.encode()).hexdigest()

                if hashed_password_input == hashed_password_from_db:
                    print("Password is correct!")
                else:
                    print("Incorrect password!")
            else:
                print("User not found.")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            if connection:
                connection.close()
            
            
    def loginUI(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1125, 680)
        MainWindow.setIconSize(QtCore.QSize(50, 50))
        MainWindow.setTabShape(QtWidgets.QTabWidget.TabShape.Triangular)
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.background_label = QLabel(self.centralwidget)
        self.background_label.setGeometry(0, 0, MainWindow.width(), MainWindow.height())
        pixmap = QPixmap("C:\\Users\\Krysss\\OneDrive\\Documents\\Programming\\SQL\\login2.png")
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.lower()

        username = QLineEdit(self.centralwidget)
        username.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Align text to the center
        username.setPlaceholderText("Enter Username...")
        username.setGeometry(QtCore.QRect(330, 300, 471, 41))
        username.show()
        
        password = QLineEdit(self.centralwidget)
        password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Align text to the center
        password.setPlaceholderText("Enter Password...")
        password.setGeometry(QtCore.QRect(330, 390, 471, 41))
        password.show()
        
        loginButton = QtWidgets.QPushButton(parent=self.centralwidget)
        loginButton.setGeometry(QtCore.QRect(504, 482, 121, 41))
        loginButton.setText("Log in")
        loginButton.setStyleSheet("background-color: rgb(148, 227, 255);")
        loginButton.clicked.connect(lambda: self.verify_password(username.text(), password.text()))
        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.loginUI(MainWindow)
    MainWindow.show()
    window = 0
    sys.exit(app.exec())