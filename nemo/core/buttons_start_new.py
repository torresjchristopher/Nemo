"""
New buttons start command with KeyboardHotkeyListener support.
This replaces the old pynput-based implementation.
"""

import time
import importlib.util
from pathlib import Path
from rich.console import Console

console = Console()

# Pre-load voice input at module level using importlib
systems_path = None
VoiceInputEngine = None
VoiceInputConfig = None
GeminiHandler = None
TemporalRewindEngine = None

def _load_voice_input():
    """Load voice input engine on demand"""
    global systems_path, VoiceInputEngine, VoiceInputConfig
    
    if VoiceInputEngine is not None:
        return  # Already loaded
    
    try:
        nemo_package_path = Path(__file__).parent.parent
        systems_path = nemo_package_path / "systems" / "task-screen-simulator"
        
        spec_voice = importlib.util.spec_from_file_location(
            "voice_input_module",
            str(systems_path / "voice_input.py")
        )
        if spec_voice and spec_voice.loader:
            voice_module = importlib.util.module_from_spec(spec_voice)
            spec_voice.loader.exec_module(voice_module)
            VoiceInputEngine = voice_module.VoiceInputEngine
            VoiceInputConfig = voice_module.VoiceInputConfig
    except Exception as e:
        console.print(f"[dim]Voice input load error: {e}[/dim]")

def _load_gemini():
    """Load Gemini handler on demand"""
    global systems_path, GeminiHandler
    
    if GeminiHandler is None:
        try:
            nemo_package_path = Path(__file__).parent.parent
            systems_path = nemo_package_path / "systems" / "task-screen-simulator"
            
            spec_gemini = importlib.util.spec_from_file_location(
                "gemini_handler_module",
                str(systems_path / "gemini_handler.py")
            )
            if spec_gemini and spec_gemini.loader:
                gemini_module = importlib.util.module_from_spec(spec_gemini)
                spec_gemini.loader.exec_module(gemini_module)
                GeminiHandler = gemini_module.GeminiHandler
        except Exception as e:
            console.print(f"[dim]Gemini load error: {e}[/dim]")
            return None
    
    if GeminiHandler:
        try:
            import os
            api_key = os.environ.get('GEMINI_API_KEY')
            if not api_key:
                return None
            
            from gemini_handler_module import GeminiConfig
            config = GeminiConfig(api_key=api_key)
            return GeminiHandler(config=config, tts_engine=tts_engine)
        except Exception as e:
            return None
    return None

def _load_rewind():
    """Load temporal rewind engine on demand"""
    global systems_path, TemporalRewindEngine
    
    if TemporalRewindEngine is None:
        try:
            nemo_package_path = Path(__file__).parent.parent
            systems_path = nemo_package_path / "systems" / "task-screen-simulator"
            
            spec_rewind = importlib.util.spec_from_file_location(
                "temporal_rewind_module",
                str(systems_path / "temporal_rewind.py")
            )
            if spec_rewind and spec_rewind.loader:
                rewind_module = importlib.util.module_from_spec(spec_rewind)
                spec_rewind.loader.exec_module(rewind_module)
                TemporalRewindEngine = rewind_module.TemporalRewindEngine
        except Exception as e:
            console.print(f"[dim]Rewind load error: {e}[/dim]")
            return None
    
    if TemporalRewindEngine:
        return TemporalRewindEngine(window_size_seconds=300)
    return None

