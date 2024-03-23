import os
import subprocess
import threading
from src import capture, visualizer

def start_capture():
    capture.start_capture()  # Continuous packet capture and analysis

def start_visualization():
    visualizer.run_visualization()
    # subprocess.Popen(['streamlit', 'run', os.path.join(os.path.dirname(__file__), 'dashboard.py')])

    # while True:
    #     visualizer.visualize_data()  # Update visualization with latest data
    #     time.sleep(60)  # Adjust the interval as needed

if __name__ == '__main__':
    # Start the packet capture in a separate thread
    capture_thread = threading.Thread(target=start_capture)
    capture_thread.start()

    # Start the visualization process in a separate thread
    visualization_thread = threading.Thread(target=start_visualization)
    visualization_thread.start()

    # Keep the main thread running to allow continuous capture and visualization
    capture_thread.join()
    visualization_thread.join()
