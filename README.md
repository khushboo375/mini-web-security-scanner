# Mini Web Security Scanner Dashboard

A full-stack web application that scans websites for common security vulnerabilities and displays the results in an interactive dashboard.

---

## Features

- Scan any URL for vulnerabilities  
- Detect:
  - Cross-Site Scripting (XSS)
  - SQL Injection (basic detection)
  - Missing Security Headers  
- Risk scoring system (Low, Medium, High)  
- Interactive dashboard built with React  
- Backend scanner engine using Python  

---

## Tech Stack

### Frontend
- React.js  
- CSS  

### Backend
- Python (Flask)  
- Requests library  

---

## Installation and Setup

### 1. Clone the repository, frontend and backend setup

```bash
git clone https://github.com/YOUR_USERNAME/mini-web-security-scanner.git
cd mini-web-security-scanner

#backend setup

cd backend
pip install -r requirements.txt
python app.py

#Frontend Setup

cd frontend
npm install
npm start