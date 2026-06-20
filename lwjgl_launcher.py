#!/usr/bin/env python3
"""
LWJGL Demo Python Launcher

A Python wrapper for the LWJGL demo that provides easy configuration
and dynamic testing without rebuilding with Maven.

Usage:
    python3 lwjgl_launcher.py [options]
    python3 lwjgl_launcher.py --preset performance
    python3 lwjgl_launcher.py --width 1920 --height 1080 --fullscreen
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path

class LWJGLLauncher:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.jar_path = self.project_dir / "target" / "lwjgl-demo-1.0-SNAPSHOT.jar"
        self.lib_dir = self.project_dir / "target" / "lib"
        
        self.presets = {
            "default": {"width": 800, "height": 600, "vsync": 1, "animate": 1},
            "performance": {"width": 800, "height": 600, "vsync": 0, "animate": 0, "title": "LWJGL Performance Test"},
            "hd": {"width": 1280, "height": 720, "title": "LWJGL HD Demo"},
            "fullhd": {"width": 1920, "height": 1080, "title": "LWJGL Full HD"},
            "fullscreen": {"fullscreen": True, "vsync": 1, "title": "LWJGL Fullscreen"},
            "purple": {"clear-r": 0.3, "clear-g": 0.1, "clear-b": 0.5, "animate-speed": 2.0, "title": "Purple Theme"},
            "minimal": {"width": 400, "height": 300, "animate": 0, "title": "Minimal Test"},
            "stress": {"width": 1920, "height": 1080, "vsync": 0, "animate": 1, "animate-speed": 5.0, "title": "Stress Test"}
        }
    
    def check_build(self):
        if not self.jar_path.exists():
            print("🔨 Building project...")
            result = subprocess.run(["mvn", "clean", "package", "-q"], cwd=self.project_dir, capture_output=True)
            if result.returncode != 0:
                print("❌ Build failed!"); return False
            print("✅ Build successful!")
        return True
    
    def build_classpath(self):
        parts = [str(self.jar_path)]
        if self.lib_dir.exists():
            parts.extend(str(p) for p in self.lib_dir.glob("*.jar"))
        return os.pathsep.join(parts)
    
    def launch(self, app_args=None):
        if not self.check_build(): return False
        cmd = ["java", "-cp", self.build_classpath(), "com.necat.lwjgl.HelloLWJGL"] + (app_args or [])
        print(f"🚀 Launching: {' '.join(app_args) if app_args else '(defaults)'}")
        try:
            subprocess.run(cmd, cwd=self.project_dir)
            return True
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted"); return False
    
    def list_presets(self):
        print("Available presets:"); print("=" * 60)
        for name, config in self.presets.items():
            print(f"\n{name}:"); [print(f"  --{k} {v}") for k, v in config.items()]
    
    def get_preset_args(self, preset_name):
        if preset_name not in self.presets: return None
        args = []
        for k, v in self.presets[preset_name].items():
            args.append(f"--{k}")
            if v is not True: args.append(str(v))
        return args

def main():
    parser = argparse.ArgumentParser(description="LWJGL Demo Launcher")
    parser.add_argument("--preset", "-p", help="Use preset configuration")
    parser.add_argument("--list-presets", action="store_true", help="List presets")
    parser.add_argument("--build-only", action="store_true", help="Only build")
    args, unknown = parser.parse_known_args()
    
    launcher = LWJGLLauncher()
    if args.list_presets: launcher.list_presets(); return 0
    if args.build_only: return 0 if launcher.check_build() else 1
    
    app_args = []
    if args.preset:
        preset_args = launcher.get_preset_args(args.preset)
        if not preset_args: return 1
        app_args.extend(preset_args)
    app_args.extend([a for a in unknown if a != "--"])
    
    return 0 if launcher.launch(app_args) else 1

if __name__ == "__main__":
    sys.exit(main())
