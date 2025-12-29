"""Test if prayer blueprint works with venv Python"""
import sys
import os

# Use venv Python
venv_python = os.path.join("venv", "Scripts", "python.exe")
if os.path.exists(venv_python):
    print(f"Testing with venv Python: {venv_python}")
    print("=" * 60)
    
    # This would need to be run separately, but let's check if we can import
    try:
        # Add venv site-packages to path
        venv_site_packages = os.path.join("venv", "Lib", "site-packages")
        if os.path.exists(venv_site_packages):
            sys.path.insert(0, venv_site_packages)
        
        from resources.prayer import prayer_bp
        print("OK: Prayer blueprint can be imported!")
        print(f"Blueprint name: {prayer_bp.name}")
    except Exception as e:
        print(f"ERROR: {e}")
else:
    print("venv not found in expected location")

