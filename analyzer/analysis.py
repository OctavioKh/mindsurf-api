import random
from datetime import datetime, timedelta
from typing import List, Dict


def get_emotion_from_ai(text_block: str) -> List[str]:
    """Simulates an expensive AI API call"""
    if len(text_block) < 100:
        return "error: text too short"
    emotions = ["disgusto", "enojo", "felicidad", "tristeza", "sorpresa", "miedo"]
    return random.choices(emotions, k=random.randint(1, 3))


class TranscriptAnalyzer:
    """Analyzes conversation transcripts"""
    
    SESSION_TIMEOUT_MINUTES = 10
    ACTION_KEYWORDS = ["need", "could", "help", "task", "do"]
    EMOTION_BLOCK_MIN_LENGTH = 100  # Minimum characters for emotion analysis
    
    def __init__(self, messages: List[Dict]):
        self.messages = sorted(messages, key=lambda m: m['timestamp'])
    
    def analyze(self) -> Dict:
        """Run full analysis on transcript"""
        return {
            "session_count": self._count_sessions(),
            "key_moments": {
                "questions_asked": self._count_questions(),
                "actions_identified": self._count_actions()
            },
            "emotion_analysis_results": self._analyze_emotions()
        }
    
    def _count_sessions(self) -> int:
        """Count sessions based on 10-minute silence threshold"""
        if not self.messages:
            return 0
        
        sessions = 1
        for i in range(1, len(self.messages)):
            prev_time = self.messages[i-1]['timestamp']
            curr_time = self.messages[i]['timestamp']
            
            if isinstance(prev_time, str):
                prev_time = datetime.fromisoformat(prev_time.replace('Z', '+00:00'))
            if isinstance(curr_time, str):
                curr_time = datetime.fromisoformat(curr_time.replace('Z', '+00:00'))
            
            time_diff = (curr_time - prev_time).total_seconds() / 60
            if time_diff > self.SESSION_TIMEOUT_MINUTES:
                sessions += 1
        
        return sessions
    
    def _count_questions(self) -> int:
        """Count messages containing question marks"""
        return sum(1 for msg in self.messages if '?' in msg['text'])
    
    def _count_actions(self) -> int:
        """Count messages containing action keywords"""
        count = 0
        for msg in self.messages:
            text_lower = msg['text'].lower()
            if any(keyword in text_lower for keyword in self.ACTION_KEYWORDS):
                count += 1
        return count
    
    def _analyze_emotions(self) -> List[Dict[str, str]]:
        """Analyze emotions using simulated AI on text blocks"""
        blocks = self._create_text_blocks()
        emotion_results = []
        
        for block in blocks:
            if len(block) > self.EMOTION_BLOCK_MIN_LENGTH:
                emotions = get_emotion_from_ai(block)
                if isinstance(emotions, list):
                    for emotion in emotions:
                        emotion_results.append({"emotion": emotion})
        
        return emotion_results
    
    def _create_text_blocks(self) -> List[str]:
        """Group consecutive messages into blocks"""
        if not self.messages:
            return []
        
        blocks = []
        current_block = ""
        
        for msg in self.messages:
            if len(current_block) + len(msg['text']) > 100:
                if current_block:
                    blocks.append(current_block)
                current_block = msg['text']
            else:
                current_block += " " + msg['text'] if current_block else msg['text']
        
        if current_block:
            blocks.append(current_block)
        
        return blocks
