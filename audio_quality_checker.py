#!/usr/bin/env python3
"""
Audio Quality Assessment Module
Checks if audio is suitable for speech analysis
"""

import os
import numpy as np
from pydub import AudioSegment
from pydub.utils import make_chunks

class AudioQualityChecker:
    """Assess audio quality for speech analysis suitability"""
    
    def __init__(self):
        self.min_duration = 3.0  # Minimum 3 seconds
        self.max_duration = 300.0  # Maximum 5 minutes
        self.min_volume_db = -60  # Minimum volume threshold
        self.max_silence_ratio = 0.8  # Maximum 80% silence
    
    def assess_audio_quality(self, audio_file_path):
        """Comprehensive audio quality assessment"""
        try:
            # Load audio file
            audio = AudioSegment.from_file(audio_file_path)
            
            assessment = {
                'overall_quality': 'good',
                'issues': [],
                'warnings': [],
                'recommendations': [],
                'metrics': {}
            }
            
            # Check duration
            duration_check = self._check_duration(audio)
            assessment['metrics']['duration'] = duration_check
            if duration_check['issue']:
                assessment['issues'].append(duration_check['message'])
                assessment['overall_quality'] = 'poor'
            
            # Check volume levels
            volume_check = self._check_volume_levels(audio)
            assessment['metrics']['volume'] = volume_check
            if volume_check['issue']:
                if volume_check['severity'] == 'critical':
                    assessment['issues'].append(volume_check['message'])
                    assessment['overall_quality'] = 'poor'
                else:
                    assessment['warnings'].append(volume_check['message'])
                    if assessment['overall_quality'] == 'good':
                        assessment['overall_quality'] = 'fair'
            
            # Check for silence
            silence_check = self._check_silence_ratio(audio)
            assessment['metrics']['silence'] = silence_check
            if silence_check['issue']:
                assessment['warnings'].append(silence_check['message'])
                if assessment['overall_quality'] == 'good':
                    assessment['overall_quality'] = 'fair'
            
            # Check audio format and quality
            format_check = self._check_audio_format(audio, audio_file_path)
            assessment['metrics']['format'] = format_check
            if format_check['warning']:
                assessment['warnings'].append(format_check['message'])
            
            # Generate recommendations
            assessment['recommendations'] = self._generate_recommendations(assessment)
            
            return assessment
            
        except Exception as e:
            return {
                'overall_quality': 'error',
                'issues': [f'Could not assess audio quality: {str(e)}'],
                'warnings': [],
                'recommendations': ['Try using a different audio file format'],
                'metrics': {}
            }
    
    def _check_duration(self, audio):
        """Check if audio duration is suitable"""
        duration_seconds = len(audio) / 1000.0
        
        if duration_seconds < self.min_duration:
            return {
                'duration_seconds': duration_seconds,
                'issue': True,
                'severity': 'critical',
                'message': f'Audio too short ({duration_seconds:.1f}s). Minimum {self.min_duration}s required.'
            }
        elif duration_seconds > self.max_duration:
            return {
                'duration_seconds': duration_seconds,
                'issue': True,
                'severity': 'warning',
                'message': f'Audio very long ({duration_seconds:.1f}s). Consider using shorter clips for better analysis.'
            }
        else:
            return {
                'duration_seconds': duration_seconds,
                'issue': False,
                'message': f'Duration is good ({duration_seconds:.1f}s)'
            }
    
    def _check_volume_levels(self, audio):
        """Check audio volume levels"""
        # Get RMS (Root Mean Square) for volume analysis
        rms = audio.rms
        db_level = audio.dBFS
        
        if db_level < self.min_volume_db:
            return {
                'db_level': db_level,
                'rms': rms,
                'issue': True,
                'severity': 'critical',
                'message': f'Audio too quiet ({db_level:.1f} dB). Please record with higher volume.'
            }
        elif db_level < -40:
            return {
                'db_level': db_level,
                'rms': rms,
                'issue': True,
                'severity': 'warning',
                'message': f'Audio quite quiet ({db_level:.1f} dB). Consider increasing volume.'
            }
        elif db_level > -3:
            return {
                'db_level': db_level,
                'rms': rms,
                'issue': True,
                'severity': 'warning',
                'message': f'Audio may be too loud ({db_level:.1f} dB). Risk of distortion.'
            }
        else:
            return {
                'db_level': db_level,
                'rms': rms,
                'issue': False,
                'message': f'Volume level is good ({db_level:.1f} dB)'
            }
    
    def _check_silence_ratio(self, audio):
        """Check ratio of silence in audio"""
        try:
            # Define silence threshold (adjust as needed)
            silence_threshold = -50  # dB
            
            # Split audio into chunks for analysis
            chunk_length = 100  # milliseconds
            chunks = make_chunks(audio, chunk_length)
            
            silent_chunks = 0
            total_chunks = len(chunks)
            
            for chunk in chunks:
                if chunk.dBFS < silence_threshold:
                    silent_chunks += 1
            
            silence_ratio = silent_chunks / total_chunks if total_chunks > 0 else 0
            
            if silence_ratio > self.max_silence_ratio:
                return {
                    'silence_ratio': silence_ratio,
                    'issue': True,
                    'message': f'Too much silence ({silence_ratio*100:.1f}%). Ensure continuous speech.'
                }
            elif silence_ratio > 0.5:
                return {
                    'silence_ratio': silence_ratio,
                    'issue': True,
                    'message': f'Significant silence detected ({silence_ratio*100:.1f}%). Consider editing audio.'
                }
            else:
                return {
                    'silence_ratio': silence_ratio,
                    'issue': False,
                    'message': f'Good speech-to-silence ratio ({silence_ratio*100:.1f}% silence)'
                }
        
        except Exception:
            return {
                'silence_ratio': 0,
                'issue': False,
                'message': 'Could not analyze silence ratio'
            }
    
    def _check_audio_format(self, audio, file_path):
        """Check audio format and quality parameters"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        format_info = {
            'format': file_extension,
            'sample_rate': audio.frame_rate,
            'channels': audio.channels,
            'sample_width': audio.sample_width,
            'warning': False,
            'message': ''
        }
        
        # Check sample rate
        if audio.frame_rate < 16000:
            format_info['warning'] = True
            format_info['message'] = f'Low sample rate ({audio.frame_rate} Hz). 16kHz+ recommended for speech.'
        elif audio.frame_rate > 48000:
            format_info['warning'] = True
            format_info['message'] = f'Very high sample rate ({audio.frame_rate} Hz). May be unnecessary for speech.'
        
        # Check channels
        if audio.channels > 2:
            format_info['warning'] = True
            format_info['message'] += f' Multi-channel audio ({audio.channels} channels) detected.'
        
        # Check bit depth
        if audio.sample_width < 2:  # Less than 16-bit
            format_info['warning'] = True
            format_info['message'] += f' Low bit depth detected.'
        
        if not format_info['message']:
            format_info['message'] = f'Audio format is suitable ({file_extension}, {audio.frame_rate}Hz, {audio.channels}ch)'
        
        return format_info
    
    def _generate_recommendations(self, assessment):
        """Generate specific recommendations based on assessment"""
        recommendations = []
        
        # Duration recommendations
        if assessment['metrics'].get('duration', {}).get('issue'):
            duration = assessment['metrics']['duration']['duration_seconds']
            if duration < self.min_duration:
                recommendations.append("Record longer audio (at least 10-30 seconds for better analysis)")
            elif duration > self.max_duration:
                recommendations.append("Use shorter audio clips (30 seconds to 2 minutes is optimal)")
        
        # Volume recommendations
        volume_info = assessment['metrics'].get('volume', {})
        if volume_info.get('issue'):
            db_level = volume_info.get('db_level', 0)
            if db_level < -40:
                recommendations.append("Increase recording volume or speak closer to microphone")
            elif db_level > -3:
                recommendations.append("Reduce recording volume to avoid distortion")
        
        # Silence recommendations
        silence_info = assessment['metrics'].get('silence', {})
        if silence_info.get('issue'):
            recommendations.append("Reduce long pauses and silent sections for better analysis")
        
        # Format recommendations
        format_info = assessment['metrics'].get('format', {})
        if format_info.get('warning'):
            recommendations.append("Consider using WAV format with 16kHz+ sample rate for best results")
        
        # General recommendations
        if assessment['overall_quality'] in ['poor', 'fair']:
            recommendations.extend([
                "Record in a quiet environment with minimal background noise",
                "Speak clearly and at a consistent volume",
                "Use a good quality microphone if possible"
            ])
        
        return recommendations
    
    def get_quality_score(self, assessment):
        """Convert quality assessment to numerical score (0-100)"""
        if assessment['overall_quality'] == 'error':
            return 0
        elif assessment['overall_quality'] == 'poor':
            return 25
        elif assessment['overall_quality'] == 'fair':
            return 60
        else:  # good
            return 90

def test_audio_quality_checker():
    """Test the audio quality checker"""
    print("🔍 TESTING AUDIO QUALITY CHECKER")
    print("=" * 50)
    
    checker = AudioQualityChecker()
    
    # Test with available files
    test_files = [
        'uploads/sathaudio.m4a',
        'uploads/sathaudio.flac'
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n📁 Testing: {test_file}")
            
            assessment = checker.assess_audio_quality(test_file)
            
            print(f"  Overall Quality: {assessment['overall_quality'].upper()}")
            print(f"  Quality Score: {checker.get_quality_score(assessment)}/100")
            
            if assessment['issues']:
                print("  🔴 Issues:")
                for issue in assessment['issues']:
                    print(f"    • {issue}")
            
            if assessment['warnings']:
                print("  🟡 Warnings:")
                for warning in assessment['warnings']:
                    print(f"    • {warning}")
            
            if assessment['recommendations']:
                print("  💡 Recommendations:")
                for rec in assessment['recommendations'][:3]:  # Show top 3
                    print(f"    • {rec}")
            
            # Show metrics
            metrics = assessment['metrics']
            if 'duration' in metrics:
                print(f"  📊 Duration: {metrics['duration']['duration_seconds']:.1f}s")
            if 'volume' in metrics:
                print(f"  🔊 Volume: {metrics['volume']['db_level']:.1f} dB")
            if 'format' in metrics:
                format_info = metrics['format']
                print(f"  🎵 Format: {format_info['sample_rate']}Hz, {format_info['channels']}ch")
        
        else:
            print(f"\n❌ Test file not found: {test_file}")
    
    print(f"\n✅ Audio quality checker ready!")

if __name__ == "__main__":
    test_audio_quality_checker()