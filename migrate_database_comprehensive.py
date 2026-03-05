#!/usr/bin/env python3
"""
Migrate database to add comprehensive analysis fields
"""

import sqlite3
import os

def migrate_database():
    """Add new columns to existing database"""
    
    print("🔄 MIGRATING DATABASE FOR COMPREHENSIVE ANALYSIS")
    print("=" * 50)
    
    db_path = os.path.join('backend', 'app.db')
    
    if not os.path.exists(db_path):
        print("❌ Database file not found. Run the app first to create it.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get current table structure
        cursor.execute("PRAGMA table_info(speech_session);")
        existing_columns = [column[1] for column in cursor.fetchall()]
        
        print(f"📋 Current columns: {len(existing_columns)}")
        for col in existing_columns:
            print(f"   - {col}")
        
        # Define new columns to add
        new_columns = [
            ("word_count", "INTEGER"),
            ("filler_percentage", "REAL"),
            ("grammar_score", "REAL"),
            ("vocabulary_diversity", "REAL"),
            ("unique_words", "INTEGER"),
            ("pronunciation_clarity", "REAL"),
            ("engagement_level", "VARCHAR(20)"),
            ("skill_level", "VARCHAR(30)"),
            ("pace_assessment", "TEXT"),
            ("filler_assessment", "TEXT"),
            ("grammar_assessment", "TEXT"),
            ("vocabulary_assessment", "TEXT"),
            ("tone_assessment", "TEXT"),
            ("general_impression", "TEXT"),
            ("strengths", "TEXT"),
            ("improvements", "TEXT"),
            ("actionable_tips", "TEXT"),
            ("grammar_errors", "TEXT")
        ]
        
        # Add missing columns
        added_columns = []
        for column_name, column_type in new_columns:
            if column_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE speech_session ADD COLUMN {column_name} {column_type};")
                    added_columns.append(column_name)
                    print(f"✅ Added column: {column_name}")
                except Exception as e:
                    print(f"❌ Failed to add column {column_name}: {e}")
        
        if added_columns:
            conn.commit()
            print(f"\n🎉 Successfully added {len(added_columns)} new columns!")
        else:
            print("\n✅ Database already up to date!")
        
        # Verify final structure
        cursor.execute("PRAGMA table_info(speech_session);")
        final_columns = [column[1] for column in cursor.fetchall()]
        
        print(f"\n📊 Final database structure: {len(final_columns)} columns")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return
    
    print("\n" + "=" * 50)
    print("✅ DATABASE MIGRATION COMPLETE!")
    print("\nNext steps:")
    print("1. Restart your Flask app")
    print("2. New analyses will include comprehensive data")
    print("3. Existing analyses will show basic data")
    print("4. History page will display all available information")

if __name__ == "__main__":
    migrate_database()