#!/usr/bin/env python3
"""
LWJGL Demo Python Launcher

Quick launcher for testing different configurations without Maven rebuilds.
"""

import subprocess
import sys
from pathlib import Path

# Simple direct launcher for quick tests
if __name__ == "__main__":
    project_dir = Path(__file__).parent
    jar = project_dir / "target" / "lwjgl-demo-1.0-SNAPSHOT.jar"
    lib_dir = project_dir / "target" / "lib"
    
    # Build classpath
    import os
    cp = [str(jar)]
    if lib_dir.exists():
        cp.extend(str(p) for p in lib_dir.glob("*.jar"))
    
    classpath = os.pathsep.join(cp)
    
    # Launch with all args passed through
    cmd = ["java", "-cp", classpath, "com.necat.lwjgl.HelloLWJGL"] + sys.argv[1:]
    
    print(f"Launching: {' '.join(cmd[:4])} ...")
    subprocess.run(cmd, cwd=project_dir)
