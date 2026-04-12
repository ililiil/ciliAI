import subprocess
import sys
import os

os.chdir(r'd:\fangtang\ciliAI')
os.environ['PYTHONUNBUFFERED'] = '1'

proc = subprocess.Popen(
    [r'.\venv\Scripts\python.exe', 'app.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    cwd=r'd:\fangtang\ciliAI'
)

lines = []
try:
    for line in proc.stdout:
        lines.append(line.rstrip())
        if len(lines) > 50:
            break
except:
    pass

proc.wait(timeout=5)

with open(r'd:\fangtang\ciliAI\flask_debug.txt', 'w', encoding='utf-8') as f:
    f.write(f"Return code: {proc.returncode}\n")
    f.write("\n".join(lines))
