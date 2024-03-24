import os
import subprocess

# def run_visualization():
#     dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard.py')
#     subprocess.Popen(['streamlit', 'run', dashboard_path])

def run_visualization():
    # Assuming this function is in a file inside the src directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dashboard_path = os.path.join(project_root, 'dashboard.py')
    subprocess.Popen(['streamlit', 'run', dashboard_path])