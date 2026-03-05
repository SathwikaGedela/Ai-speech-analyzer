#!/usr/bin/env python3
"""
Backfill comprehensive analysis data for existing sessions
"""

import sys
import os
sys.path.append('backend')

from backend.app import create_app
from backend.database import db
from backend.models.session import SpeechSession
from backend.services.text_analysis import analyze_text
from backend.routes.analyze import (
    get_skill_level, get_general_impression, get_pace_assessment,
    get_filler_assessment, get_grammar_assessment, get_vocabulary_assessment,
    get_tone_assessment, get_engagement_level, generate_strengths,
    generate_improvements, generate_actionable_tips
)
import json

def backfill_session_data():
    """Backfill comprehensive data for existing sessions"""
    
    print("🔄 BACKFILLING COMPREHENSIVE DATA FOR EXISTING SESSIONS")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        # Get sessions that need backfilling (missing comprehensive data)
        sessions_to_update = SpeechSession.query.filter(
            SpeechSession.word_count.is_(None)
        ).all()
        
        if not sessions_to_update:
            print("✅ All sessions already have comprehensive data!")
            return
        
        print(f"📊 Found {len(sessions_to_update)} sessions to update")
        
        for i, session in enumerate(sessions_to_update, 1):
            print(f"\n🔄 Processing session {i}/{len(sessions_to_update)} (ID: {session.id})")
            
            try:
                # Re-analyze the transcript to get comprehensive metrics
                if not session.transcript:
                    print("   ⚠️ No transcript available, skipping...")
                    continue
                
                # Estimate duration from WPM and word count
                words = session.transcript.split()
                word_count = len(words)
                estimated_duration = (word_count / session.wpm) * 60 if session.wpm > 0 else 60
                
                print(f"   📝 Transcript: {len(session.transcript)} chars, {word_count} words")
                print(f"   ⏱️ Estimated duration: {estimated_duration:.1f} seconds")
                
                # Analyze text to get comprehensive metrics
                metrics = analyze_text(session.transcript, estimated_duration)
                
                # Update session with comprehensive data
                session.word_count = metrics.get("word_count", word_count)
                session.filler_percentage = metrics.get("filler_percentage", 0)
                session.grammar_score = metrics.get("grammar_score", 85)
                session.vocabulary_diversity = metrics.get("vocabulary_diversity", 70)
                session.unique_words = metrics.get("unique_words", len(set(word.lower() for word in words)))
                session.pronunciation_clarity = max(70, 100 - session.fillers * 2)
                session.engagement_level = get_engagement_level(session.confidence)
                session.skill_level = get_skill_level(session.confidence)
                
                # Generate assessments
                session.pace_assessment = get_pace_assessment(session.wpm)
                session.filler_assessment = get_filler_assessment(session.fillers)
                session.grammar_assessment = get_grammar_assessment(metrics['grammar_score'], metrics.get('grammar_errors', []))
                session.vocabulary_assessment = get_vocabulary_assessment(metrics['vocabulary_diversity'])
                session.tone_assessment = get_tone_assessment(session.sentiment)
                session.general_impression = get_general_impression(session.confidence)
                
                # Generate JSON data
                session.strengths = json.dumps(generate_strengths(metrics, session.confidence))
                session.improvements = json.dumps(generate_improvements(metrics, session.confidence))
                session.actionable_tips = json.dumps(generate_actionable_tips(metrics, session.confidence))
                session.grammar_errors = json.dumps(metrics.get('grammar_errors', []))
                
                print(f"   ✅ Updated comprehensive data:")
                print(f"      - Word count: {session.word_count}")
                print(f"      - Grammar score: {session.grammar_score}%")
                print(f"      - Vocabulary diversity: {session.vocabulary_diversity}%")
                print(f"      - Skill level: {session.skill_level}")
                print(f"      - Engagement: {session.engagement_level}")
                
            except Exception as e:
                print(f"   ❌ Error processing session {session.id}: {e}")
                continue
        
        # Save all changes
        try:
            db.session.commit()
            print(f"\n🎉 Successfully updated {len(sessions_to_update)} sessions!")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Failed to save changes: {e}")
            return
    
    print("\n" + "=" * 60)
    print("✅ BACKFILL COMPLETE!")
    print("\nNext steps:")
    print("1. Restart your Flask app")
    print("2. Go to history page")
    print("3. Click 'Details' on any session")
    print("4. You should now see comprehensive data instead of 'N/A'")

def verify_backfill():
    """Verify that backfill was successful"""
    
    print("\n🔍 VERIFYING BACKFILL RESULTS")
    print("=" * 40)
    
    app = create_app()
    
    with app.app_context():
        # Check sessions with comprehensive data
        total_sessions = SpeechSession.query.count()
        sessions_with_data = SpeechSession.query.filter(
            SpeechSession.word_count.isnot(None)
        ).count()
        
        print(f"📊 Total sessions: {total_sessions}")
        print(f"📈 Sessions with comprehensive data: {sessions_with_data}")
        
        if sessions_with_data == total_sessions:
            print("✅ All sessions have comprehensive data!")
        else:
            print(f"⚠️ {total_sessions - sessions_with_data} sessions still missing data")
        
        # Show sample of updated data
        sample_session = SpeechSession.query.filter(
            SpeechSession.word_count.isnot(None)
        ).first()
        
        if sample_session:
            print(f"\n📋 Sample session data (ID: {sample_session.id}):")
            print(f"   Word count: {sample_session.word_count}")
            print(f"   Grammar score: {sample_session.grammar_score}%")
            print(f"   Skill level: {sample_session.skill_level}")
            print(f"   Engagement: {sample_session.engagement_level}")
            print(f"   Strengths: {len(sample_session.get_strengths_list())} items")
            print(f"   Improvements: {len(sample_session.get_improvements_list())} items")

if __name__ == "__main__":
    backfill_session_data()
    verify_backfill()