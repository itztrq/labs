"""
Setup Verification Script
Run this to verify that the vulnerable application is properly configured
"""

import sys
import os
import sqlite3

def check_python_version():
    """Check if Python version is 3.8+"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking dependencies...")
    required = ['flask', 'werkzeug']
    all_installed = True
    
    for package in required:
        try:
            __import__(package)
            print(f"  ✅ {package} - Installed")
        except ImportError:
            print(f"  ❌ {package} - Not installed")
            all_installed = False
    
    return all_installed

def check_files():
    """Check if all required files exist"""
    print("\n🔍 Checking project files...")
    required_files = [
        'app.py',
        'init_db.py',
        'requirements.txt',
        'README.md',
        'static/style.css',
        'templates/base.html',
        'templates/home.html',
        'templates/greet.html',
        'templates/users.html',
        'templates/user_detail.html',
        'templates/upload.html',
        'templates/session.html',
        'templates/command.html',
        'templates/vulnerabilities.html',
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - Missing")
            all_exist = False
    
    return all_exist

def check_database():
    """Check if database exists and has data"""
    print("\n🔍 Checking database...")
    
    if not os.path.exists('users.db'):
        print("  ❌ Database not found - Run: python init_db.py")
        return False
    
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("  ❌ Users table not found")
            conn.close()
            return False
        
        # Check if there are users
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"  ✅ Database OK - {count} users found")
            conn.close()
            return True
        else:
            print("  ❌ No users in database")
            conn.close()
            return False
            
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        return False

def check_directories():
    """Check if required directories exist"""
    print("\n🔍 Checking directories...")
    required_dirs = ['static', 'templates', 'uploads']
    all_exist = True
    
    for dir in required_dirs:
        if os.path.exists(dir) and os.path.isdir(dir):
            print(f"  ✅ {dir}/")
        else:
            print(f"  ❌ {dir}/ - Missing")
            all_exist = False
            
    return all_exist

def check_vulnerabilities():
    """Check if vulnerabilities are present in code"""
    print("\n🔍 Checking vulnerabilities in code...")
    
    vulnerabilities_found = 0
    
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
        
        checks = [
            ("VULN #1", "'dev_secret_123'", "Hardcoded Secret Key"),
            ("VULN #2", "render_template_string(", "SSTI"),
            ("VULN #3", 'f"SELECT * FROM users WHERE id = {user_id}"', "SQL Injection"),
            ("VULN #4", "file.save(f'uploads/{file.filename}')", "Path Traversal"),
            ("VULN #5", "pickle.loads(", "Insecure Deserialization"),
            ("VULN #6", "os.popen(cmd)", "Command Injection"),
            ("VULN #7", "debug=True", "Debug Mode"),
        ]
        
        for vuln_id, pattern, name in checks:
            if pattern in content:
                print(f"  ✅ {vuln_id}: {name}")
                vulnerabilities_found += 1
            else:
                print(f"  ❌ {vuln_id}: {name} - Not found")
    
    return vulnerabilities_found == 7

def main():
    """Main verification function"""
    print("=" * 60)
    print("🔓 Vulnerable Web Application - Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version()),
        ("Dependencies", check_dependencies()),
        ("Project Files", check_files()),
        ("Directories", check_directories()),
        ("Database", check_database()),
        ("Vulnerabilities", check_vulnerabilities()),
    ]
    
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    for name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("\n" + "=" * 60)
    
    if passed == total:
        print("✅ All checks passed! The application is ready to use.")
        print("\nTo start the application, run:")
        print("  python app.py")
        print("\nThen open your browser to: http://127.0.0.1:5000")
    else:
        print(f"⚠️  {total - passed} check(s) failed.")
        print("\nPlease fix the issues above before running the application.")
        
        if not checks[1][1]:  # Dependencies failed
            print("\nTo install dependencies:")
            print("  pip install -r requirements.txt")
        
        if not checks[4][1]:  # Database failed
            print("\nTo initialize the database:")
            print("  python init_db.py")
    
    print("=" * 60)
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
