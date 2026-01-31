"""
GeminiVoiceKey - Gemini Voice AI with Screenshot Context

RIGHT ALT hotkey - Hold to record question + capture screen, release to query Gemini.
Ideal for: Screen-aware Q&A, contextual help, AI assistance with full context.

Uses:
- AudioCapture tool (voice recording)
- ScreenCapture tool (screenshot)
- google-generativeai (Gemini Pro Vision)
"""

from nemo.tools import NemoKey, AudioCapture, ScreenCapture
import google.generativeai as genai
import base64
from typing import Optional
import speech_recognition as sr


class GeminiVoiceKey(NemoKey):
    """
    Gemini Voice AI Key
    
    Hold RIGHT ALT to record question + capture screenshot.
    Release to send to Gemini Pro Vision and display response.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            key_name="Gemini Voice AI",
            key_combo="right alt",
            description="Hold to ask Gemini about your screen"
        )
        self.audio = AudioCapture(energy_threshold=300, timeout=5)
        self.screen = ScreenCapture()
        self.recognizer = sr.Recognizer()
        
        # Initialize Gemini
        if api_key:
            genai.configure(api_key=api_key)
        
        # State
        self.recording = False
        self.last_response = None
        self.last_screenshot = None
    
    def on_press(self) -> None:
        """Called when RIGHT ALT pressed"""
        # Capture screenshot immediately
        self.last_screenshot = self.screen.capture()
        
        # Start recording voice
        self.audio.start_recording()
        self.recording = True
    
    def on_hold(self, duration: float) -> None:
        """Called while RIGHT ALT held"""
        # Optional: Show recording indicator
        pass
    
    def on_release(self, total_duration: float) -> Optional[str]:
        """Called when RIGHT ALT released - query Gemini"""
        self.audio.stop_recording()
        self.recording = False
        
        if total_duration < 0.3:
            # Too short
            return None
        
        # Transcribe voice question
        question = self._transcribe_audio()
        if not question:
            self._notify("No speech detected")
            return None
        
        # Query Gemini with context
        response = self._query_gemini(question, self.last_screenshot)
        
        if response:
            self.last_response = response
            self._display_response(response)
            return response
        else:
            self._notify("Gemini query failed")
            return None
    
    def _transcribe_audio(self) -> Optional[str]:
        """Transcribe audio to text"""
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=5)
            
            # Try Google first
            try:
                text = self.recognizer.recognize_google(audio, language='en-US')
                return text
            except:
                # Fall back to Bing
                try:
                    text = self.recognizer.recognize_bing(audio, language='en-US')
                    return text
                except:
                    return None
        except:
            return None
    
    def _query_gemini(self, question: str, screenshot_bytes: Optional[bytes]) -> Optional[str]:
        """Send question + screenshot to Gemini Pro Vision"""
        try:
            model = genai.GenerativeModel('gemini-pro-vision')
            
            # Convert screenshot to base64
            if screenshot_bytes:
                screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
                image_data = genai.types.ImageData(
                    mime_type="image/png",
                    data=screenshot_b64
                )
                
                # Create prompt with context
                prompt = f"""User is asking about what they see on their screen.
                
User question: {question}

Context: The screenshot above shows the current state of the user's screen. 
Please analyze it and answer their question directly and concisely.
"""
                
                response = model.generate_content([prompt, image_data])
            else:
                # No screenshot, just answer the question
                response = model.generate_content(question)
            
            return response.text
        except Exception as e:
            print(f"[GEMINI ERROR] {e}")
            return None
    
    def _display_response(self, response: str) -> None:
        """Display Gemini response to user"""
        print("\n" + "="*60)
        print("[NEMO GEMINI]")
        print("="*60)
        print(response)
        print("="*60 + "\n")
    
    def _notify(self, message: str) -> None:
        """Notify user of status"""
        print(f"[GEMINI] {message}")
    
    def get_status(self) -> dict:
        """Return status"""
        status = super().get_status()
        status.update({
            'recording': self.recording,
            'last_response': self.last_response[:100] if self.last_response else None,
            'has_screenshot': self.last_screenshot is not None,
        })
        return status
