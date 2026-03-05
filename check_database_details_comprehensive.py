#!/usr/bin/env python3
"""
Comprehensive Database Details Checker
Shows complete information about your database structure, content, and configuration
"""

import sys
import os
import sqlite3
from datetime import datetime

# Add backend to path for imports
sys.path.append('backend')

def check_database_file_info():
    """Check basic database file information"""
    print("📁 DATABASE FILE INFORMATION")
    print("=" * 50)
    
    db_paths = [
        'backend/app.db',
        'instance/app.db',
        'app.db'
    ]
    
    db_path = None
    for path in db_paths:
        if os.path.exists(path):
            db_path = path
            break
    
    if not db_path:
        print("❌ No database file found in expected locations:")
        for path in db_paths:
            print(f"   - {path}")
        return None
    
    print(f"✅ Database found: {db_path}")
    
    # Get file stats
    stat = os.stat(db_path)
    size_mb = stat.st_size / (1024 * 1024)
    modified = datetime.fromtimestamp(stat.st_mtime)
    
    print(f"📊 File size: {stat.st_size:,} bytes ({size_mb:.2f} MB)")
    print(f"📅 Last modified: {modified}")
    print(f"🔒 Permissions: {oct(stat.st_mode)[-3:]}")
    
    return db_path

def check_database_structure(db_path):
    """Check detailed database structure"""
    print(f"\n🏗️ DATABASE STRUCTURE")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get SQLite version
        cursor.execute("SELECT sqlite_version();")
        sqlite_version = cursor.fetchone()[0]
        print(f"🔧 SQLite version: {sqlite_version}")
        
        # Get database schema version (if exists)
        try:
            cursor.execute("PRAGMA user_version;")
            user_version = cursor.fetchone()[0]
            print(f"📋 Schema version: {user_version}")
        except:
            print("📋 Schema version: Not set")
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()
        
        print(f"\n📊 Tables ({len(tables)} total):")
        
        total_rows = 0
        for table in tables:
            table_name = table[0]
            
            # Skip sqlite internal tables
            if table_name.startswith('sqlite_'):
                continue
                
            print(f"\n   📋 Table: {table_name}")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            print(f"      📝 Columns ({len(columns)} total):")
            for col in columns:
                col_id, col_name, col_type, not_null, default, pk = col
                
                # Build column description
                desc_parts = [col_type]
                if pk:
                    desc_parts.append("PRIMARY KEY")
                if not_null:
                    desc_parts.append("NOT NULL")
                if default is not None:
                    desc_parts.append(f"DEFAULT {default}")
                
                desc = " ".join(desc_parts)
                print(f"         • {col_name}: {desc}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            total_rows += count
            print(f"      📊 Rows: {count:,}")
            
            # Get table size (approximate)
            cursor.execute(f"SELECT SUM(length(quote(c))) FROM (SELECT * FROM {table_name});")
            try:
                size_result = cursor.fetchone()[0]
                if size_result:
                    size_kb = size_result / 1024
                    print(f"      💾 Approximate size: {size_kb:.2f} KB")
            except:
                pass
        
        print(f"\n📊 Total rows across all tables: {total_rows:,}")
        
        # Check indexes
        cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%' ORDER BY tbl_name, name;")
        indexes = cursor.fetchall()
        
        if indexes:
            print(f"\n🔍 Indexes ({len(indexes)} total):")
            current_table = None
            for idx_name, tbl_name in indexes:
                if tbl_name != current_table:
                    print(f"   📋 Table: {tbl_name}")
                    current_table = tbl_name
                print(f"      • {idx_name}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error checking database structure: {e}")
        return False

def check_database_content(db_path):
    """Check database content with sample data"""
    print(f"\n📄 DATABASE CONTENT PREVIEW")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all user tables (exclude sqlite internal tables)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            
            print(f"\n📋 Table: {table_name} ({count:,} rows)")
            
            if count == 0:
                print("      (empty)")
                continue
            
            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            col_names = [col[1] for col in columns]
            
            # Show sample data (first 3 rows)
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
            rows = cursor.fetchall()
            
            if rows:
                print("      Sample data:")
                for i, row in enumerate(rows, 1):
                    print(f"         Row {i}:")
                    for j, value in enumerate(row):
                        col_name = col_names[j] if j < len(col_names) else f"col_{j}"
                        # Truncate long values
                        if isinstance(value, str) and len(value) > 50:
                            display_value = value[:47] + "..."
                        else:
                            display_value = value
                        print(f"            {col_name}: {display_value}")
            
            # Show recent data if there's a timestamp column
            timestamp_cols = ['created_at', 'updated_at', 'timestamp', 'date_created']
            timestamp_col = None
            for col in timestamp_cols:
                if col in col_names:
                    timestamp_col = col
                    break
            
            if timestamp_col and count > 3:
                print(f"      Most recent entries (by {timestamp_col}):")
                cursor.execute(f"SELECT * FROM {table_name} ORDER BY {timestamp_col} DESC LIMIT 2;")
                recent_rows = cursor.fetchall()
                
                for i, row in enumerate(recent_rows, 1):
                    print(f"         Recent {i}:")
                    for j, value in enumerate(row):
                        col_name = col_names[j] if j < len(col_names) else f"col_{j}"
                        if isinstance(value, str) and len(value) > 50:
                            display_value = value[:47] + "..."
                        else:
                            display_value = value
                        print(f"            {col_name}: {display_value}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error checking database content: {e}")

def check_database_config():
    """Check database configuration from the app"""
    print(f"\n⚙️ DATABASE CONFIGURATION")
    print("=" * 50)
    
    try:
        # Try to import Flask app configuration
        from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
        
        print(f"🔗 Database URI: {SQLALCHEMY_DATABASE_URI}")
        print(f"📊 Track modifications: {SQLALCHEMY_TRACK_MODIFICATIONS}")
        
        # Check if it's SQLite
        if 'sqlite' in SQLALCHEMY_DATABASE_URI.lower():
            print("💾 Database type: SQLite")
            
            # Extract database path from URI
            if ':///' in SQLALCHEMY_DATABASE_URI:
                db_file = SQLALCHEMY_DATABASE_URI.split(':///')[-1]
                print(f"📁 Database file path: {db_file}")
        
    except ImportError as e:
        print(f"⚠️ Could not import database config: {e}")
        print("   This might be normal if config.py doesn't exist")
    except Exception as e:
        print(f"❌ Error checking database config: {e}")

def check_flask_models():
    """Check Flask SQLAlchemy models"""
    print(f"\n🏗️ FLASK MODELS")
    print("=" * 50)
    
    try:
        # Import models
        from models.user import User
        from models.session import SpeechSession
        
        print("✅ Successfully imported models:")
        print("   • User model")
        print("   • SpeechSession model")
        
        # Try to get model information
        print(f"\n📋 User model fields:")
        for column in User.__table__.columns:
            print(f"   • {column.name}: {column.type}")
        
        print(f"\n📋 SpeechSession model fields:")
        for column in SpeechSession.__table__.columns:
            print(f"   • {column.name}: {column.type}")
            
    except ImportError as e:
        print(f"⚠️ Could not import models: {e}")
    except Exception as e:
        print(f"❌ Error checking models: {e}")

def main():
    """Main function to check all database details"""
    print("🗄️ COMPREHENSIVE DATABASE DETAILS CHECK")
    print("=" * 60)
    print(f"🕒 Check time: {datetime.now()}")
    
    # Check database file
    db_path = check_database_file_info()
    
    if db_path:
        # Check structure
        if check_database_structure(db_path):
            # Check content
            check_database_content(db_path)
    
    # Check configuration
    check_database_config()
    
    # Check Flask models
    check_flask_models()
    
    print(f"\n✅ Database details check complete!")
    print("\n💡 TIP: If you want to see more specific data, you can:")
    print("   • Run 'python check_database.py' for basic structure")
    print("   • Run 'python check_users_database.py' for user-specific data")
    print("   • Use SQLite browser tools for visual inspection")

if __name__ == "__main__":
    main()