import subprocess
import sys
import os

os.chdir(r'd:\fangtang\fangtang')
os.environ['PYTHONUNBUFFERED'] = '1'

proc = subprocess.Popen(
    [r'.\venv\Scripts\python.exe', 'app.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    cwd=r'd:\fangtang\fangtang'
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

with open(r'd:\fangtang\fangtang\flask_debug.txt', 'w', encoding='utf-8') as f:
    f.write(f"Return code: {proc.returncode}\n")
    f.write("\n".join(lines))
