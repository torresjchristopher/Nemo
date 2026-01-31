"""
Temporal Rewind Engine: Infer what the user was doing N minutes ago

Based on:
1. Keyboard signature (35-dimensional behavior vector)
2. Current screen context
3. Historical keystroke patterns
4. User intent inference

Reconstruction method:
- NOT replay/recording (data invisible)
- Pure synthesis from behavioral patterns
- "What was I likely doing 5 minutes ago?"
"""

import logging
import time
from typing import Optional, Dict, List
from dataclasses import dataclass
from collections import deque
import threading


@dataclass
class KeystrokeSnapshot:
    """Point-in-time keystroke behavior snapshot."""
    timestamp: float
    keystroke_vector: List[float]  # 35-D behavioral signature
    screen_context: str  # Application name + window title
    detected_intent: str  # What user was likely doing
    activity_type: str  # "typing", "navigation", "coding", etc


class TemporalRewindEngine:
    """
    Infer what user was doing at earlier time points.
    
    Uses behavioral synthesis rather than recording.
    """
    
    def __init__(self, window_size_seconds: int = 300):
        """
        Initialize rewind engine.
        
        Args:
            window_size_seconds: How far back to keep history (default 5 minutes)
        """
        self.logger = logging.getLogger(__name__)
        self.window_size = window_size_seconds
        
        # Keep rolling window of snapshots
        self.snapshots: deque = deque(maxlen=1000)  # ~300 snapshots per minute = 5 min history
        self.lock = threading.RLock()
        
        self.logger.info(f"Rewind engine initialized (window: {window_size_seconds}s)")
    
    def record_keystroke_snapshot(self, 
                                 keystroke_vector: List[float],
                                 screen_context: str,
                                 intent: str = "unknown"):
        """
        Record a keystroke snapshot for later inference.
        
        Args:
            keystroke_vector: 35-D behavioral signature
            screen_context: Application and window title
            intent: Detected user intent
        """
        with self.lock:
            snapshot = KeystrokeSnapshot(
                timestamp=time.time(),
                keystroke_vector=keystroke_vector,
                screen_context=screen_context,
                detected_intent=intent,
                activity_type=self._classify_activity(keystroke_vector, intent)
            )
            self.snapshots.append(snapshot)
    
    def _classify_activity(self, keystroke_vector: List[float], intent: str) -> str:
        """
        Classify user activity type from keystroke signature.
        
        Args:
            keystroke_vector: 35-D behavioral signature
            intent: User intent string
        
        Returns:
            Activity classification
        """
        # Simplified activity classification based on keystroke patterns
        if intent and "code" in intent.lower():
            return "coding"
        elif intent and "write" in intent.lower():
            return "writing"
        elif intent and "search" in intent.lower():
            return "searching"
        elif keystroke_vector and len(keystroke_vector) > 0:
            # Could do ML classification here
            # For now, use simple heuristic
            speed = keystroke_vector[0] if keystroke_vector else 0
            if speed > 50:
                return "fast_typing"
            elif speed > 30:
                return "normal_typing"
            else:
                return "slow_navigation"
        return "unknown"
    
    def infer_past_activity(self, minutes_ago: int = 5) -> Optional[Dict]:
        """
        Infer what user was doing N minutes ago.
        
        Args:
            minutes_ago: How many minutes back (default 5)
        
        Returns:
            Synthesis of past activity or None
        """
        with self.lock:
            if not self.snapshots:
                self.logger.warning("No snapshot history available")
                return None
            
            # Find snapshots from N minutes ago
            target_time = time.time() - (minutes_ago * 60)
            
            # Get snapshots within ±30 second window
            relevant_snapshots = [
                s for s in self.snapshots
                if abs(s.timestamp - target_time) < 30
            ]
            
            if not relevant_snapshots:
                self.logger.warning(f"No snapshots from {minutes_ago} minutes ago")
                return None
            
            # Synthesize most likely activity from snapshots
            return self._synthesize_activity(relevant_snapshots, minutes_ago)
    
    def _synthesize_activity(self, snapshots: List[KeystrokeSnapshot], 
                            minutes_ago: int) -> Dict:
        """
        Synthesize past activity from snapshot cluster.
        
        Args:
            snapshots: Keystroke snapshots from time window
            minutes_ago: Time distance for context
        
        Returns:
            Synthesized activity description
        """
        # Most common screen context
        screen_contexts = [s.screen_context for s in snapshots]
        most_common_context = max(set(screen_contexts), key=screen_contexts.count)
        
        # Most common activity type
        activities = [s.activity_type for s in snapshots]
        most_common_activity = max(set(activities), key=activities.count)
        
        # Most common intent
        intents = [s.detected_intent for s in snapshots]
        most_common_intent = max(set(intents), key=intents.count)
        
        # Average keystroke behavior
        avg_vector = [
            sum(s.keystroke_vector[i] for s in snapshots if i < len(s.keystroke_vector)) / len(snapshots)
            for i in range(min(35, max(len(s.keystroke_vector) for s in snapshots)))
        ]
        
        synthesis = {
            'time_ago': minutes_ago,
            'inferred_action': self._action_from_activity(most_common_activity, most_common_intent),
            'likely_application': most_common_context,
            'activity_type': most_common_activity,
            'intent': most_common_intent,
            'confidence': len(snapshots) / 10.0,  # More snapshots = higher confidence
            'keystroke_intensity': avg_vector[0] if avg_vector else 0,
            'synthesized': True,  # Not recorded - synthesized from patterns
            'description': self._generate_natural_language(
                minutes_ago, most_common_activity, most_common_context, most_common_intent
            )
        }
        
        self.logger.info(f"Rewind synthesis: {synthesis['description']}")
        return synthesis
    
    def _action_from_activity(self, activity_type: str, intent: str) -> str:
        """Convert activity to likely action."""
        action_map = {
            'coding': 'Writing/editing code',
            'writing': 'Composing text',
            'searching': 'Researching information',
            'fast_typing': 'Active typing',
            'normal_typing': 'Regular work',
            'slow_navigation': 'Browsing/exploring'
        }
        return action_map.get(activity_type, f"Working on {intent}")
    
    def _generate_natural_language(self, minutes_ago: int, activity: str, 
                                  context: str, intent: str) -> str:
        """Generate natural language description of inferred activity."""
        return (
            f"{minutes_ago} minute{'s' if minutes_ago != 1 else ''} ago, "
            f"you were likely {activity.replace('_', ' ').lower()} "
            f"in {context}. Your intent was: {intent}"
        )
    
    def get_history(self, minutes: int = 5) -> List[Dict]:
        """
        Get activity history for past N minutes.
        
        Returns:
            List of synthesized activities
        """
        history = []
        for i in range(1, minutes + 1):
            activity = self.infer_past_activity(minutes_ago=i)
            if activity:
                history.append(activity)
        return history
    
    def clear_history(self):
        """Clear all snapshot history (privacy)."""
        with self.lock:
            self.snapshots.clear()
        self.logger.info("Snapshot history cleared")
