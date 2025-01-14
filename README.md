# Ed Mor's Videoke Rental Database Project
## Overview
This project aims to develop a database system to manage the operations of Ed Mor’s Videoke Rental, a small business in Upper Nazareth, Cagayan de Oro City. The system addresses inefficiencies caused by manual recordkeeping, providing a digital solution for tracking customer reservations, delivery schedules, machine maintenance, and rental payments.

## Project Objectives
- Replace manual recordkeeping with a **SQL-based digital database**.
- Automate tracking of rental details, delivery schedules, and maintenance.
- Ensure **data consistency** across customer reservations and delivery schedules.
- Calculate **rental fees** based on duration, with a maximum of two days.
## Technologies Used
- **Database**: PostgreSQL
- **Programming Language**: Python
- **UI Framework**: PyQt6
- **Database Connection**: Psycopg2
## Key Features
- Authentication: User access levels based on roles.
- CRUD Operations: Add, view, edit, and delete data across tables (Customers, Reservations, Deliveries, Videoke Machines, Maintenance).
- Search Functionality: Locate specific records in the database.
- Data Refresh: Sync changes made in the database with the application.
## Scope and Limitations
- Tracks up to 8 karaoke machines with rental fees of ₱1,800 for the first day and ₱500 for each additional day (up to 2 days max).
- Excludes tracking of monetary transactions or down payments.
- Maintenance schedules are only tracked for reported issues.
## Team Members
- Arao, Hugh Humphrey S.
- Bacalso, Krystal Heart M.
- Bañas, James B.
- Vallecera, Kirk Patrick T.
## Acknowledgment
- This project is submitted in partial fulfillment of the requirements for **CS214 Fundamentals of Database Systems** at the **University of Science and Technology of Southern Philippines**, January 2024.
