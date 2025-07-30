#!/usr/bin/env python3
"""
Debug script to understand key event handling in Textual
"""

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Input, Static, RichLog
from textual.containers import Vertical
from textual.binding import Binding
from textual import events

class DebugInput(Input):
    """Input widget that logs all key events for debugging"""
    
    def __init__(self, **kwargs):
        super().__init__(placeholder="Type here and try Ctrl+C...", **kwargs)
        
    async def on_key(self, event: events.Key) -> None:
        """Log all key events"""
        app = self.app
        if hasattr(app, 'log_widget'):
            app.log_widget.write(f"🔍 Input widget received key: '{event.key}' (unicode: {event.unicode_key})")
        
        # Let's see what happens when we DON'T prevent default for ctrl keys
        if event.key.startswith("ctrl+"):
            app.log_widget.write(f"🚨 Ctrl key detected: {event.key} - NOT preventing default")
            # Do NOT call event.prevent_default() or return
            # Let it bubble up to the app
        else:
            # For non-ctrl keys, handle normally
            await super().on_key(event)

class DebugScreen(Screen):
    """Screen for debugging key events"""
    
    BINDINGS = [
        Binding("ctrl+c", "quit_debug", "Quit (Screen Level)"),
        Binding("ctrl+h", "help_debug", "Help (Screen Level)"),
        Binding("f1", "test_f1", "Test F1"),
    ]
    
    def compose(self) -> ComposeResult:
        """Compose the debug screen"""
        yield Static("🔧 Key Event Debug Tool", id="title")
        yield Static("Press keys to see events. Try Ctrl+C, Ctrl+H, F1...", id="instructions")
        yield DebugInput(id="debug_input")
        yield RichLog(id="debug_log")
    
    async def on_mount(self) -> None:
        """Initialize the debug screen"""
        self.log_widget = self.query_one("#debug_log")
        self.app.log_widget = self.log_widget
        self.log_widget.write("🚀 Debug session started")
        self.log_widget.write("🎯 Screen-level bindings: ctrl+c, ctrl+h, f1")
        
        # Focus the input
        input_widget = self.query_one("#debug_input")
        input_widget.focus()
    
    def action_quit_debug(self):
        """Quit action triggered by Ctrl+C"""
        self.log_widget.write("✅ SCREEN action_quit_debug called! Ctrl+C works at screen level!")
        self.app.exit()
    
    def action_help_debug(self):
        """Help action triggered by Ctrl+H"""
        self.log_widget.write("✅ SCREEN action_help_debug called! Ctrl+H works at screen level!")
    
    def action_test_f1(self):
        """Test action triggered by F1"""
        self.log_widget.write("✅ SCREEN action_test_f1 called! F1 works at screen level!")

class DebugApp(App):
    """App for debugging key events"""
    
    BINDINGS = [
        Binding("ctrl+c", "quit_app", "Quit (App Level)"),
        Binding("ctrl+h", "help_app", "Help (App Level)"),  
        Binding("f2", "test_f2", "Test F2"),
    ]
    
    def on_mount(self) -> None:
        """Initialize the app"""
        self.push_screen(DebugScreen())
    
    def action_quit_app(self):
        """Quit action at app level"""
        if hasattr(self, 'log_widget'):
            self.log_widget.write("✅ APP action_quit_app called! Ctrl+C works at app level!")
        self.exit()
    
    def action_help_app(self):
        """Help action at app level"""
        if hasattr(self, 'log_widget'):
            self.log_widget.write("✅ APP action_help_app called! Ctrl+H works at app level!")
    
    def action_test_f2(self):
        """Test action triggered by F2"""
        if hasattr(self, 'log_widget'):
            self.log_widget.write("✅ APP action_test_f2 called! F2 works at app level!")

if __name__ == "__main__":
    app = DebugApp()
    app.run() 