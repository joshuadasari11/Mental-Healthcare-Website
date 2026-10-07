# Smartphone & Internet Addiction Awareness Website

> **DTSI First Year Project**  
> Developed by **KLE Tech Students**

An interactive web application designed to create awareness about smartphone and internet addiction among children and young adults, provide actionable solutions for digital balance, and manage community inquiries and newsletter subscriptions via an administrative dashboard.

---

## 📌 Project Features

### 🌐 Public Website
* **Home Page (`index.html`)**: Overview of screen time risks, causes of phone addiction (poor sleep, loneliness, slow development), and key solutions.
* **About (`about.html`)**: Information about the project mission and KLE Tech student initiatives.
* **Resources (`service.html`)**: Detailed resources for parents, educators, and children.
* **Solution (`why.html`)**: Actionable boundaries, study space optimizations, and digital wellness guidelines.
* **Team (`team.html`)**: Profiles of team members and project mentors.
* **Contact & Newsletter Forms**: Forms allowing users to submit inquiries or subscribe to newsletter updates.

### 🔐 Admin Dashboard (`admin.html`)
* **Glassmorphism UI**: Modern aesthetic dashboard with real-time stats and smooth animations.
* **Inquiry Management**: View details of submitted contact inquiries and delete processed messages.
* **Subscriber Management**: View and manage the newsletter mailing list.
* **Role & User Management**: Multi-user admin support (capped at 2 administrators) with session-based authentication.

---

## 🛠️ Tech Stack

* **Backend**: Python 3, Flask, Werkzeug (Password Hashing & Session Management)
* **Database**: SQLite3 (`database.db`)
* **Frontend**: HTML5, CSS3, JavaScript (jQuery, Bootstrap, Owl Carousel, Font Awesome)

---

## 📂 Project Structure

```text
├── app.py              # Main Flask server application & API routes
├── init_db.py          # Database initialization & table creation script
├── database.db         # SQLite database (auto-created on run)
├── requirements.txt    # Python dependency specifications
├── index.html          # Homepage
├── about.html          # About page
├── service.html        # Resources & services page
├── why.html            # Solutions & advice page
├── team.html           # Project team page
├── login.html          # Admin login & registration page
├── admin.html          # Protected Admin Dashboard
├── css/                # Custom CSS stylesheets & Bootstrap
├── js/                 # JavaScript dependencies & custom scripts
├── images/             # Media and image assets
└── fonts/              # Custom font packages
```

---

## 🗄️ Database Schema

The SQLite database (`database.db`) consists of three main tables:

1. **`users`**: Stores administrator login details.
   - `id`, `username`, `password_hash`, `role`, `created_at`
2. **`contacts`**: Stores inquiries submitted via the website contact form.
   - `id`, `name`, `email`, `mobile_number`, `address`, `message`, `created_at`
3. **`subscribers`**: Stores emails subscribed to the newsletter.
   - `id`, `email`, `created_at`

---

## 🚀 Getting Started & How to Run

### Prerequisites
Make sure you have **Python 3.x** installed on your system.

### 1. Install Dependencies
Open your terminal in the project root directory and run:
```powershell
pip install -r requirements.txt
```

### 2. Start the Server
Run the Flask application:
```powershell
python app.py
```
*(The server will automatically run `init_db.py` to create the database and seed the default admin account if it does not already exist).*

### 3. Open in Browser
* **Main Website**: [http://localhost:5000](http://localhost:5000)
* **Admin Login**: [http://localhost:5000/login.html](http://localhost:5000/login.html)

---

## 🔑 Default Admin Credentials & Password Reset

### Default Credentials
* **Username**: `admin`
* **Password**: `admin123`

### Reset Admin Password
If you ever forget the admin password, run this command in your terminal inside the project directory:

```powershell
python -c "import sqlite3; from werkzeug.security import generate_password_hash; conn=sqlite3.connect('database.db'); conn.execute('UPDATE users SET password_hash = ? WHERE username = ?', (generate_password_hash('YOUR_NEW_PASSWORD'), 'admin')); conn.commit(); print('Password updated successfully!')"
```
*(Replace `YOUR_NEW_PASSWORD` with your desired password).*

---

## 👥 Project Team

* **Mentor**: Abhishek Kamadollishettar
* **Team Head**: Janaki M.
* **Assistant Team Head**: Shifa S.
* **Founder**: Varsha
* **Marketing Head**: Joshua D.
* **Team Member**: Sumanth
