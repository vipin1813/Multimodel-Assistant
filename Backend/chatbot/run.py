import subprocess
import os
import sys

def main():
    # Get the directory of the run.py script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the backend main.py
    backend_main = os.path.join(script_dir, "main.py")
    
    # Path to the frontend app.py
    frontend_app = os.path.join(script_dir, "frontend", "app.py")

    # Command to run the backend
    backend_command = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    
    # Command to run the frontend
    frontend_command = [sys.executable, "-m", "streamlit", "run", frontend_app]

    # Run the backend and frontend in parallel
    backend_process = subprocess.Popen(backend_command, cwd=script_dir)
    frontend_process = subprocess.Popen(frontend_command, cwd=script_dir)

    # Wait for both processes to complete
    backend_process.wait()
    frontend_process.wait()

if __name__ == "__main__":
    main()
