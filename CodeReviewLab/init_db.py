"""
Database Initialization Script
Creates SQLite database with sample data for the vulnerable web application
"""

import sqlite3
import os


def init_database():
    """Initialize the database with tables and sample data"""
    
    # Remove existing database if it exists
    if os.path.exists('users.db'):
        os.remove('users.db')
        print("Removed existing database")
    
    # Create new database connection
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample users
    sample_users = [
        ('admin', 'admin@vulnerable-app.local', 'admin123', 'administrator'),
        ('john_doe', 'john@example.com', 'password123', 'user'),
        ('jane_smith', 'jane@example.com', 'qwerty456', 'user'),
        ('bob_wilson', 'bob@example.com', 'letmein789', 'user'),
        ('alice_jones', 'alice@example.com', 'welcome2024', 'moderator'),
        ('charlie_brown', 'charlie@example.com', 'passw0rd!', 'user'),
        ('david_miller', 'david@example.com', '123456abc', 'user'),
        ('emma_davis', 'emma@example.com', 'password!', 'user'),
    ]
    
    cursor.executemany(
        'INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
        sample_users
    )
    
    # Create sessions table for demonstration
    cursor.execute('''
        CREATE TABLE sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database initialized successfully!")
    print(f"Created {len(sample_users)} sample users")
    print("\nSample credentials:")
    print("  Username: admin | Password: admin123")
    print("  Username: john_doe | Password: password123")


if __name__ == '__main__':
    init_database()
