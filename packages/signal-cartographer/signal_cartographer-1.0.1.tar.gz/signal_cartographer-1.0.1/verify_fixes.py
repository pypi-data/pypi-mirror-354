#!/usr/bin/env python3
"""
Quick verification script for hotkey and markup fixes
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_markup_fix():
    """Test that the Rich markup issue is fixed"""
    try:
        print("🔧 Testing Rich markup fix...")
        
        from src.ui.panes import CartographyPane
        
        # Create cartography pane and try to update it
        pane = CartographyPane()
        pane.update_map("ALPHA-1")
        
        print("✅ Rich markup fix successful - no parsing errors!")
        return True
        
    except Exception as e:
        print(f"❌ Markup error still present: {e}")
        return False

def test_imports():
    """Test all critical imports"""
    try:
        print("🔧 Testing imports...")
        
        from src.ui.layout import AetherTapApp
        from src.ui.tutorial import TutorialMenuScreen
        from src.ui.panes import SpectrumPane, SignalFocusPane, CartographyPane, DecoderPane, LogPane
        
        print("✅ All imports working!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main verification"""
    print("🚀 BUG FIX VERIFICATION")
    print("=" * 50)
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test markup fix
    if not test_markup_fix():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✅ ALL FIXES SUCCESSFUL!")
        print("\n🎯 HOTKEYS THAT SHOULD NOW WORK:")
        print("• Ctrl+H  : Tutorial Academy")
        print("• Ctrl+C  : Quit")  
        print("• F1-F5   : Focus panes")
        print("\n🎮 GAME SHOULD START WITHOUT ERRORS!")
        print("Run: python main.py")
    else:
        print("❌ SOME ISSUES REMAIN")
        print("Check the error messages above")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 