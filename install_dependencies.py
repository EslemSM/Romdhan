"""Install missing dependencies for the prayer endpoint"""
import subprocess
import sys

dependencies = ['adhan', 'pytz']

print("Installing dependencies for prayer endpoint...")
print("=" * 60)

for dep in dependencies:
    print(f"Installing {dep}...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
        print(f"OK: {dep} installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install {dep}")
        print(f"Try manually: pip install {dep}")

print("=" * 60)
print("Done! Please restart your Flask server.")

