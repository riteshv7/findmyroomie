<div align="center">
  <img src="https://img.icons8.com/color/94/home.png" width="80" height="80" />
  <h1>FindMyRoomie</h1>
  <p><i>A smart roommate matching and housing application built with Django</i></p>

  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
</div>

<br />

## 📖 Overview

**FindMyRoomie** is a dedicated web application designed to help university students and young professionals find compatible roommates and housing options. Built on a robust Django backend, it allows users to create detailed profiles, set preferences, and intelligently match with potential roommates based on lifestyle habits and budget constraints.

## ⚙️ Tech Stack

- **Backend Framework**: Django (Python 3.x)
- **Database**: SQLite (Development) / PostgreSQL (Production ready)
- **Frontend**: HTML5, CSS3, JavaScript (Django Templates)

## 🚀 Setup & Installation

To run this application on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/riteshv7/findmyroomie.git
cd findmyroomie
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations & Start Server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
The application will be accessible at `http://127.0.0.1:8000/`.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Check out the [issues page](https://github.com/riteshv7/findmyroomie/issues).
