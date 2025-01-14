from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDateEdit
import psycopg2 
from config import config

class AddCustomerDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Customer")
        layout = QVBoxLayout()

        self.customer_name_label = QLabel("Customer Name:")
        self.customer_name_edit = QLineEdit()

        self.contact_number_label = QLabel("Contact Number:")
        self.contact_number_edit = QLineEdit()

        self.house_number_label = QLabel("House Number:")
        self.house_number_edit = QLineEdit()

        self.street_label = QLabel("Street:")
        self.street_edit = QLineEdit()

        self.barangay_label = QLabel("Barangay:")
        self.barangay_edit = QLineEdit()

        self.city_label = QLabel("City:")
        self.city_edit = QLineEdit()

        self.add_button = QPushButton("Add Customer")
        self.add_button.clicked.connect(self.addCustomer)

        layout.addWidget(self.customer_name_label)
        layout.addWidget(self.customer_name_edit)
        layout.addWidget(self.contact_number_label)
        layout.addWidget(self.contact_number_edit)
        layout.addWidget(self.house_number_label)
        layout.addWidget(self.house_number_edit)
        layout.addWidget(self.street_label)
        layout.addWidget(self.street_edit)
        layout.addWidget(self.barangay_label)
        layout.addWidget(self.barangay_edit)
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_edit)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def addCustomer(self):
        # Retrieve data from the input fields
        customer_name = self.customer_name_edit.text()
        contact_number = self.contact_number_edit.text()
        house_number = self.house_number_edit.text()
        street = self.street_edit.text()
        barangay = self.barangay_edit.text()
        city = self.city_edit.text()

        try:
            # Connect to the database
            connection = psycopg2.connect(**config())
            with connection.cursor() as cursor:
                # Insert new customer data into the customer table
                query = "INSERT INTO customer (CustomerName, ContactNumber, HouseNumber, Street, Barangay, City) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (customer_name, contact_number, house_number, street, barangay, city))
                connection.commit()
            QMessageBox.information(None, "Success", "Customer added successfully!")
        except (Exception, psycopg2.Error) as error:
            QMessageBox.critical(None, "Error", f"Failed to add customer: {error}")
        finally:
            if connection:
                connection.close()

class AddReservationDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Reservation")
        layout = QVBoxLayout()

        self.reservation_date_label = QLabel("Reservation Date:")
        self.reservation_date_edit = QDateEdit()  # Use a date picker widget for better usability

        self.return_date_label = QLabel("Return Date:")
        self.return_date_edit = QDateEdit()  # Use a date picker widget for better usability

        self.customer_id_label = QLabel("Customer ID:")
        self.customer_id_edit = QLineEdit()  # Consider a dropdown for selecting from existing customers

        self.videoke_id_label = QLabel("Videoke ID:")
        self.videoke_id_edit = QLineEdit()  # Consider a dropdown for selecting available units

        self.add_button = QPushButton("Add Reservation")
        self.add_button.clicked.connect(self.addReservation)

        layout.addWidget(self.reservation_date_label)
        layout.addWidget(self.reservation_date_edit)
        layout.addWidget(self.return_date_label)
        layout.addWidget(self.return_date_edit)
        layout.addWidget(self.customer_id_label)
        layout.addWidget(self.customer_id_edit)
        layout.addWidget(self.videoke_id_label)
        layout.addWidget(self.videoke_id_edit)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

        self.connection = None  # Initialize connection at class level

    def addReservation(self):
        # Retrieve data from the input fields
        reservation_date = self.reservation_date_edit.text()
        return_date = self.return_date_edit.text()
        customer_id = self.customer_id_edit.text()
        videoke_id = self.videoke_id_edit.text()

        try:
            if self.connection is None:  # Establish connection if not already existing
                self.connection = psycopg2.connect(**config())

            with self.connection.cursor() as cursor:
                # Insert new reservation data into the reservation table
                query = "INSERT INTO reservation (ReservationDate, ReturnDate, CustomerID, VideokeID) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (reservation_date, return_date, customer_id, videoke_id))
                self.connection.commit()
            QMessageBox.information(None, "Success", "Reservation added successfully!")
        except (Exception, psycopg2.Error) as error:
            QMessageBox.critical(None, "Error", f"Failed to add reservation: {error}")
        finally:
            if self.connection:
                self.connection.close()
        
class AddVideokeDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Videoke")
        layout = QVBoxLayout()

        self.model_label = QLabel("Model:")
        self.model_edit = QLineEdit()

        self.condition_label = QLabel("Condition:")
        self.condition_edit = QLineEdit()

        self.status_label = QLabel("Status:")
        self.status_edit = QLineEdit()

        self.add_button = QPushButton("Add Videoke")
        self.add_button.clicked.connect(self.addVideoke)

        layout.addWidget(self.model_label)
        layout.addWidget(self.model_edit)
        layout.addWidget(self.condition_label)
        layout.addWidget(self.condition_edit)
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_edit)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def addVideoke(self):
        # Retrieve data from the input fields
        model = self.model_edit.text()
        condition = self.condition_edit.text()
        status = self.status_edit.text()

        try:
            # Connect to the database
            connection = psycopg2.connect(**config())  # Assuming config() provides database credentials
            with connection.cursor() as cursor:

                # Insert new videoke data into the Videoke table
                query = "INSERT INTO Videoke (Model, Condition, Status) VALUES (%s, %s, %s)"
                cursor.execute(query, (model, condition, status))
                connection.commit()
            QMessageBox.information(None, "Success", "Videoke added successfully!")
        except (Exception, psycopg2.Error) as error:
            QMessageBox.critical(None, "Error", f"Failed to add videoke: {error}")
        finally:
            if connection:
                connection.close()

class AddDeliveryDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Delivery")
        layout = QVBoxLayout()

        self.reservation_id_label = QLabel("Reservation ID:")
        self.reservation_id_edit = QLineEdit()

        self.delivery_address_label = QLabel("Delivery Address:")
        self.delivery_address_edit = QLineEdit()

        self.delivery_personnel_label = QLabel("Delivery Personnel:")
        self.delivery_personnel_edit = QLineEdit()

        self.delivery_status_label = QLabel("Delivery Status:")
        self.delivery_status_edit = QLineEdit()

        self.add_button = QPushButton("Add Delivery")
        self.add_button.clicked.connect(self.addDelivery)

        layout.addWidget(self.reservation_id_label)
        layout.addWidget(self.reservation_id_edit)
        layout.addWidget(self.delivery_address_label)
        layout.addWidget(self.delivery_address_edit)
        layout.addWidget(self.delivery_personnel_label)
        layout.addWidget(self.delivery_personnel_edit)
        layout.addWidget(self.delivery_status_label)
        layout.addWidget(self.delivery_status_edit)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def addDelivery(self):
        # Retrieve data from the input fields
        reservation_id = self.reservation_id_edit.text()
        delivery_address = self.delivery_address_edit.text()
        delivery_personnel = self.delivery_personnel_edit.text()
        delivery_status = self.delivery_status_edit.text()

        try:
            # Connect to the database
            connection = psycopg2.connect(**config())  # Assuming config() provides database credentials
            with connection.cursor() as cursor:
                # Insert new delivery data into the Delivery table
                query = "INSERT INTO Delivery (ReservationID, DeliveryAddress, DeliveryPersonnel, DeliveryStatus) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (reservation_id, delivery_address, delivery_personnel, delivery_status))
                connection.commit()
            QMessageBox.information(None, "Success", "Delivery added successfully!")
        except (Exception, psycopg2.Error) as error:
            QMessageBox.critical(None, "Error", f"Failed to add delivery: {error}")
        finally:
            if connection:
                connection.close()

class AddMaintenanceDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Maintenance")
        layout = QVBoxLayout()

        self.videoke_id_label = QLabel("Videoke ID:")
        self.videoke_id_edit = QLineEdit()

        self.issues_label = QLabel("Issues:")
        self.issues_edit = QLineEdit()

        self.date_reported_label = QLabel("Date Reported:")
        self.date_reported_edit = QDateEdit()  # Use QDateEdit for date input

        self.date_maintained_label = QLabel("Date Maintained:")
        self.date_maintained_edit = QDateEdit()  # Use QDateEdit for date input

        self.notes_label = QLabel("Notes:")
        self.notes_edit = QLineEdit()

        self.add_button = QPushButton("Add Maintenance")
        self.add_button.clicked.connect(self.addMaintenance)

        layout.addWidget(self.videoke_id_label)
        layout.addWidget(self.videoke_id_edit)
        layout.addWidget(self.issues_label)
        layout.addWidget(self.issues_edit)
        layout.addWidget(self.date_reported_label)
        layout.addWidget(self.date_reported_edit)
        layout.addWidget(self.date_maintained_label)
        layout.addWidget(self.date_maintained_edit)
        layout.addWidget(self.notes_label)
        layout.addWidget(self.notes_edit)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def addMaintenance(self):
        # Retrieve data from the input fields
        videoke_id = self.videoke_id_edit.text()
        issues = self.issues_edit.text()
        date_reported = self.date_reported_edit.date().toString("yyyy-MM-dd")  # Format date as string
        date_maintained = self.date_maintained_edit.date().toString("yyyy-MM-dd")  # Format date as string
        notes = self.notes_edit.text()

        try:
            # Connect to the database
            connection = psycopg2.connect(**config())  # Assuming config() provides database credentials
            with connection.cursor() as cursor:
                # Insert new maintenance data into the Maintenance table
                query = "INSERT INTO Maintenance (VideokeID, Issues, DateReported, DateMaintained, Notes) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (videoke_id, issues, date_reported, date_maintained, notes))
                connection.commit()
            QMessageBox.information(None, "Success", "Maintenance added successfully!")
        except (Exception, psycopg2.Error) as error:
            QMessageBox.critical(None, "Error", f"Failed to add maintenance: {error}")
        finally:
            if connection:
                connection.close()


class AddAccountDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Accoount")
        layout = QVBoxLayout()

        self.user_label = QLabel("Username:")
        self.user_edit = QLineEdit()

        self.password_label = QLabel("Passowrd:")
        self.password_edit = QLineEdit()

        self.authorization_label = QLabel("Authorization Level:")
        self.authorization_edit = QLineEdit()

        self.add_button = QPushButton("Add Account")
        self.add_button.clicked.connect(self.addAccount)

        layout.addWidget(self.user_label)
        layout.addWidget(self.user_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.authorization_label)
        layout.addWidget(self.authorization_edit)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def addAccount(self):
        # Retrieve data from the input fields
        username = self.user_edit.text()
        condition = self.password_edit.text()
        authorization = self.authorization_edit.text()

        try:
            # Connect to the database
            connection = psycopg2.connect(**config())  # Assuming config() provides database credentials
            with connection.cursor() as cursor:

                # Insert new videoke data into the Videoke table
                query = "INSERT INTO users (username, password, authorization_level) VALUES (%s, %s, %s)"
                cursor.execute(query, (username, condition, authorization))
                connection.commit()
            QMessageBox.information(None, "Success", "Account added successfully!")
        except (Exception, psycopg2.Error) as error:
            QMessageBox.critical(None, "Error", f"Failed to add Account: {error}")
        finally:
            if connection:
                connection.close()