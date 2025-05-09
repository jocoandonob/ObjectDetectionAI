"""
Simplified runner script for Replit - executes start.py
"""
import os
import subprocess
import sys

def main():
    print("Starting Image Processing App...")
    
    # Run our start.py script
    try:
        subprocess.run([sys.executable, "start.py"], check=True)
    except KeyboardInterrupt:
        print("Server shutdown initiated")
    except Exception as e:
        print(f"Error starting server: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())