def buttons_start_new():
    """Start button listeners daemon with keyboard library support"""
    try:
        # Find the nemo repo location
        nemo_package_path = Path(__file__).parent.parent
        systems_path = nemo_package_path / "systems" / "task-screen-simulator"
        
        # Load keyboard_hotkeys (primary - better Windows support)
        spec_kb = importlib.util.spec_from_file_location(
            "keyboard_hotkeys",
            str(systems_path / "keyboard_hotkeys.py")
        )
        KeyboardHotkeyListener = None
        if spec_kb and spec_kb.loader:
            try:
                kb_module = importlib.util.module_from_spec(spec_kb)
                spec_kb.loader.exec_module(kb_module)
                KeyboardHotkeyListener = kb_module.KeyboardHotkeyListener
            except Exception as e:
                console.print(f"[dim]Keyboard library unavailable: {e}[/dim]")
        
        # Load tts_engine
        spec_tts = importlib.util.spec_from_file_location(
            "tts_engine",
            str(systems_path / "tts_engine.py")
        )
        if not spec_tts or not spec_tts.loader:
            raise ImportError("Could not load tts_engine")
        
        tts_module = importlib.util.module_from_spec(spec_tts)
        spec_tts.loader.exec_module(tts_module)
        TTSEngine = tts_module.TTSEngine
        
    except Exception as e:
        console.print(f"\n[red]✗ Failed to import required modules: {e}[/red]\n")
        import traceback
        traceback.print_exc()
        return
    
    console.print("\n[magenta bold]Starting 4-Button Control System...[/magenta bold]\n")
    console.print("[cyan]Initializing components...[/cyan]")
    
    # Initialize listener - must use KeyboardHotkeyListener
    try:
        if KeyboardHotkeyListener is None:
            console.print("[red]✗ Keyboard library not available. Run PowerShell as Administrator.[/red]")
            return
        
        listener = KeyboardHotkeyListener()
        tts_engine = TTSEngine()
        console.print("[green]✓ Components initialized[/green]")
    except Exception as e:
        console.print(f"[red]✗ Failed to initialize: {e}[/red]\n")
        import traceback
        traceback.print_exc()
        return
    
    # State for tracking active recording
    active_voice_engine = None
    recording = False
    
    # Define callbacks for hold-based recording
    def on_tts_hold_start(event):
        """RIGHT SHIFT pressed - start listening"""
        nonlocal active_voice_engine, recording
        
        if recording:
            return  # Already recording
        
        recording = True
        console.print("\n[green bold]✓ RIGHT SHIFT HELD - Recording...[/green bold]")
        console.print("[yellow]🎤 Speak now (release RIGHT SHIFT to end)[/yellow]")
        
        # Load voice input on first use
        _load_voice_input()
        
        if VoiceInputEngine is None:
            console.print("[red]✗ Voice input not available[/red]")
            recording = False
            return
        
        # Transcription callback for live display
        def show_transcription(text: str, is_final: bool):
            if is_final:
                console.print(f"\n[green]✓ You said:[/green] {text}")
            else:
                # Live partial transcription
                import sys
                sys.stdout.write(f"\r[cyan]Transcribing: {text}[/cyan]")
                sys.stdout.flush()
        
        try:
            config = VoiceInputConfig()
            active_voice_engine = VoiceInputEngine(
                config=config,
                tts_engine=tts_engine,
                transcription_callback=show_transcription
            )
            
            # Try to read highlighted text first
            highlighted = active_voice_engine.read_highlighted_text()
            if not highlighted:
                # Listen to microphone (will record until stopped)
                active_voice_engine.listen_and_transcribe()
        except Exception as e:
            console.print(f"[red]✗ Error: {e}[/red]")
            recording = False
    
    def on_tts_hold_end(event):
        """RIGHT SHIFT released - stop listening"""
        nonlocal active_voice_engine, recording
        
        if not recording:
            return
        
        recording = False
        console.print("\n[dim][Recording stopped][/dim]")
        
        if active_voice_engine:
            try:
                # Stop the transcription thread
                active_voice_engine.stop_transcription()
                
                # Wait for result (up to 2 seconds)
                result = active_voice_engine.get_transcription(timeout=2.0)
                
                if result:
                    text = result.get('text', '')
                    console.print(f"[green]✓ Final text:[/green] {text}")
                else:
                    console.print("[dim][No speech detected - try again][/dim]")
            except Exception as e:
                console.print(f"[red]Error getting result: {e}[/red]")
            finally:
                active_voice_engine = None
    
    def on_gemini_hold_start(event):
        """RIGHT ALT pressed - start Gemini listening"""
        nonlocal active_voice_engine, recording
        
        if recording:
            return
        
        recording = True
        console.print("\n[green bold]✓ RIGHT ALT HELD - Gemini Voice AI[/green bold]")
        console.print("[yellow]🎤 Speak to Gemini (with optional screenshot)[/yellow]")
        
        # Load voice input and Gemini
        _load_voice_input()
        gemini_handler = _load_gemini()
        
        if VoiceInputEngine is None:
            console.print("[red]✗ Voice input not available[/red]")
            recording = False
            return
        
        if gemini_handler is None:
            console.print("[red]✗ Gemini not configured (set GEMINI_API_KEY)[/red]")
            recording = False
            return
        
        # Transcription callback
        def show_transcription(text: str, is_final: bool):
            if is_final:
                console.print(f"\n[cyan]You said:[/cyan] {text}")
            else:
                import sys
                sys.stdout.write(f"\r[cyan]Transcribing: {text}[/cyan]")
                sys.stdout.flush()
        
        try:
            config = VoiceInputConfig()
            active_voice_engine = VoiceInputEngine(
                config=config,
                tts_engine=tts_engine,
                transcription_callback=show_transcription
            )
            
            # Listen to microphone
            active_voice_engine.listen_and_transcribe()
        except Exception as e:
            console.print(f"[red]✗ Error: {e}[/red]")
            recording = False
    
    def on_gemini_hold_end(event):
        """RIGHT ALT released - send to Gemini"""
        nonlocal active_voice_engine, recording
        
        if not recording:
            return
        
        recording = False
        console.print("\n[dim][Sending to Gemini...][/dim]")
        
        if active_voice_engine:
            try:
                # Stop recording
                active_voice_engine.stop_transcription()
                
                # Get transcribed text
                result = active_voice_engine.get_transcription(timeout=2.0)
                
                if result:
                    voice_text = result.get('text', '')
                    console.print(f"[green]✓ Transcribed:[/green] {voice_text}")
                    
                    # Load Gemini and send
                    gemini_handler = _load_gemini()
                    if gemini_handler and gemini_handler.model:
                        # Process with optional screenshot
                        response = gemini_handler.process_voice_with_screenshot(
                            voice_text,
                            capture_screenshot=True
                        )
                        if response:
                            console.print(f"\n[cyan]Gemini:[/cyan] {response}")
                    else:
                        console.print("[dim][Gemini API key not configured][/dim]")
                else:
                    console.print("[dim][No speech detected][/dim]")
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
            finally:
                active_voice_engine = None
    
    def on_rewind(event):
        """RIGHT ALT + LEFT ARROW - REWIND SCREEN"""
        console.print("\n[magenta bold]⏮️  REWIND - Rewinding screen...[/magenta bold]")
        
        try:
            from nemo.systems.task_screen_simulator.rewind_engine_v3 import get_rewind_engine
            rewind = get_rewind_engine()
            rewind.rewind_continuous()
            console.print(f"[magenta]✓ Rewind continuous! Stack size: {rewind.get_stack_size()}[/magenta]")
        except Exception as e:
            console.print(f"[red]✗ Rewind error: {e}[/red]")
    
    def on_rewind_start(event):
        """RIGHT ALT + LEFT - Start continuous rewind"""
        console.print("\n[magenta bold]⏮️  REWIND STARTED[/magenta bold]")
    
    def on_rewind_stop(event):
        """RIGHT ALT released - Stop continuous rewind"""
        console.print("[magenta]⏮️  REWIND COMPLETE[/magenta]")
        
        try:
            from nemo.systems.task_screen_simulator.rewind_engine_v3 import get_rewind_engine
            rewind = get_rewind_engine()
            rewind.rewind_stop()
        except Exception:
            pass
    
    def on_forward(event):
        console.print("\n[yellow]⏭️  Forward - predicting next action...[/yellow]")
        console.print("[dim][FORWARD prediction coming soon - machine learning integration][/dim]")
    
    # Register callbacks
    listener.register_callback('tts_hold_start', on_tts_hold_start)
    listener.register_callback('tts_hold_end', on_tts_hold_end)
    listener.register_callback('gemini_hold_start', on_gemini_hold_start)
    listener.register_callback('gemini_hold_end', on_gemini_hold_end)
    listener.register_callback('rewind_start', on_rewind_start)
    listener.register_callback('rewind_stop', on_rewind_stop)
    listener.register_callback('forward', on_forward)
    
    console.print("\n[cyan]Listening for hotkeys:[/cyan]\n")
    console.print("  🎤 [yellow]RIGHT ALT[/yellow]           → Gemini Voice AI")
    console.print("  🔊 [yellow]RIGHT SHIFT[/yellow]         → Speech-to-Text + Read Highlighted")
    console.print("  ⏮️  [yellow]RIGHT ALT + ← ARROW[/yellow]  → Rewind (infer past 5s)")
    console.print("  ⏭️  [yellow]RIGHT ALT + → ARROW[/yellow]  → Forward (predict next 5s)")
    console.print("\n[dim][Ctrl+C to stop][/dim]\n")
    
    # Start listener
    try:
        listener.start()
        console.print("[green]✓ System hotkeys active[/green]\n")
    except Exception as e:
        console.print(f"[red]✗ Failed to start listener: {e}[/red]\n")
        import traceback
        traceback.print_exc()
        return
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        try:
            listener.stop()
        except:
            pass
        console.print("\n[yellow]Shutting down...[/yellow]\n")


if __name__ == "__main__":
    buttons_start_new()
