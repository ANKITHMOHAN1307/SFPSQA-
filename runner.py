# runner.py
import subprocess
import json
from Decoding import decode_from_upload, decode_from_scan

# PYTHON_32_PATH = r"A:\python.exe"  # Update to your 32-bit python path


import subprocess

def run_32bit_script(script_name):
    try:
        result = subprocess.run(
            [r"A:\Python311-32\python.exe", script_name],
            cwd=r"A:\Barcode Reader",
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        print("Standard Output:", e.stdout)
        print("Standard Error:", e.stderr)
        return {"Error": f"Failed to run {script_name}: {e.stderr}"}
