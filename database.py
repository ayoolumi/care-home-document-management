"""
Care Home Document Management System - Database Module
Created: July 2023
Author: Ayoolumi Melehon
"""

import sqlite3
import os
from datetime import datetime, timedelta
import json

DATABASE_PATH = "documents.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT,
        role TEXT DEFAULT 'staff',
        department TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        is_active INTEGER DEFAULT 1
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        color TEXT DEFAULT '#0d9488',
        icon TEXT DEFAULT '📄',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        category_id INTEGER,
        file_name TEXT NOT NULL,
        file_type TEXT,
        file_size INTEGER,
        file_data BLOB,
        version INTEGER DEFAULT 1,
        status TEXT DEFAULT 'active',
        uploaded_by TEXT,
        department TEXT,
        review_date DATE,
        expiry_date DATE,
        tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS document_versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER NOT NULL,
        version INTEGER NOT NULL,
        file_name TEXT NOT NULL,
        file_data BLOB,
        changes_summary TEXT,
        uploaded_by TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (document_id) REFERENCES documents(id)
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        action TEXT NOT NULL,
        document_id INTEGER,
        document_title TEXT,
        details TEXT,
        ip_address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    
    default_categories = [
        ('Policies & Procedures', 'Organizational policies and standard operating procedures', '#0d9488', '📋'),
        ('Care Plans', 'Individual resident care plans and assessments', '#3b82f6', '💊'),
        ('Staff Training', 'Training records, certificates, and competency documents', '#8b5cf6', '🎓'),
        ('Health & Safety', 'Risk assessments, safety protocols, and incident reports', '#ef4444', '⚠️'),
        ('Quality Assurance', 'Audit reports, inspection findings, and improvement plans', '#f59e0b', '✅'),
        ('HR Documents', 'Staff contracts, DBS checks, and personnel files', '#6366f1', '👥'),
        ('Meeting Minutes', 'Staff meetings, board meetings, and case conferences', '#10b981', '📝'),
        ('Regulatory', 'CQC/Care Inspectorate correspondence and reports', '#ec4899', '🏛️'),
        ('Templates & Forms', 'Blank forms and document templates', '#64748b', '📄'),
        ('Resident Records', 'Resident information and family communications', '#06b6d4', '🏠')
    ]
    
    for name, desc, color, icon in default_categories:
        try:
            cursor.execute('INSERT OR IGNORE INTO categories (name, description, color, icon) VALUES (?, ?, ?, ?)',
                          (name, desc, color, icon))
        except:
            pass
    
    conn.commit()
    conn.close()

def add_document(title, description, category_id, file_name, file_type, file_size, file_data, 
                 uploaded_by, department=None, review_date=None, expiry_date=None, tags=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO documents (title, description, category_id, file_name, file_type, 
                      file_size, file_data, uploaded_by, department, review_date, expiry_date, tags)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (title, description, category_id, file_name, file_type, file_size, file_data,
                    uploaded_by, department, review_date, expiry_date, json.dumps(tags) if tags else None))
    
    doc_id = cursor.lastrowid
    cursor.execute('''INSERT INTO activity_log (user, action, document_id, document_title, details)
                      VALUES (?, ?, ?, ?, ?)''',
                   (uploaded_by, 'upload', doc_id, title, f'New document uploaded: {file_name}'))
    
    conn.commit()
    conn.close()
    return doc_id

def get_all_documents(category_id=None, search_term=None, status='active'):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''SELECT d.*, c.name as category_name, c.color as category_color, c.icon as category_icon
               FROM documents d LEFT JOIN categories c ON d.category_id = c.id WHERE d.status = ?'''
    params = [status]
    
    if category_id:
        query += ' AND d.category_id = ?'
        params.append(category_id)
    
    if search_term:
        query += ' AND (d.title LIKE ? OR d.description LIKE ? OR d.tags LIKE ?)'
        search_pattern = f'%{search_term}%'
        params.extend([search_pattern, search_pattern, search_pattern])
    
    query += ' ORDER BY d.updated_at DESC'
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def get_document_by_id(doc_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT d.*, c.name as category_name, c.color as category_color
                      FROM documents d LEFT JOIN categories c ON d.category_id = c.id WHERE d.id = ?''', (doc_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def delete_document(doc_id, deleted_by):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT title FROM documents WHERE id = ?', (doc_id,))
    result = cursor.fetchone()
    title = result['title'] if result else 'Unknown'
    cursor.execute("UPDATE documents SET status = 'deleted', updated_at = CURRENT_TIMESTAMP WHERE id = ?", (doc_id,))
    cursor.execute('INSERT INTO activity_log (user, action, document_id, document_title, details) VALUES (?, ?, ?, ?, ?)',
                   (deleted_by, 'delete', doc_id, title, 'Document deleted'))
    conn.commit()
    conn.close()

def get_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories ORDER BY name')
    results = cursor.fetchall()
    conn.close()
    return results

def get_category_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT c.id, c.name, c.color, c.icon, COUNT(d.id) as doc_count
                      FROM categories c LEFT JOIN documents d ON c.id = d.category_id AND d.status = 'active'
                      GROUP BY c.id ORDER BY doc_count DESC''')
    results = cursor.fetchall()
    conn.close()
    return results

def get_expiring_documents(days=30):
    conn = get_connection()
    cursor = conn.cursor()
    future_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''SELECT d.*, c.name as category_name, c.color as category_color
                      FROM documents d LEFT JOIN categories c ON d.category_id = c.id
                      WHERE d.status = 'active' AND d.expiry_date IS NOT NULL 
                      AND d.expiry_date <= ? AND d.expiry_date >= ? ORDER BY d.expiry_date ASC''',
                   (future_date, today))
    results = cursor.fetchall()
    conn.close()
    return results

def get_documents_for_review(days=30):
    conn = get_connection()
    cursor = conn.cursor()
    future_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
    cursor.execute('''SELECT d.*, c.name as category_name, c.color as category_color
                      FROM documents d LEFT JOIN categories c ON d.category_id = c.id
                      WHERE d.status = 'active' AND d.review_date IS NOT NULL 
                      AND d.review_date <= ? ORDER BY d.review_date ASC''', (future_date,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_document_versions(doc_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM document_versions WHERE document_id = ? ORDER BY version DESC', (doc_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_recent_activity(limit=50):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM activity_log ORDER BY created_at DESC LIMIT ?', (limit,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()
    stats = {}
    
    cursor.execute("SELECT COUNT(*) FROM documents WHERE status = 'active'")
    stats['total_documents'] = cursor.fetchone()[0]
    
    future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) FROM documents WHERE status = 'active' AND expiry_date IS NOT NULL AND expiry_date <= ?", (future_date,))
    stats['expiring_soon'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM documents WHERE status = 'active' AND review_date IS NOT NULL AND review_date <= ?", (future_date,))
    stats['due_for_review'] = cursor.fetchone()[0]
    
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute("SELECT COUNT(*) FROM documents WHERE status = 'active' AND created_at >= ?", (week_ago,))
    stats['recent_uploads'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(file_size) FROM documents WHERE status = 'active'")
    total_size = cursor.fetchone()[0]
    stats['total_size'] = total_size if total_size else 0
    
    conn.close()
    return stats

init_database()
