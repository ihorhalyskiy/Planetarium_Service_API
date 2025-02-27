# 🌌 Planetarium Service System 🌌

Welcome to the **Planetarium Service Api**! 
🚀 This project is designed to manage astronomy shows, planetarium domes, show sessions, reservations, and tickets. 
It’s built using **Django** and **Django REST Framework** to provide a robust backend API. 🌠

---

## 🌟 Features

- **Astronomy Shows Management** 🌠
  - Create, update, and manage astronomy shows.
  - Assign multiple show themes to each show.
  
- **Planetarium Domes Management** 🏛️
  - Manage planetarium domes with rows and seats.
  - Automatically calculate dome capacity.

- **Show Sessions Management** 🎥
  - Schedule show sessions for specific astronomy shows in planetarium domes.
  - Manage show times and availability.

- **Reservations & Tickets Management** 🎟️
  - Users can create reservations for show sessions.
  - Book specific seats in the planetarium dome.

- **User Authentication & Permissions** 🔐
  - Custom user model with email-based authentication.
  - Role-based permissions for admins and regular users.

---

## 🛠️ Technologies Used

- **Backend**: Django, Django REST Framework
- **Database**: SQLite local and PostgreSQL in docker 
- **Authentication**: JWT (JSON Web Tokens)
- **Permissions**: Custom permission classes for fine-grained access control.

---
## 📖 API Documentation
 ### The project provides interactive API documentation using drf-spectacular:

- Swagger: http://localhost:8000/api/schema/swagger/

- Redoc: http://localhost:8000/api/schema/redoc/

## 🚀 Getting Started

### Prerequisites

- Python 3.13
- Django 5+
- Django REST Framework 5.4
- Docker 28.0

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ihorhalyskiy/Planetarium_Service_API
   cd planetarium-service-api

2. Create a virtual environment and activate it:
    ```bash
   python -m venv venv
   source venv/bin/activate on Macbook
   venv\Scripts\activate  on Windows

3. Install requirements:
   ```bash
    pip install -r requirements.txt

4. Apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate

5. Create a superuser:
    ```bash
   python manage.py createsuperuser

6. Run the server:
    ```bash
   python manage.py runserver


## 📚 Models Overview

- **User Model** 📧
  - Email-based authentication.

- **Astronomy Show** 🌠
  - Title, description, and show themes.

- **Planetarium Dome** 🏛️
  - Name, rows, seats per row, and capacity.

---

## 🔒 Permissions

- **IsAdminOrReadOnly** 🔐
  - Only admins can modify data, but anyone can read.

- **IsOwnerOrAdmin** 🔐
  - Users can only modify their own reservations/tickets, or admins can modify any.

---

## 🌟 Example Use Cases

- **Create a New Astronomy Show** 🌠
  - Add a show with themes like "Black Holes" or "Galaxies".

- **Schedule a Show Session** 🎥
  - Assign the show to a planetarium dome at a specific time.

- **Manage Reservations** 📋
  - Admins can view all reservations, while users can only view their own.

- **Reservation Deletion** ⚠️
  - Reservations cannot be canceled 5 hours before the show.

---

## 🌠 Enjoy Exploring the Cosmos! 🌠
