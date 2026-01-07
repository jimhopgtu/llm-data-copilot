import os
import subprocess
import sys

print("=== Checking for database ===")
db_path = "/app/data/sample.db"

if not os.path.exists(db_path):
    print("Database not found, initializing...")
    os.chdir("/app/data")
    subprocess.run([sys.executable, "init_db.py"], check=True)
    print("Database initialized!")
else:
    print(f"Database already exists at {db_path}")

print("=== Starting server ===")
os.chdir("/app")
os.execvp("uvicorn", ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"])
