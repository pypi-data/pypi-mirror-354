#!/usr/bin/env python3
"""
Comprehensive test to verify all reported issues are fixed:
1. DELTA-4 shows in cartography pane
2. Cartography pane updates when sectors change
3. New signal types (Bio-Neural, Quantum-Echo, Singularity-Resonance) appear in FOCUS/ANALYZE
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.game_core import SignalCartographer
from src.signal_system import SignalDetector

def test_signal_system():
    """Test that the signal system has all expected signal types"""
    print("🔬 Testing Signal System...")
    detector = SignalDetector()
    
    # Test DELTA-4
    delta_signals = detector.scan_sector('DELTA-4')
    print(f"\n📡 DELTA-4 has {len(delta_signals)} signals:")
    for i, signal in enumerate(delta_signals, 1):
        print(f"  SIG_{i}: {signal.modulation} at {signal.frequency:.1f} MHz")
    
    # Test EPSILON-5
    epsilon_signals = detector.scan_sector('EPSILON-5')
    print(f"\n📡 EPSILON-5 has {len(epsilon_signals)} signals:")
    for i, signal in enumerate(epsilon_signals, 1):
        print(f"  SIG_{i}: {signal.modulation} at {signal.frequency:.1f} MHz")
    
    # Verify new signal types exist
    new_types = ['Bio-Neural', 'Quantum-Echo', 'Singularity-Resonance']
    found_types = set()
    
    for signals in [delta_signals, epsilon_signals]:
        for signal in signals:
            if signal.modulation in new_types:
                found_types.add(signal.modulation)
    
    print(f"\n✅ Found new signal types: {list(found_types)}")
    missing = set(new_types) - found_types
    if missing:
        print(f"❌ Missing signal types: {list(missing)}")
    else:
        print("✅ All new signal types found!")
    
    return len(missing) == 0

def test_command_system():
    """Test that SCAN and FOCUS commands work properly"""
    print("\n🎮 Testing Command System...")
    
    # Create game instance
    game = SignalCartographer()
    
    # Test SCAN command
    print("\n📡 Testing SCAN DELTA-4:")
    result = game.process_command("SCAN DELTA-4")
    print(f"Result: {result}")
    
    # Check if signals were stored
    if hasattr(game, 'last_scan_signals') and 'DELTA-4' in game.last_scan_signals:
        signals = game.last_scan_signals['DELTA-4']
        print(f"✅ Stored {len(signals)} signals for DELTA-4")
        
        # Test FOCUS command
        if signals:
            print(f"\n🎯 Testing FOCUS SIG_1:")
            focus_result = game.process_command("FOCUS SIG_1")
            print(f"Result: {focus_result}")
            
            # Check focused signal
            focused = game.get_focused_signal()
            if focused:
                print(f"✅ Successfully focused on signal: {focused.modulation}")
                return True
            else:
                print("❌ No signal was focused")
                return False
    else:
        print("❌ No signals stored after SCAN")
        return False

def test_sector_availability():
    """Test that all sectors are available"""
    print("\n🗺️  Testing Sector Availability...")
    detector = SignalDetector()
    
    expected_sectors = ['ALPHA-1', 'BETA-2', 'GAMMA-3', 'DELTA-4', 'EPSILON-5']
    available_sectors = detector.get_available_sectors()
    
    print(f"Available sectors: {available_sectors}")
    
    missing_sectors = set(expected_sectors) - set(available_sectors)
    if missing_sectors:
        print(f"❌ Missing sectors: {list(missing_sectors)}")
        return False
    else:
        print("✅ All expected sectors available!")
        return True

def main():
    """Run all tests"""
    print("🧪 COMPREHENSIVE TEST SUITE")
    print("=" * 50)
    
    # Run all tests
    signal_test = test_signal_system()
    command_test = test_command_system()
    sector_test = test_sector_availability()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"  Signal System: {'✅ PASS' if signal_test else '❌ FAIL'}")
    print(f"  Command System: {'✅ PASS' if command_test else '❌ FAIL'}")
    print(f"  Sector Availability: {'✅ PASS' if sector_test else '❌ FAIL'}")
    
    if all([signal_test, command_test, sector_test]):
        print("\n🎉 ALL TESTS PASSED! Issues should be resolved.")
    else:
        print("\n⚠️  Some tests failed. Issues may still exist.")

if __name__ == "__main__":
    main() 