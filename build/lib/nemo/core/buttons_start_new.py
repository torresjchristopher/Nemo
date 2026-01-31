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
            active_voice_engine.stop_transcription()
            # Get final result
            result = active_voice_engine.get_transcription(timeout=0.5)
            if result:
                console.print(f"[green]✓ Final text:[/green] {result.get('text', '')}")
            active_voice_engine = None
    
    def on_gemini_hold_start(event):
        """RIGHT ALT pressed - start Gemini listening"""
        console.print("\n[green bold]✓ RIGHT ALT HELD - Gemini Voice AI[/green bold]")
        console.print("[yellow]🎤 Speak to Gemini...[/yellow]")
    
    def on_gemini_hold_end(event):
        """RIGHT ALT released - Gemini done"""
        console.print("[dim][Gemini listening ended][/dim]")
    
    def on_rewind(event):
        console.print("\n[yellow]⏮️  Rewind - inferring past 5 seconds...[/yellow]")
    
    def on_forward(event):
        console.print("\n[yellow]⏭️  Forward - predicting next action...[/yellow]")
    
    # Register callbacks
    listener.register_callback('tts_hold_start', on_tts_hold_start)
    listener.register_callback('tts_hold_end', on_tts_hold_end)
    listener.register_callback('gemini_hold_start', on_gemini_hold_start)
    listener.register_callback('gemini_hold_end', on_gemini_hold_end)
    listener.register_callback('rewind', on_rewind)
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
