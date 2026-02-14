# 🔓 Vulnerable Web Application - Code Review Lab

![Security Training](https://img.shields.io/badge/Purpose-Educational-yellow)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![License](https://img.shields.io/badge/License-Educational-red)

> ⚠️ **WARNING**: This application contains intentional security vulnerabilities for educational purposes only. **NEVER** deploy this application to production or expose it to the internet!

## 📋 Overview

This is a deliberately vulnerable web application designed for security training and code review practice. It demonstrates **7 critical security vulnerabilities** commonly found in web applications, providing hands-on experience in identifying and understanding security flaws.

## 🎯 Learning Objectives

By exploring this lab, you will learn to identify and understand:

1. **Hardcoded Secrets** - Exposure of sensitive configuration in source code
2. **Server-Side Template Injection (SSTI)** - Arbitrary code execution through template engines
3. **SQL Injection** - Database manipulation through unsanitized queries
4. **Path Traversal / Unrestricted File Upload** - Unauthorized file system access
5. **Insecure Deserialization** - Code execution through pickle vulnerabilities
6. **Command Injection** - Operating system command execution
7. **Debug Mode in Production** - Information disclosure and interactive debugging

## 🏗️ Project Structure

```
CodeReviewLab/
├── app.py                  # Main Flask application (contains all vulnerabilities)
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
├── README.md             # This file
├── users.db              # SQLite database (created after init)
├── static/
│   └── style.css         # Modern CSS styling
├── templates/
│   ├── base.html         # Base template
│   ├── home.html         # Homepage
│   ├── greet.html        # Greeting form (SSTI)
│   ├── users.html        # User list (SQL Injection)
│   ├── user_detail.html  # User details page
│   ├── upload.html       # File upload (Path Traversal)
│   ├── session.html      # Session manager (Deserialization)
│   ├── command.html      # Command execution (Command Injection)
│   ├── vulnerabilities.html  # Vulnerability documentation
│   ├── 404.html          # Not found page
│   └── 500.html          # Server error page
└── uploads/              # Upload directory
    └── .gitkeep
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation & Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd s:\cb\lab\CodeReviewLab
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   ```bash
   python init_db.py
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:5000
   ```

## 🔍 Vulnerability Details

### VULN #1: Hardcoded Secret Key
**Location:** `app.py` line 17  
**Severity:** HIGH  
**Description:** Flask secret key is hardcoded in source code  
**Code:**
```python
app.config['SECRET_KEY'] = 'dev_secret_123'  # VULN #1
```
**Impact:** Session forgery, unauthorized access  
**Remediation:** Use environment variables or secure secret management

---

### VULN #2: Server-Side Template Injection (SSTI)
**Location:** `/greet` endpoint  
**Severity:** CRITICAL  
**Description:** User input directly embedded in template without escaping  
**Code:**
```python
return render_template_string(f'<h1>Hello {name}!</h1>')  # VULN #2
```
**Test:**
- Try: `http://127.0.0.1:5000/greet?name={{7*7}}`
- Try: `http://127.0.0.1:5000/greet?name={{config.items()}}`

**Impact:** Remote code execution, full system compromise  
**Remediation:** Use `render_template()` with proper auto-escaping

---

### VULN #3: SQL Injection
**Location:** `/user/<user_id>` endpoint  
**Severity:** CRITICAL  
**Description:** SQL queries built with string interpolation  
**Code:**
```python
query = f"SELECT * FROM users WHERE id = {user_id}"  # VULN #3
```
**Test:**
- Try: `http://127.0.0.1:5000/user/1 OR 1=1`
- Try: `http://127.0.0.1:5000/user/1 UNION SELECT 1,2,3,4,5,6`

**Impact:** Data breach, unauthorized access, data manipulation  
**Remediation:** Use parameterized queries or ORM

---

### VULN #4: Path Traversal / Unrestricted File Upload
**Location:** `/upload` endpoint  
**Severity:** HIGH  
**Description:** No validation of filenames or file types  
**Code:**
```python
file.save(f'uploads/{file.filename}')  # VULN #4
```
**Test:**
- Upload file with name: `../../../test.txt`
- Upload malicious file: `shell.php`, `malware.exe`

**Impact:** Arbitrary file write, code execution, system compromise  
**Remediation:** Validate filenames, restrict file types, use secure paths

---

### VULN #5: Insecure Deserialization
**Location:** `/session/load` endpoint  
**Severity:** CRITICAL  
**Description:** Pickle deserialization of user-controlled data  
**Code:**
```python
data = pickle.loads(base64.b64decode(data_cookie))  # VULN #5
```
**Impact:** Remote code execution through crafted pickle payloads  
**Remediation:** Use JSON or other safe serialization formats

---

### VULN #6: Command Injection
**Location:** `/command` endpoint  
**Severity:** CRITICAL  
**Description:** Direct execution of user input as system commands  
**Code:**
```python
output = os.popen(cmd).read()  # VULN #6
```
**Test:**
- Try: `dir & whoami`
- Try: `ipconfig`

**Impact:** Full system compromise, data exfiltration  
**Remediation:** Never execute user input; use safer alternatives

---

### VULN #7: Debug Mode in Production
**Location:** Application startup  
**Severity:** HIGH  
**Description:** Flask debug mode enabled  
**Code:**
```python
app.run(debug=True)  # VULN #7
```
**Impact:** Source code disclosure, interactive debugger access  
**Remediation:** Always set `debug=False` in production

## 🎓 Training Exercises

1. **Explore each vulnerability** by navigating through the application
2. **Attempt to exploit** each vulnerability using the hints provided
3. **Review the source code** to understand how vulnerabilities occur
4. **Practice remediation** by creating a secure version of the application
5. **Use security tools** like OWASP ZAP or Burp Suite to scan the application

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Sample Credentials
- **Username:** admin | **Password:** admin123
- **Username:** john_doe | **Password:** password123

## 🛡️ Security Best Practices

This application demonstrates what **NOT** to do. Secure alternatives include:

1. ✅ Store secrets in environment variables or secret managers
2. ✅ Use parameterized queries or ORM for database operations
3. ✅ Validate and sanitize all user input
4. ✅ Use allow-lists for file uploads with content validation
5. ✅ Use safe serialization formats (JSON, not pickle)
6. ✅ Never execute user input as system commands
7. ✅ Disable debug mode in production
8. ✅ Implement proper authentication and authorization
9. ✅ Use HTTPS for all communications
10. ✅ Keep dependencies updated and scan for vulnerabilities

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Flask Security Considerations](https://flask.palletsprojects.com/en/latest/security/)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)

## ⚠️ Disclaimer

This application is designed exclusively for educational and training purposes. It contains deliberate security vulnerabilities and should **NEVER** be:

- Deployed to production environments
- Exposed to the internet
- Used with real user data
- Used for malicious purposes

The creators of this lab are not responsible for any misuse of this code.

## 📝 License

This project is for educational purposes only. Use at your own risk.

## 🤝 Contributing

This is an educational project. If you find additional vulnerabilities or have suggestions for improvement, feel free to document them for learning purposes.

## 📧 Contact

This lab was created for security training and code review practice.

---

**Remember:** The best way to learn security is to understand how things can go wrong! 🎯
