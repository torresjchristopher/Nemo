#!/usr/bin/env python3
"""
Standalone test interface for Nemo RIGHT SHIFT hotkey.
Full voice input + speech-to-text experience.
Run this to test the complete workflow.
"""

import time
import sys
import importlib.util
from pathlib import Path

# Add nemo to path
nemo_repo = Path(__file__).parent
sys.path.insert(0, str(nemo_repo))

from rich.console import Console
from rich.panel import Panel

console = Console()

# Load components via importlib
systems_path = nemo_repo / "nemo" / "systems" / "task-screen-simulator"

# Load KeyboardHotkeyListener
spec_kb = importlib.util.spec_from_file_location(
    "keyboard_hotkeys",
    str(systems_path / "keyboard_hotkeys.py")
)
kb_module = importlib.util.module_from_spec(spec_kb)
spec_kb.loader.exec_module(kb_module)
KeyboardHotkeyListener = kb_module.KeyboardHotkeyListener

# Load TTSEngine
spec_tts = importlib.util.spec_from_file_location(
    "tts_engine",
    str(systems_path / "tts_engine.py")
)
tts_module = importlib.util.module_from_spec(spec_tts)
spec_tts.loader.exec_module(tts_module)
TTSEngine = tts_module.TTSEngine

# Load VoiceInputEngine
spec_voice = importlib.util.spec_from_file_location(
    "voice_input",
    str(systems_path / "voice_input.py")
)
voice_module = importlib.util.module_from_spec(spec_voice)
spec_voice.loader.exec_module(voice_module)
VoiceInputEngine = voice_module.VoiceInputEngine
VoiceInputConfig = voice_module.VoiceInputConfig


def main():
    """Run standalone test interface"""
    
    console.print(Panel(
        "[magenta bold]🎤 Nemo RIGHT SHIFT Test Interface[/magenta bold]\n"
        "[cyan]Test the complete voice input experience[/cyan]",
        border_style="magenta"
    ))
    
    console.print("\n[yellow]Initializing...[/yellow]")
    
    # Initialize components
    try:
        listener = KeyboardHotkeyListener()
        tts_engine = TTSEngine()
        console.print("[green]✓ Components ready[/green]\n")
    except Exception as e:
        console.print(f"[red]✗ Failed to initialize: {e}[/red]")
        return
    
    # Define callback for RIGHT SHIFT
    def on_right_shift(event):
        """Handle RIGHT SHIFT press - the complete workflow"""
        console.print("\n" + "=" * 60)
        console.print("[green bold]✓ RIGHT SHIFT ACTIVATED[/green bold]")
        console.print("[cyan]Smart Voice Mode[/cyan]")
        console.print("=" * 60 + "\n")
        
        # Step 1: Check for highlighted text
        console.print("[yellow]Step 1: Checking for highlighted text...[/yellow]")
        voice_engine = VoiceInputEngine(
            config=VoiceInputConfig(),
            tts_engine=tts_engine,
            transcription_callback=None  # Temp - set below
        )
        
        if voice_engine.read_highlighted_text():
            console.print("[green]✓ Read highlighted text[/green]\n")
            return
        
        console.print("[dim]No highlighted text found[/dim]\n")
        
        # Step 2: Listen to microphone
        console.print("[yellow]Step 2: Listening to microphone (5 seconds)...[/yellow]")
        console.print("[dim]🎤 Speak now... (you'll see live transcription below)\n[/dim]")
        
        # Define transcription display callback
        def show_transcription(text: str, is_final: bool):
            if is_final:
                console.print(f"\n[green bold]✓ Final transcription:[/green bold]")
                console.print(f"[cyan]{text}[/cyan]\n")
            else:
                # Live partial transcription
                console.print(f"[yellow]{text}[/yellow]", end='\r', flush=True)
        
        try:
            config = VoiceInputConfig()
            voice_engine = VoiceInputEngine(
                config=config,
                tts_engine=tts_engine,
                transcription_callback=show_transcription
            )
            
            # Start listening
            voice_engine.listen_and_transcribe()
            
            # Wait for transcription to complete
            time.sleep(config.mic_timeout + 1)
            result = voice_engine.get_transcription(timeout=1.0)
            
            if result:
                console.print(f"\n[green bold]✓ You said:[/green bold] {result['text']}")
                console.print("[dim]This text is now available for Nemo to process...[/dim]\n")
            else:
                console.print("[yellow][No speech detected][/yellow]\n")
        
        except Exception as e:
            console.print(f"\n[red]✗ Error: {e}[/red]\n")
            import traceback
            traceback.print_exc()
    
    def on_right_alt(event):
        """Handle RIGHT ALT press"""
        console.print("\n[green bold]✓ RIGHT ALT ACTIVATED[/green bold]")
        console.print("[yellow]Gemini Voice AI mode[/yellow]")
        try:
            tts_engine.speak("Gemini voice mode", blocking=False)
        except:
            pass
    
    # Register callbacks
    listener.register_callback('tts_tap', on_right_shift)
    listener.register_callback('gemini_tap', on_right_alt)
    
    # Display instructions
    console.print("\n[cyan bold]Ready to test![/cyan bold]\n")
    console.print("  [yellow]RIGHT SHIFT[/yellow]    → Test speech-to-text + read highlighted")
    console.print("  [yellow]RIGHT ALT[/yellow]      → Test Gemini voice AI")
    console.print("  [yellow]Ctrl+C[/yellow]        → Exit\n")
    console.print("[dim]Make sure PowerShell is running as Administrator![/dim]\n")
    
    # Start listener
    try:
        listener.start()
        console.print("[green]✓ Hotkeys active - press RIGHT SHIFT to test[/green]\n")
        
        # Keep running
        while True:
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        try:
            listener.stop()
        except:
            pass
        console.print("\n[yellow]Shutting down...[/yellow]\n")
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
