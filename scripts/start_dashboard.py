#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Add 'src' and project root to sys.path for import resolution
project_root = Path(__file__).resolve().parent.parent
src_path = project_root / 'src'
sys.path[:0] = [str(src_path), str(project_root)]
# Ensure the src directory is in the path
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))
if __name__ == "__main__":
    os.chdir(project_root)

    try:
        from api.app import app, logger
    except ImportError as e:
        print(f"❌ Failed to import: {e}")
        sys.exit(1)

    logger.info("🌐 Starting EDR Web Dashboard...")
    print("🔗 Dashboard will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop")

    app.run(host="0.0.0.0", port=5000, debug=False)