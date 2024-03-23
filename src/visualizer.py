import os
import subprocess

def run_visualization():
    dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard.py')
    subprocess.Popen(['streamlit', 'run', dashboard_path])
