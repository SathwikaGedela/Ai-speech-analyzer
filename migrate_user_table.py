#!/usr/bin/env python3
"""
Migrate User table to add authentication fields
"""

import sqlite3
import os

def migrate_user_table():
    print("🔄 Migrating User table for authentication...")
    
    db_path = "backend/app.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file not found. Creating new database...")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check current user table structure
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        
        print("Current user table columns:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Check if new columns exist
        column_names = [col[1] for col in columns]
        
        migrations_needed = []
        
        if 'first_name' not in column_names:
            migrations_needed.append("ALTER TABLE user ADD COLUMN first_name VARCHAR(50)")
        
        if 'last_name' not in column_names:
            migrations_needed.append("ALTER TABLE user ADD COLUMN last_name VARCHAR(50)")
        
        if 'phone' not in column_names:
            migrations_needed.append("ALTER TABLE user ADD COLUMN phone VARCHAR(20)")
        
        if 'password_hash' not in column_names:
            migrations_needed.append("ALTER TABLE user ADD COLUMN password_hash VARCHAR(255)")
        
        if 'is_active' not in column_names:
            migrations_needed.append("ALTER TABLE user ADD COLUMN is_active BOOLEAN DEFAULT 1")
        
        # Execute migrations
        if migrations_needed:
            print(f"\n🔧 Executing {len(migrations_needed)} migrations...")
            for migration in migrations_needed:
                print(f"  Running: {migration}")
                cursor.execute(migration)
            
            conn.commit()
            print("✅ Migrations completed successfully!")
        else:
            print("✅ User table is already up to date!")
        
        # Show updated structure
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        
        print("\nUpdated user table columns:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    migrate_user_table()