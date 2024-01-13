import os
import subprocess

def run_pyinstaller():
    project_root = os.getcwd()
    command = f"pyinstaller -y --specpath {project_root}/build main.py"
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    run_pyinstaller()