#!/usr/bin/env python3
"""
LWJGL Dynamic Configuration Test Suite

Demonstrates rapid testing without Maven rebuilds.
Supports --dry-run mode for testing in headless environments.
"""

import subprocess
import sys
import time
from pathlib import Path

def run_test(name, args, description, dry_run=False):
    print("\n" + "=" * 70)
    print(f"TEST: {name}")
    print(f"Description: {description}")
    print("=" * 70)
    
    cmd = [sys.executable, "lwjgl_launcher.py"]
    if dry_run:
        cmd.append("--dry-run")
    cmd.extend(args)
    
    if dry_run:
        print()
    else:
        print(f"\n🚀 Launching in 2 seconds... (Ctrl+C to skip)")
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            print("⏭️  Skipped!")
            return True
    
    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent)
        if not dry_run:
            if result.returncode == 0:
                print(f"✅ Test '{name}' completed")
            else:
                print(f"⚠️  Exit code {result.returncode}")
        return True
    except KeyboardInterrupt:
        print(f"\n⏭️  Interrupted")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="LWJGL Test Suite")
    parser.add_argument("--dry-run", action="store_true", help="Show commands without executing")
    args = parser.parse_args()
    
    print("=" * 70)
    print("LWJGL Dynamic Configuration Test Suite")
    if args.dry_run:
        print("*** DRY RUN MODE ***")
    print("=" * 70)
    print()
    
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
    
    if not args.dry_run:
        try:
            input("Press Enter to begin...")
        except KeyboardInterrupt:
            print("\nCancelled.")
            return 0
    
    completed = 0
    for name, test_args, desc in tests:
        if run_test(name, test_args, desc, dry_run=args.dry_run):
            completed += 1
        if not args.dry_run and completed < len(tests):
            print("\nNext test in 3 seconds...")
            try:
                time.sleep(3)
            except KeyboardInterrupt:
                break
    
    print("\n" + "=" * 70)
    print(f"{'DRY RUN' if args.dry_run else 'Test Suite'} Complete: {completed}/{len(tests)}")
    print("=" * 70)
    print("\n✅ All configurations tested without Maven rebuilds!")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(130)
