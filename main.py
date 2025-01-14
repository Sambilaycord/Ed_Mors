from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QAbstractItemView, QLabel, QLineEdit, QMessageBox
from PyQt6.QtGui import QPixmap
import psycopg2, AddDialog
    
class Ui_MainWindow(object):
    def build_connection(self, username, password):
        try:
            self.connection_params = {
                'dbname': 'Edmores',
                'user': username,
                'password': password,
                'host': 'localhost',
                'port': '5432',
            }
            self.connection = psycopg2.connect(**self.connection_params)
            return self.connection

        except Exception as e:
            print(f"Error building connection: {e}")
            return None
        
    def loadData(self):
        tabName = self.customerTabs.tabText(self.customerTabs.currentIndex())
        if tabName == "Customer" or tabName == "Reservation":
            self.loadDataCustomer()
        if tabName == "Delivery" or tabName == "Videoke":
            self.loadDataDelivery()
        if tabName == "Videoke" or tabName == "Maintenance":
            self.loadDataMaintenance()
        if tabName == "Accounts":
            self.loadDataAccounts()
        
    def loadDataCustomer(self):
        _translate = QtCore.QCoreApplication.translate
        try:
            self.connection = psycopg2.connect(**self.connection_params)  # Connect to the database
            with self.connection.cursor() as cursor:
                # Load data for the Customer tab
                self.setupTableWidget2UI()
                self.customerTabs.setTabText(self.customerTabs.indexOf(self.customerTab), _translate("MainWindow", "Customer"))
                self.customerTabs.setTabText(self.customerTabs.indexOf(self.reservationTab), _translate("MainWindow", "Reservation"))
                customer_query = "SELECT * FROM customer ORDER BY CustomerID"
                cursor.execute(customer_query)
                customer_result = cursor.fetchall()
                self.loadTableData(self.tableWidget, customer_result, cursor)

                # Load data for the Reservation tab
                reservation_query = "SELECT * FROM reservation ORDER BY ReservationID"
                cursor.execute(reservation_query)
                reservation_result = cursor.fetchall()
                self.loadTableData(self.tableWidget_2, reservation_result, cursor)


        except (Exception, psycopg2.Error) as error:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to fetch data: {error}")
        finally:
            self.closeConnection()
        
    def loadDataDelivery(self):
        try:
            _translate = QtCore.QCoreApplication.translate
            self.customerTabs.setTabText(self.customerTabs.indexOf(self.customerTab), _translate("MainWindow", "Delivery"))
            self.connection = psycopg2.connect(**self.connection_params)

            with self.connection.cursor() as cursor:
                # Load data for the Delivery tab
                self.customerTabs.removeTab(1)
                delivery_query = "SELECT * FROM delivery ORDER BY DeliveryDate"
                cursor.execute(delivery_query)
                delivery_result = cursor.fetchall()
                self.loadTableData(self.tableWidget, delivery_result, cursor)
                         
        except (Exception, psycopg2.Error) as error:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to fetch data: {error}")
            
    def loadDataMaintenance(self):
        try:
            _translate = QtCore.QCoreApplication.translate
            self.setupTableWidget2UI()
            self.customerTabs.setTabText(self.customerTabs.indexOf(self.customerTab), _translate("MainWindow", "Videoke"))
            self.customerTabs.setTabText(self.customerTabs.indexOf(self.reservationTab), _translate("MainWindow", "Maintenance"))
            self.connection = psycopg2.connect(**self.connection_params)  # Connect to the database
            with self.connection.cursor() as cursor:
                # Load data for the Videoke tab
                videoke_query = "SELECT * FROM videoke ORDER BY VideokeID"
                cursor.execute(videoke_query)
                videoke_result = cursor.fetchall()
                self.loadTableData(self.tableWidget, videoke_result, cursor)

                # Load data for the Maintenance tab
                maintenance_query = "SELECT * FROM maintenance ORDER BY MaintenanceID"
                cursor.execute(maintenance_query)
                maintenance_result = cursor.fetchall()
                self.loadTableData(self.tableWidget_2, maintenance_result, cursor)

        except (Exception, psycopg2.Error) as error:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to fetch data: {error}")
        finally:
            self.closeConnection()
        
    def loadDataAccounts(self):
        try:
            _translate = QtCore.QCoreApplication.translate

            # Check the authentication level before proceeding
            if self.authorizationLevel not in ["admin", "manager"]:
                return  # Exit if authorization level is not high enough

            self.customerTabs.setTabText(self.customerTabs.indexOf(self.customerTab), _translate("MainWindow", "Accounts"))
            self.connection = psycopg2.connect(**self.connection_params)

            with self.connection.cursor() as cursor:
                # Load data for the Delivery tab
                self.customerTabs.removeTab(1)
                user_query = "SELECT id, username, authorization_level FROM users ORDER BY id"
                cursor.execute(user_query)
                user_result = cursor.fetchall()
                self.loadTableData(self.tableWidget, user_result, cursor)

        except (Exception, psycopg2.Error) as error:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to fetch data: {error}")
        finally:
            self.closeConnection()
    
    def loadTableData(self, tableWidget, result, cursor):
        column_names = [desc[0] for desc in cursor.description]  # Fetch column names
        tableWidget.setRowCount(0)  # Clear existing rows
        tableWidget.setColumnCount(len(column_names))  # Set column count
        tableWidget.setHorizontalHeaderLabels(column_names)  # Set column headers
        
        stylesheet = "::section{Background-color:rgb(148, 227, 255);font-size: 12pt;}"
        tableWidget.horizontalHeader().setStyleSheet(stylesheet)
        
        for row_number, row_data in enumerate(result):
            tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        tableWidget.resizeColumnsToContents()
        tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    
    def search(self):
        try:
            current_tab_index = self.customerTabs.currentIndex()
            current_tab_name = self.customerTabs.tabText(current_tab_index)

            table_name = None
            identifier_column = None

            if current_tab_name == "Customer":
                table_name = "customer"
                identifier_column = "customerid"
            elif current_tab_name == "Reservation":
                table_name = "reservation"
                identifier_column = "reservationid"
            elif current_tab_name == "Delivery":
                table_name = "delivery"
                identifier_column = "deliveryid"
            elif current_tab_name == "Videoke":
                table_name = "videoke"
                identifier_column = "videokeid"
            elif current_tab_name == "Maintenance":
                table_name = "maintenance"
                identifier_column = "maintenanceid"
            elif current_tab_name == "Accounts":
                table_name = "users"
                identifier_column = "id"

            if table_name and identifier_column:
                tableWidget = self.tableWidget if current_tab_index == 0 else self.tableWidget_2

                # Prompt user for search term and column
                search_term, ok = QtWidgets.QInputDialog.getText(
                    None, "Search", f"Enter search term for {current_tab_name} table:")
                if not ok:
                    return  # User canceled

                column_name, ok = QtWidgets.QInputDialog.getText(
                    None, "Search Column", "Enter the name of the column to search:")
                if not ok:
                    return  # User canceled

                # Find column index
                header_labels = [tableWidget.horizontalHeaderItem(column_number).text()
                                for column_number in range(tableWidget.columnCount())]

                if column_name not in header_labels:
                    QMessageBox.warning(None, "Warning", f"Column '{column_name}' not found.")
                    return

                column_index = header_labels.index(column_name)

                # Highlight rows with matching search term
                for row_number in range(tableWidget.rowCount()):
                    item = tableWidget.item(row_number, column_index)
                    if item is not None and search_term.lower() in item.text().lower():
                        for column_number in range(tableWidget.columnCount()):
                            tableWidget.item(row_number, column_number).setBackground(QtGui.QColor(255, 255, 0))  # Yellow highlighting

                QMessageBox.information(None, "Search Result", f"Search completed for {search_term} in {column_name}.")

        except Exception as error:
            QMessageBox.critical(None, "Error", f"Error during search: {error}")
        
    def saveChanges(self):
        self.connection = psycopg2.connect(**self.connection_params)
        try:
            with self.connection.cursor() as cursor:
                current_tab_index = self.customerTabs.currentIndex()
                current_tab_name = self.customerTabs.tabText(current_tab_index)

                table_name = None
                identifier_column = None

                if current_tab_name == "Customer":
                    table_name = "customer"
                    identifier_column = "customerid"
                elif current_tab_name == "Reservation":
                    table_name = "reservation"
                    identifier_column = "reservationid"
                elif current_tab_name == "Delivery":
                    table_name = "delivery"
                    identifier_column = "deliveryid"
                elif current_tab_name == "Videoke":
                    table_name = "videoke"
                    identifier_column = "videokeid"
                elif current_tab_name == "Maintenance":
                    table_name = "maintenance"
                    identifier_column = "maintenanceid"
                elif current_tab_name == "Accounts":
                    table_name = "users"
                    identifier_column = "id"

                if table_name and identifier_column:
                    tableWidget = self.tableWidget if current_tab_index == 0 else self.tableWidget_2

                    for row_number in range(tableWidget.rowCount()):
                        row_data = []
                        for column_number in range(tableWidget.columnCount()):
                            item = tableWidget.item(row_number, column_number)
                            if item is not None:  # Check if the item exists
                                row_data.append(item.text())
                            else:
                                row_data.append(None)

                        # Construct UPDATE query based on row data and column names
                        header_labels = [tableWidget.horizontalHeaderItem(column_number).text()
                                        for column_number in range(tableWidget.columnCount())]

                        id_index = header_labels.index(identifier_column) if identifier_column in header_labels else None
                        if id_index is not None:
                            query = f"UPDATE {table_name} SET " + \
                                    ", ".join([f"{column_name} = %s" for column_name in header_labels if column_name != identifier_column]) + \
                                    f" WHERE {identifier_column} = %s"
                            cursor.execute(query, row_data[1:] + [row_data[id_index]])
                        else:
                            print("Header Labels:", header_labels)
                            QMessageBox.critical(None, "Error", f"{identifier_column} column not found!")

                    self.connection.commit()
                    QMessageBox.information(None, "Success", "Changes saved successfully!")

        except (Exception, psycopg2.Error) as error:
            QMessageBox.critical(None, "Error", f"Failed to save changes: {error}")
        finally:
            self.closeConnection()
    
    def deleteData(self):
        self.connection = psycopg2.connect(**self.connection_params)
        try:
            with self.connection.cursor() as cursor:
                current_tab_index = self.customerTabs.currentIndex()
                current_tab_name = self.customerTabs.tabText(current_tab_index)

                table_name = None
                identifier_column = None

                if current_tab_name == "Customer":
                    table_name = "customer"
                    identifier_column = "customerid"
                elif current_tab_name == "Reservation":
                    table_name = "reservation"
                    identifier_column = "reservationid"
                elif current_tab_name == "Delivery":
                    table_name = "delivery"
                    identifier_column = "deliveryid"
                elif current_tab_name == "Videoke":
                    table_name = "videoke"
                    identifier_column = "videokeid"
                elif current_tab_name == "Maintenance":
                    table_name = "maintenance"
                    identifier_column = "maintenanceid"
                elif current_tab_name == "Accounts":
                    table_name = "users"
                    identifier_column = "id"

                if table_name and identifier_column:
                    tableWidget = self.tableWidget if current_tab_index == 0 else self.tableWidget_2

                    selected_row = tableWidget.currentRow()

                    if selected_row == -1:
                        QMessageBox.warning(None, "Warning", "No row selected.")
                        return

                    primary_key_value = tableWidget.item(selected_row, 0).text()  # Assuming primary key is in the second column

                    query = f"DELETE FROM {table_name} WHERE {identifier_column} = %s"
                    cursor.execute(query, (primary_key_value,))
                    self.connection.commit()

                    QMessageBox.information(None, "Success", "Row deleted successfully!")

        except (Exception, psycopg2.DatabaseError) as error:
            QMessageBox.critical(None, "Error", f"Error deleting row: {error}")
        finally:
            self.closeConnection()
            
        self.loadData()

    def showAddDialog(self):
        tabIndex = self.customerTabs.currentIndex()
        tabName = self.customerTabs.tabText(self.customerTabs.currentIndex())
        
        if tabIndex == 0:
            if tabName == "Customer" and not self.authorizationLevel == 'deliverydept' and not self.authorizationLevel == 'maintenancedept':
                AddDialog.AddCustomerDialog().exec()
            elif tabName == "Delivery" and not self.authorizationLevel == 'customerdept' and not self.authorizationLevel == 'maintenancedept':
                AddDialog.AddDeliveryDialog().exec()
            elif tabName == "Videoke" and not self.authorizationLevel == 'deliverydept' and not self.authorizationLevel == 'customerdept':
                AddDialog.AddVideokeDialog().exec()
            elif tabName == "Accounts" and self.authorizationLevel == "admin":
                AddDialog.AddAccountDialog().exec()
            else:
                QMessageBox.critical(None, "Error", "Unauthorized access!")
  
        elif tabIndex == 1:
            if tabName == "Reservation" and not self.authorizationLevel == 'deliverydept' and not self.authorizationLevel == 'maintenancedept':
                AddDialog.AddReservationDialog().exec()
            elif tabName == "Maintenance" and not self.authorizationLevel == 'deliverydept' and not self.authorizationLevel == 'customerdept':
                AddDialog.AddMaintenanceDialog().exec()
    
    def verifyPassword(self, username, password):
        try:
            connection = self.build_connection(username, password)
            self.authorizationLevel = username
            
            if connection:
                if self.authorizationLevel == "admin" or self.authorizationLevel == "manager":  # Replace with your authorization level check
                    self.MainMenu()
                    self.highAccessUi()
                else:
                    self.MainMenu()
            else:
                QMessageBox.critical(None, "Error", "Incorrect Password or Username!")

        except Exception as e:
            print(f"Error: {e}")
            return False

        finally:
            if connection:
                connection.close()

    
    def hideUI(self):
        self.background.hide()
        self.logo.hide()
        self.customerTabs.hide()
        self.tableWidget.hide()
        self.loadButton.hide()
        self.addDataButton.hide()
        self.saveButton.hide()
        self.deleteButton.hide()
        self.searchButton.hide()
        self.label.hide()
        self.CustomerAndReservation.hide()
        self.Delivery.hide()
        self.Maintenance.hide()
        self.Accounts.hide()
        
    def MainMenu(self):
        self.username.hide()
        self.password.hide()
        self.loginBackground.hide()
        self.loginButton.hide()
        self.searchButton.show()
        
        self.background.show()
        self.logo.show()
        self.customerTabs.show()
        self.tableWidget.show()
        self.loadButton.show()
        self.addDataButton.show()
        self.saveButton.show()
        self.deleteButton.show()
        self.label.show()
        
        self.CustomerAndReservation.show()
        self.Delivery.show()
        self.Maintenance.show()
        
    def highAccessUi(self):
        self.Accounts.show()
        
    def setupUi(self, MainWindow):
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(148, 227, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1125, 680)
        MainWindow.setPalette(palette)
        MainWindow.setIconSize(QtCore.QSize(50, 50))
        MainWindow.setTabShape(QtWidgets.QTabWidget.TabShape.Triangular)
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.customerTabs = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.customerTabs.setGeometry(QtCore.QRect(270, 110, 831, 461))
        
        self.loginBackground = QLabel(self.centralwidget)
        self.loginBackground.setGeometry(0, 0, MainWindow.width(), MainWindow.height())
        pixmap = QPixmap("C:\\Users\\Krysss\\OneDrive\\Documents\\Programming\\SQL\\FINAL PIT\\Images\\login2.png")
        self.loginBackground.setPixmap(pixmap)
        self.loginBackground.setScaledContents(True)
        self.loginBackground.lower()

        self.username = QLineEdit(self.centralwidget)
        self.username.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Align text to the center
        self.username.setPlaceholderText("Enter Username...")
        self.username.setGeometry(QtCore.QRect(330, 300, 471, 41))
        self.username.show()
        
        self.password = QLineEdit(self.centralwidget)
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Align text to the center
        self.password.setPlaceholderText("Enter Password...")
        self.password.setGeometry(QtCore.QRect(330, 390, 471, 41))
        self.password.show()
        
        self.loginButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.loginButton.setGeometry(QtCore.QRect(504, 482, 121, 41))
        self.loginButton.setText("Log in")
        self.loginButton.setStyleSheet("background-color: rgb(148, 227, 255);")
        self.loginButton.clicked.connect(lambda: self.verifyPassword(self.username.text(), self.password.text()))
        
         # Create a QLabel for the background
        self.background = QLabel(self.centralwidget)
        self.background.setGeometry(0, 0, MainWindow.width(), MainWindow.height())
        pixmap = QPixmap("C:\\Users\\Krysss\\OneDrive\\Documents\\Programming\\SQL\\FINAL PIT\\Images\\BG.png")
        self.background.setPixmap(pixmap)
        self.background.setScaledContents(True)
        self.background.lower()
        
        self.logo = QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(460, 10, 481, 111))
        pixmap = QPixmap("C:\\Users\\Krysss\\OneDrive\\Documents\\Programming\\SQL\\FINAL PIT\\Images\\title.png")
        self.logo.setPixmap(pixmap)
        self.logo.setScaledContents(True)
        
        self.customerTabs.setPalette(palette)
        self.customerTabs.setFont(font)
        self.customerTabs.setAutoFillBackground(False)
        self.customerTabs.setTabShape(QtWidgets.QTabWidget.TabShape.Triangular)
        self.customerTabs.setIconSize(QtCore.QSize(50, 50))
        self.customerTabs.setObjectName("customerTabs")
        self.customerTab = QtWidgets.QWidget()
        self.customerTab.setObjectName("customerTab")
        self.customerTabs.addTab(self.customerTab, "")
        
        self.tableWidget = QtWidgets.QTableWidget(parent=self.customerTab)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 821, 431))
        self.tableWidget.setPalette(palette)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
       
        self.loadButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(970, 90, 121, 31))
        self.loadButton.setPalette(palette)
        self.loadButton.setStyleSheet("background-color: rgb(148, 227, 255);")
        self.loadButton.setObjectName("loadButton")
        self.loadButton.clicked.connect(self.loadData)
        self.loadButton.setFont(font)
        self.saveButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(970, 580, 121, 31))
        
        self.saveButton.setPalette(palette)
        self.saveButton.setFont(font)
        self.saveButton.setStyleSheet("background-color: rgb(148, 227, 255);")
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(self.saveChanges)
        
        self.deleteButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(710, 580, 121, 31))
        self.deleteButton.setPalette(palette)
        self.deleteButton.setFont(font)
        self.deleteButton.setStyleSheet("background-color: rgb(148, 227, 255);")
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.clicked.connect(self.deleteData)
        
        self.addDataButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.addDataButton.setGeometry(QtCore.QRect(840, 580, 121, 31))
        self.addDataButton.setPalette(palette)
        self.addDataButton.setFont(font)
        self.addDataButton.setStyleSheet("background-color: rgb(148, 227, 255);")
        self.addDataButton.setObjectName("addDataButton")
        self.addDataButton.clicked.connect(self.showAddDialog)
        
        self.searchButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(20, 530, 241, 31))
        self.searchButton.setPalette(palette)
        self.searchButton.setFont(font)
        self.searchButton.setStyleSheet("background-color: rgb(148, 227, 255);")
        self.searchButton.setObjectName("addDataButton")
        self.searchButton.clicked.connect(self.search)
        
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(610, 150, 47, 13))
        self.label.setPalette(palette)
        self.label.setText("")
        self.label.setObjectName("label")
        
        self.CustomerAndReservation = QtWidgets.QPushButton(parent=self.centralwidget)
        self.CustomerAndReservation.setGeometry(QtCore.QRect(20, 130, 241, 51))
        self.CustomerAndReservation.setPalette(palette)
        self.CustomerAndReservation.setFont(font)
        self.CustomerAndReservation.setStyleSheet("background-color: rgb(148, 227, 255);")
        self.CustomerAndReservation.setObjectName("CustomerAndReservation")
        
        self.Delivery = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Delivery.setGeometry(QtCore.QRect(20, 190, 241, 51))
        self.Delivery.setPalette(palette)
        self.Delivery.setFont(font)
        self.Delivery.setStyleSheet("background-color: rgb(148, 227, 255);")
        self.Delivery.setObjectName("Delivery")
        
        self.Maintenance = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Maintenance.setGeometry(QtCore.QRect(20, 250, 241, 51))
        self.Maintenance.setPalette(palette)
        self.Maintenance.setFont(font)
        self.Maintenance.setStyleSheet("background-color: rgb(148, 227, 255);")
        self.Maintenance.setObjectName("Maintenance")
        
        self.Accounts = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Accounts.setGeometry(QtCore.QRect(20, 310, 241, 51))
        self.Accounts.setPalette(palette)
        self.Accounts.setFont(font)
        self.Accounts.setStyleSheet("background-color: rgb(148, 227, 255);")
        self.Accounts.setObjectName("Accounts")
        
        self.Delivery.clicked.connect(self.loadDataDelivery)
        self.CustomerAndReservation.clicked.connect(self.loadDataCustomer)
        self.Maintenance.clicked.connect(self.loadDataMaintenance)
        self.Accounts.clicked.connect(self.loadDataAccounts)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1125, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.retranslateUi(MainWindow)
        self.customerTabs.setCurrentIndex(0)
        
        self.hideUI()
    
    def setupTableWidget2UI(self):
        if self.customerTabs.count() < 2:
            self.reservationTab = QtWidgets.QWidget()
            self.reservationTab.setObjectName("reservationTab")
            self.tableWidget_2 = QtWidgets.QTableWidget(parent=self.reservationTab)
            self.tableWidget_2.setGeometry(QtCore.QRect(0, 0, 821, 431))
            font = QtGui.QFont()
            font.setFamily("Segoe UI")
            font.setPointSize(11)
            self.tableWidget_2.setFont(font)
            self.tableWidget_2.setObjectName("tableWidget_2")
            self.tableWidget_2.setColumnCount(0)
            self.tableWidget_2.setRowCount(0)
            self.customerTabs.addTab(self.reservationTab, "")
        else:
            return
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Edmore's Videoke Rental"))
        self.loadButton.setText(_translate("MainWindow", "Load Data"))
        self.saveButton.setText(_translate("MainWindow", "Save Changes"))
        self.deleteButton.setText(_translate("MainWindow", "Delete"))
        self.addDataButton.setText(_translate("MainWindow", "Add Data"))
        self.searchButton.setText(_translate("MainWindow", "Search"))
        self.CustomerAndReservation.setText(_translate("MainWindow", "Customer and Reservation"))
        self.Delivery.setText(_translate("MainWindow", "Delivery"))
        self.Maintenance.setText(_translate("MainWindow", "Equipment and Maintenance"))
        self.Accounts.setText(_translate("MainWindow", "Accounts"))
    
    def closeConnection(self):
        if self.connection:
            self.connection.close()
    
    def __del__(self):
        self.closeConnection()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    window = 0
    sys.exit(app.exec())