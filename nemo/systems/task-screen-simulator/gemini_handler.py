"""
Gemini Voice AI Handler: Screenshot capture + voice input → Gemini API → voice response

Features:
- Voice input while RIGHT ALT held
- Optional screenshot capture (configurable)
- Send to Gemini API with context
- Voice response generation
- Data invisibility (no local storage)
"""

import logging
import os
import base64
import threading
import queue
from typing import Optional, Callable, Dict
from dataclasses import dataclass
from enum import Enum
import time

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None


class GeminiMode(Enum):
    """Gemini interaction mode."""
    VOICE_ONLY = "voice"  # Just voice input to Gemini
    WITH_SCREENSHOT = "screenshot"  # Voice + screenshot
    WITH_VIDEO = "video"  # Voice + screen recording


@dataclass
class GeminiConfig:
    """Configuration for Gemini integration."""
    api_key: Optional[str] = None
    model: str = "gemini-2.0-flash"
    mode: GeminiMode = GeminiMode.VOICE_ONLY
    screenshot_enabled: bool = True
    video_enabled: bool = False
    max_tokens: int = 1024
    temperature: float = 0.7
    timeout_seconds: int = 30


class GeminiHandler:
    """
    Handle Gemini API interactions with optional screenshot context.
    
    Workflow:
    1. User holds RIGHT ALT
    2. Optional: Screenshot captured
    3. User speaks (voice transcribed)
    4. Voice + screenshot sent to Gemini
    5. Response comes back
    6. Response spoken aloud via TTS
    """
    
    def __init__(self, config: Optional[GeminiConfig] = None, 
                 tts_engine = None,
                 response_callback: Optional[Callable[[str], None]] = None):
        """
        Initialize Gemini handler.
        
        Args:
            config: Gemini configuration
            tts_engine: TTS engine for speaking responses
            response_callback: Callback for response text updates
        """
        self.config = config or GeminiConfig()
        self.tts_engine = tts_engine
        self.response_callback = response_callback
        self.logger = logging.getLogger(__name__)
        
        # Initialize Gemini client
        self._init_gemini()
        
        # Thread management
        self.current_task: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.response_queue = queue.Queue()
    
    def _init_gemini(self):
        """Initialize Gemini API client."""
        if genai is None:
            self.logger.warning("google-generativeai library not installed. Gemini disabled.")
            return
        
        if not self.config.api_key:
            self.logger.warning("GEMINI_API_KEY not set. Gemini disabled.")
            return
        
        try:
            genai.configure(api_key=self.config.api_key)
            self.model = genai.GenerativeModel(self.config.model)
            self.logger.info(f"Gemini initialized ({self.config.model})")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini: {e}")
            self.model = None
    
    def capture_screenshot(self) -> Optional[bytes]:
        """
        Capture current screen as PNG bytes.
        
        Returns:
            PNG image bytes or None if capture failed
        """
        if not self.config.screenshot_enabled:
            return None
        
        if ImageGrab is None:
            self.logger.warning("PIL not available for screenshot")
            return None
        
        try:
            # Capture screen to PIL Image
            screenshot = ImageGrab.grab()
            
            # Convert to PNG bytes
            import io
            img_bytes = io.BytesIO()
            screenshot.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            self.logger.info(f"Screenshot captured ({len(img_bytes.getvalue())} bytes)")
            return img_bytes.getvalue()
        
        except Exception as e:
            self.logger.error(f"Screenshot capture failed: {e}")
            return None
    
    def send_to_gemini(self, text_input: str, screenshot_bytes: Optional[bytes] = None) -> Optional[str]:
        """
        Send text (and optional screenshot) to Gemini API.
        
        Args:
            text_input: User's voice transcription
            screenshot_bytes: Optional screenshot PNG bytes
        
        Returns:
            Gemini's response text or None
        """
        if self.model is None:
            self.logger.error("Gemini model not initialized")
            if self.response_callback:
                self.response_callback("[Gemini not configured]")
            return None
        
        try:
            # Build the message
            content_parts = [text_input]
            
            # Add screenshot if provided
            if screenshot_bytes:
                # Convert bytes to base64 for Gemini API
                import base64
                b64_screenshot = base64.b64encode(screenshot_bytes).decode('utf-8')
                
                # Add as image to content
                content_parts.append({
                    "mime_type": "image/png",
                    "data": b64_screenshot
                })
                self.logger.info("Screenshot included in Gemini request")
            
            if self.response_callback:
                self.response_callback("[Sending to Gemini...]")
            
            # Call Gemini API
            response = self.model.generate_content(content_parts)
            result_text = response.text
            
            self.logger.info(f"Gemini response: {result_text[:100]}...")
            
            # Queue for processing
            self.response_queue.put({
                'text': result_text,
                'complete': True,
                'has_screenshot': bool(screenshot_bytes)
            })
            
            return result_text
        
        except Exception as e:
            self.logger.error(f"Gemini API error: {e}")
            if self.response_callback:
                self.response_callback(f"[Error: {str(e)[:50]}]")
            return None
    
    def process_voice_with_screenshot(self, voice_text: str, 
                                     capture_screenshot: bool = True) -> Optional[str]:
        """
        Process voice input with optional screenshot context.
        
        Args:
            voice_text: Transcribed voice input
            capture_screenshot: Whether to capture screen
        
        Returns:
            Gemini's response or None
        """
        # Capture screenshot if enabled
        screenshot_bytes = None
        if capture_screenshot and self.config.screenshot_enabled:
            screenshot_bytes = self.capture_screenshot()
        
        # Send to Gemini
        response = self.send_to_gemini(voice_text, screenshot_bytes)
        
        # Speak response if TTS available
        if response and self.tts_engine:
            try:
                self.tts_engine.speak(response, blocking=False)
                self.logger.info("TTS response started")
            except Exception as e:
                self.logger.error(f"TTS error: {e}")
        
        return response
    
    def get_response(self, timeout: float = 0.1) -> Optional[Dict]:
        """
        Get Gemini response from queue.
        
        Returns:
            Response dict or None
        """
        try:
            return self.response_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def configure_screenshot(self, enabled: bool):
        """Enable/disable screenshot capture."""
        self.config.screenshot_enabled = enabled
        self.logger.info(f"Screenshot: {'enabled' if enabled else 'disabled'}")
    
    def configure_video(self, enabled: bool):
        """Enable/disable video recording."""
        self.config.video_enabled = enabled
        self.logger.info(f"Video recording: {'enabled' if enabled else 'disabled'}")
