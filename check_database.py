#!/usr/bin/env python3
"""
Check the database structure and content
"""

import sqlite3
import os

def check_database():
    """Check database structure and content"""
    print("🗄️ CHECKING DATABASE STRUCTURE")
    print("=" * 40)
    
    db_path = os.path.join('backend', 'app.db')
    
    if not os.path.exists(db_path):
        print("❌ Database file not found")
        return
    
    print(f"✅ Database file found: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n📋 Tables in database:")
        for table in tables:
            table_name = table[0]
            print(f"   ✅ {table_name}")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            print(f"      Columns:")
            for col in columns:
                col_id, col_name, col_type, not_null, default, pk = col
                pk_marker = " (PRIMARY KEY)" if pk else ""
                null_marker = " NOT NULL" if not_null else ""
                print(f"        - {col_name}: {col_type}{null_marker}{pk_marker}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"      Rows: {count}")
            
            # Show sample data if any
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                rows = cursor.fetchall()
                print(f"      Sample data:")
                for i, row in enumerate(rows, 1):
                    print(f"        Row {i}: {row}")
            
            print()
        
        conn.close()
        
        print("🎉 Database structure verified!")
        
    except Exception as e:
        print(f"❌ Database check error: {e}")

if __name__ == "__main__":
    check_database()