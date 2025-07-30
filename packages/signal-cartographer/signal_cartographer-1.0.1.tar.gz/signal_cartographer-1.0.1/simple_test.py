#!/usr/bin/env python3
"""
Minimal textual test to debug content visibility
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.screen import Screen

class SimpleScreen(Screen):
    """Simple screen with just static widgets"""
    
    def compose(self) -> ComposeResult:
        """Compose the screen"""
        yield Header(show_clock=True)
        yield Static("[bold cyan]Test Pane 1[/bold cyan]\nThis is test content\nLine 2\nLine 3", id="pane1")
        yield Static("[bold yellow]Test Pane 2[/bold yellow]\nMore test content\n[red]Red text[/red]", id="pane2")
        yield Footer()

class SimpleApp(App):
    """Simple test app"""
    
    CSS = """
    #pane1, #pane2 {
        border: solid #58a6ff;
        margin: 1;
        padding: 1;
        height: 50%;
        background: #0d1117;
        color: #c9d1d9;
    }
    
    Header {
        background: #21262d;
        color: #7c3aed;
    }
    
    Footer {
        background: #21262d;
        color: #8b949e;
    }
    """
    
    async def on_mount(self) -> None:
        """Set up the application"""
        await self.push_screen(SimpleScreen())

if __name__ == "__main__":
    app = SimpleApp()
    app.run()
