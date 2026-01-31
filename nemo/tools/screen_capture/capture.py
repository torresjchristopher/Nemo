"""
ScreenCapture Tool - Screenshot abstraction

Public tool for any key that needs screen images:
- RIGHT ALT (Gemini with screenshots)
- RIGHT ALT + UP (Agent synthesis)
"""

from typing import Optional, Tuple
from PIL import ImageGrab
import base64
import io


class ScreenCapture:
    """Handle screenshot capture for keys"""
    
    def __init__(self):
        """Initialize screenshot capture"""
        self.last_screenshot = None
        self.capture_enabled = True
    
    def capture(self) -> Optional[bytes]:
        """
        Capture current screen
        
        Returns:
            PNG image bytes or None
        """
        if not self.capture_enabled:
            return None
        
        try:
            screenshot = ImageGrab.grab()
            self.last_screenshot = screenshot
            
            # Convert to PNG bytes
            img_byte_arr = io.BytesIO()
            screenshot.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue()
        except Exception as e:
            print(f"[SCREEN CAPTURE ERROR] {e}")
            return None
    
    def capture_base64(self) -> Optional[str]:
        """
        Capture and return as base64 (for API calls)
        
        Returns:
            Base64 encoded PNG or None
        """
        screenshot_bytes = self.capture()
        if screenshot_bytes:
            return base64.b64encode(screenshot_bytes).decode('utf-8')
        return None
    
    def enable(self) -> None:
        """Enable screen capture"""
        self.capture_enabled = True
    
    def disable(self) -> None:
        """Disable screen capture"""
        self.capture_enabled = False
    
    def is_enabled(self) -> bool:
        """Check if capture is enabled"""
        return self.capture_enabled
    
    def get_dimensions(self) -> Tuple[int, int]:
        """Get screen dimensions"""
        try:
            screenshot = ImageGrab.grab()
            return screenshot.size
        except:
            return (0, 0)
