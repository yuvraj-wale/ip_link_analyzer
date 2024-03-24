import threading
import time
import dashboard
from src import visualizer
# from dashboard import dashboard
from src import capture

def start_capture():
    capture.start_capture()  # Continuous packet capture and analysis

# def check_capture_start():
#     while not dashboard.st.session_state.get('capture_started', False):
#         time.sleep(1)
#     capture_thread = threading.Thread(target=start_capture)
#     capture_thread.start()

def start_visualization():
    visualizer.run_visualization()
    # subprocess.Popen(['streamlit', 'run', os.path.join(os.path.dirname(__file__), 'dashboard.py')])

    # while True:
    #     visualizer.visualize_data()  # Update visualization with latest data
    #     time.sleep(60)  # Adjust the interval as needed

if __name__ == '__main__':
    # # Start a thread to check for capture start
    # check_thread = threading.Thread(target=check_capture_start)
    # check_thread.start()

    # # Start the visualization process
    # start_visualization()

    # # Wait for the check thread to finish
    # check_thread.join()

    # Start the packet capture in a separate thread
    # capture_thread = threading.Thread(target=start_capture)
    # capture_thread.start()

    # Start the visualization process in a separate thread
    visualization_thread = threading.Thread(target=start_visualization)
    visualization_thread.start()

    # Keep the main thread running to allow continuous capture and visualization
    # capture_thread.join()
    # if dashboard.capture_thread is not None:
    #     dashboard.capture_thread.join()
    visualization_thread.join()
