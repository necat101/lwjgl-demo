#!/usr/bin/env python3
"""
LWJGL Dynamic Configuration Test Suite

Demonstrates rapid testing without Maven rebuilds.
"""

import subprocess
import sys
import time
from pathlib import Path

def run_test(name, args, description):
    print("\n" + "=" * 70)
    print(f"TEST: {name}")
    print(f"Description: {description}")
    print("=" * 70)
    
    cmd = [sys.executable, "lwjgl_launcher.py"] + args
    print(f"\nLaunching in 2 seconds... (Ctrl+C to skip)")
    try:
        time.sleep(2)
    except KeyboardInterrupt:
        print("⏭️  Skipped!"); return True
    
    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent)
        print(f"✅ Test completed" if result.returncode == 0 else f"⚠️  Exit code {result.returncode}")
        return True
    except KeyboardInterrupt:
        print(f"\n⏭️  Interrupted"); return True
    except Exception as e:
        print(f"❌ Failed: {e}"); return False

def main():
    print("=" * 70)
    print("LWJGL Dynamic Configuration Test Suite")
    print("=" * 70)
    print("\nThis demonstrates testing different configurations")
    print("without rebuilding. Close window or press ESC to continue.\n")
    
    tests = [
        ("Default", [], "Baseline 800x600"),
        ("Performance", ["--preset", "performance"], "No vsync, no animation"),
        ("HD", ["--preset", "hd"], "1280x720"),
        ("Purple Theme", ["--preset", "purple"], "Purple with fast animation"),
        ("Minimal", ["--preset", "minimal"], "400x300 quick test"),
        ("Custom", ["--width", "1024", "--height", "768", "--clear-r", "0.2", 
                   "--clear-g", "0.3", "--clear-b", "0.1"], "Custom green tint"),
        ("Stress", ["--preset", "stress"], "1080p, no vsync, 5x speed"),
    ]
    
    print(f"Running {len(tests)} tests...\n")
    try:
        input("Press Enter to begin...")
    except KeyboardInterrupt:
        print("\nCancelled."); return 0
    
    completed = 0
    for name, args, desc in tests:
        if run_test(name, args, desc):
            completed += 1
        if completed < len(tests):
            print("\nNext test in 3 seconds... (Ctrl+C to stop)")
            try:
                time.sleep(3)
            except KeyboardInterrupt:
                break
    
    print("\n" + "=" * 70)
    print(f"Complete: {completed}/{len(tests)} tests")
    print("=" * 70)
    print("\n✅ All tested without Maven rebuilds!")
    print("✅ Command-line flags enable rapid iteration")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(130)
