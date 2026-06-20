#!/usr/bin/env python3
"""
LWJGL Demo Python Launcher

A Python wrapper for the LWJGL demo that provides easy configuration
and dynamic testing without rebuilding with Maven.
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
    
    def launch(self, java_args=None, app_args=None, dry_run=False):
        if java_args is None: java_args = []
        if app_args is None: app_args = []
        
        if not dry_run and not self.check_build():
            return False
        
        classpath = self.build_classpath()
        cmd = ["java", "-cp", classpath] + java_args + ["com.necat.lwjgl.HelloLWJGL"] + app_args
        
        if dry_run:
            print("🔍 DRY RUN MODE - Command that would be executed:")
            print("=" * 70)
            print(" ".join(cmd))
            print("=" * 70)
            print("\nClasspath entries:")
            for i, entry in enumerate(classpath.split(os.pathsep), 1):
                exists = "✓" if Path(entry).exists() else "✗"
                print(f"  {i}. [{exists}] {entry}")
            print()
            return True
        
        print("🚀 Launching LWJGL Demo...")
        print(f"   Args: {' '.join(app_args) if app_args else '(none)'}\n")
        
        try:
            process = subprocess.Popen(cmd, cwd=self.project_dir, stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT, text=True, bufsize=1)
            for line in process.stdout:
                print(line, end='')
            process.wait()
            return process.returncode == 0
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            process.terminate()
            return False
        except Exception as e:
            print(f"\n❌ Error launching: {e}")
            return False
    
    def list_presets(self):
        print("Available presets:\n" + "=" * 60)
        for name, config in self.presets.items():
            print(f"\n{name}:")
            for k, v in config.items():
                print(f"  --{k} {v}")
        print()
    
    def get_preset_args(self, preset_name):
        if preset_name not in self.presets:
            print(f"❌ Unknown preset: {preset_name}")
            print(f"Available: {', '.join(self.presets.keys())}")
            return None
        args = []
        for k, v in self.presets[preset_name].items():
            args.append(f"--{k}")
            if v is not True:
                args.append(str(v))
        return args

def main():
    parser = argparse.ArgumentParser(
        description="LWJGL Demo Python Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n  %(prog)s\n  %(prog)s --preset performance\n  %(prog)s --width 1024 --height 768\n  %(prog)s --dry-run --preset minimal"
    )
    
    parser.add_argument("--preset", "-p", help="Use a preset configuration")
    parser.add_argument("--list-presets", action="store_true", help="List available presets and exit")
    parser.add_argument("--build-only", action="store_true", help="Only build the project, don't run")
    parser.add_argument("--dry-run", action="store_true", help="Print command without executing")
    parser.add_argument("--java-args", nargs=argparse.REMAINDER, help="Additional JVM arguments")
    parser.add_argument("app_args", nargs=argparse.REMAINDER, help="Arguments for LWJGL application")
    
    args, unknown = parser.parse_known_args()
    launcher = LWJGLLauncher()
    
    if args.list_presets:
        launcher.list_presets()
        return 0
    
    if args.build_only:
        return 0 if launcher.check_build() else 1
    
    app_args = []
    if args.preset:
        preset_args = launcher.get_preset_args(args.preset)
        if preset_args is None:
            return 1
        app_args.extend(preset_args)
    
    if unknown:
        app_args.extend([arg for arg in unknown if arg != "--"])
    
    if args.app_args:
        app_args.extend(args.app_args)
    
    java_args = args.java_args if args.java_args else []
    success = launcher.launch(java_args, app_args, dry_run=args.dry_run)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
