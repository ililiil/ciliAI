import subprocess
import sys

result = subprocess.run(
    [sys.executable, 'app.py'],
    capture_output=True,
    text=True,
    cwd=r'd:\fangtang\ciliAI'
)

with open(r'd:\fangtang\flask_output.txt', 'w', encoding='utf-8') as f:
    f.write("STDOUT:\n")
    f.write(result.stdout)
    f.write("\nSTDERR:\n")
    f.write(result.stderr)
    f.write(f"\nReturn code: {result.returncode}")
