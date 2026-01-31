"""
Nemo Main - Application entry point

Initializes NemoEngine, KeyboardListener, and all 5 keys.
Starts the system-level keyboard listener.
"""

from nemo.tools import NemoEngine
from nemo.core import KeyboardListener
from nemo.keys.right_shift_stt import STTKey
from nemo.keys.right_alt_gemini import GeminiVoiceKey
from nemo.keys.right_alt_left_rewind import RewindKey
from nemo.keys.right_alt_right_forward import ForwardKey
from nemo.keys.right_alt_up_agent import AgentSynthesisKey
import os


class NemoApp:
    """
    Main Nemo Application
    
    Orchestrates:
    - NemoEngine (hotkey registry and routing)
    - KeyboardListener (system-level hotkey detection)
    - All 5 keys (STT, Gemini, Rewind, Forward, Agent)
    """
    
    def __init__(self):
        """Initialize Nemo app"""
        self.engine = NemoEngine()
        self.listener = KeyboardListener(self.engine)
        self.running = False
        
        # Initialize Gemini API key if available
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        # Register all keys
        self._register_keys()
    
    def _register_keys(self) -> None:
        """Register all 5 keys with the engine"""
        print("[NEMO] Registering keys...")
        
        # STT Key
        stt_key = STTKey()
        self.engine.register_key(stt_key)
        
        # Gemini Key
        gemini_key = GeminiVoiceKey(api_key=self.gemini_api_key)
        self.engine.register_key(gemini_key)
        
        # Rewind Key
        rewind_key = RewindKey()
        self.engine.register_key(rewind_key)
        
        # Forward Key (proprietary stub)
        forward_key = ForwardKey()
        self.engine.register_key(forward_key)
        
        # Agent Key (proprietary stub)
        agent_key = AgentSynthesisKey()
        self.engine.register_key(agent_key)
        
        print(f"[NEMO] Registered {len(self.engine.get_all_keys())} keys")
    
    def start(self) -> None:
        """Start Nemo"""
        if self.running:
            print("[NEMO] Already running")
            return
        
        self.running = True
        print("[NEMO] Starting...")
        print("[NEMO] System hotkeys active:")
        print("  RIGHT SHIFT      → Speech-to-Text")
        print("  RIGHT ALT        → Gemini Voice AI")
        print("  RIGHT ALT + LEFT → Rewind")
        print("  RIGHT ALT + RIGHT → Forward")
        print("  RIGHT ALT + UP   → Agent Synthesis")
        print("\n[NEMO] Ready! Press Ctrl+C to exit.")
        
        # Start keyboard listener
        self.listener.start()
        
        # Keep running
        try:
            while self.running:
                import time
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self) -> None:
        """Stop Nemo"""
        self.running = False
        self.listener.stop()
        print("[NEMO] Stopped")
    
    def get_status(self) -> dict:
        """Get Nemo status"""
        return {
            'running': self.running,
            'engine': self.engine.get_status(),
            'listener': self.listener.get_status(),
        }


def main():
    """Main entry point"""
    app = NemoApp()
    app.start()


if __name__ == '__main__':
    main()
