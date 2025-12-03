# L.M.S
# 📚 Library Management System

A Django-based web application that helps librarians manage books,
users, and transactions.\
It also includes a built-in **quiz module** for engaging readers or
testing knowledge.
I built this for my school (Lagos State Cooperative College) as partial require for the award of national diploma(ND)

this project solves problems regarding book management and engagement of student in the school library  

## 🚀 Features

-   **Book Management**\
    Add, update, delete, and search for books.
-   **Transaction Handling**\
    Track book borrowing and returns.
-   **User Management**\
    Manage student or member accounts.
-   **Quiz Module**\
    Create quizzes and view results.
-   **Admin Dashboard**\
    Clean interface using Django Admin.

## 🛠️ Tech Stack

-   **Backend:** Django (Python)\
-   **Database:** SQLite/PostgreSQL\
-   **Frontend:** HTML, CSS, Django Templates

## 📦 Installation & Setup

### 1. Clone the repository

``` bash
git clone <your-repo-url>
cd library-management-system
```

### 2. Create a virtual environment

``` bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

``` bash
venv\Scripts\activate
```

**Mac/Linux:**

``` bash
source venv/bin/activate
```

### 4. Install dependencies

``` bash
pip install -r requirements.txt
```

### 5. Run migrations

``` bash
python manage.py migrate
```

### 6. Start the server

``` bash
python manage.py runserver
```

App will be available at:\
**http://127.0.0.1:8000/**

## 📝 Future Improvements

-   Add book recommendation system\
-   Add user notifications for due dates\
-   Add API endpoints

## 📄 License

This project is open source and available under the MIT License (or
another license of your choice).
