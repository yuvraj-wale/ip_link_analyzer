import psutil
import threading
import streamlit as st
import json
import pandas as pd
import os
import time
import matplotlib.pyplot as plt
from src import capture

capture_thread = None

def get_network_interfaces():
    return list(psutil.net_if_addrs().keys())

def clear_aggregated_data():
    with open('aggregated_data.json', 'w') as f:
        f.write("""
            {
                "protocol_counts": {},
                "application_protocol_counts": {},
                "encryption_counts": {},
                "country_traffic": {},
                "port_traffic": {},
                "traffic_between_countries": {},
                "bytes_per_second": 0,
                "bits_per_second": 0,
                "megabits_per_second": 0,
                "gigabits_per_second": 0,
                "packets_per_second": 0,
                "total_bytes": 0,
                "total_packets": 0,
                "encrypted_percentage": 0
            }
        """)

def stop_processes():
    capture.stop_capture()
    clear_aggregated_data()
    st.session_state['page'] = 'settings'
    st.success("Processes stopped.")
    st.rerun()

def capture_start():
    clear_aggregated_data()
    capture.start_capture()

def update_settings(new_settings):
    settings_path = os.path.join(os.path.dirname(__file__), 'settings.py')
    with open(settings_path, 'w') as f:
        f.write("# settings.py\n")
        for key, value in new_settings.items():
            if isinstance(value, str):
                f.write(f'{key} = "{value}"\n')
            else:
                f.write(f'{key} = {value}\n')

def load_data(retries=5, delay=1):
    for _ in range(retries):
        try:
            with open('aggregated_data.json', 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            time.sleep(delay)
    raise Exception("Failed to load JSON data after multiple retries.")

def display_metrics_analysis():

    st.title("IP Link Analyzer Dashboard")

    if st.button("Stop Processes"):
         stop_processes()

    while True:
        data = load_data()
        # print(data)

        st.header("Protocol Counts")
        df_protocol = pd.DataFrame(list(data['protocol_counts'].items()), columns=['Protocol', 'Count'])
        st.bar_chart(df_protocol.set_index('Protocol'))

        st.header("Application Protocol Counts")
        df_protocol = pd.DataFrame(list(data['application_protocol_counts'].items()), columns=['Application Protocol', 'Count'])
        st.bar_chart(df_protocol.set_index('Application Protocol'))

        st.header("Encryption Counts")
        df_encryption = pd.DataFrame(list(data['encryption_counts'].items()), columns=['Encryption Status', 'Count'])
        st.bar_chart(df_encryption.set_index('Encryption Status'))

        st.header("Country Traffic")
        df_country_traffic = pd.DataFrame(list(data['country_traffic'].items()), columns=['Country Traffic', 'Count'])
        st.bar_chart(df_country_traffic.set_index('Country Traffic'))

        st.header("Port Traffic")
        df_port_traffic = pd.DataFrame(list(data['port_traffic'].items()), columns=['Port Traffic', 'Count'])
        st.bar_chart(df_port_traffic.set_index('Port Traffic'))

        st.header("Traffic Between Countries")
        # Convert dictionary keys from tuples to strings for display
        # traffic_between_countries = {f"{key[0]} & {key[1]}": value for key, value in data['traffic_between_countries'].items()}
        df_traffic_between_countries = pd.DataFrame(list(data['traffic_between_countries'].items()), columns=['Traffic Between Countries', 'Count'])
        st.bar_chart(df_traffic_between_countries.set_index('Traffic Between Countries'))
        
        # Pie chart for encrypted percentage
        st.header("Encryption Percentage")
        encryption_data = {
            'Encrypted': data["encrypted_percentage"],
            'Unencrypted': 100 - data["encrypted_percentage"]
        }
        fig, ax = plt.subplots()
        ax.pie(encryption_data.values(), labels=encryption_data.keys(), autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#F44336'])
        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
        st.pyplot(fig)


        st.header("Link Rate Metrics")
        link_rate_metrics = {
            'Bytes per Second': data["bytes_per_second"],
            'Bits per Second': data["bits_per_second"],
            'Megabits per Second': data["megabits_per_second"],  # Add Mbps to the metrics
            'Gigabits per Second': data["gigabits_per_second"],
            'Packets per Second': data["packets_per_second"],
            'Total Bytes': data["total_bytes"],
            'Total Packets': data["total_packets"],
            'Encrypted Percentage': data["encrypted_percentage"]
        }
        df_link_rate_metrics = pd.DataFrame(list(link_rate_metrics.items()), columns=['Metric', 'Value'])
        st.table(df_link_rate_metrics.set_index('Metric'))

        time.sleep(5)  # Refresh data every 5 seconds
        st.rerun()

    # # Create placeholders for the metrics analysis
    # protocol_counts_placeholder = st.empty()
    # application_protocol_counts_placeholder = st.empty()
    # encryption_counts_placeholder = st.empty()
    # country_traffic_placeholder = st.empty()
    # port_traffic_placeholder = st.empty()
    # traffic_between_countries_placeholder = st.empty()
    # encryption_percentage_placeholder = st.empty()
    # link_rate_metrics_placeholder = st.empty()

    # while True:
    #     data = load_data()

    #     protocol_counts_placeholder.header("Protocol Counts")
    #     df_protocol = pd.DataFrame(list(data['protocol_counts'].items()), columns=['Protocol', 'Count'])
    #     protocol_counts_placeholder.bar_chart(df_protocol.set_index('Protocol'))

    #     application_protocol_counts_placeholder.header("Application Protocol Counts")
    #     df_protocol = pd.DataFrame(list(data['application_protocol_counts'].items()), columns=['Application Protocol', 'Count'])
    #     application_protocol_counts_placeholder.bar_chart(df_protocol.set_index('Application Protocol'))

    #     encryption_counts_placeholder.header("Encryption Counts")
    #     df_encryption = pd.DataFrame(list(data['encryption_counts'].items()), columns=['Encryption Status', 'Count'])
    #     encryption_counts_placeholder.bar_chart(df_encryption.set_index('Encryption Status'))

    #     country_traffic_placeholder.header("Country Traffic")
    #     df_country_traffic = pd.DataFrame(list(data['country_traffic'].items()), columns=['Country Traffic', 'Count'])
    #     country_traffic_placeholder.bar_chart(df_country_traffic.set_index('Country Traffic'))

    #     port_traffic_placeholder.header("Port Traffic")
    #     df_port_traffic = pd.DataFrame(list(data['port_traffic'].items()), columns=['Port Traffic', 'Count'])
    #     port_traffic_placeholder.bar_chart(df_port_traffic.set_index('Port Traffic'))

    #     traffic_between_countries_placeholder.header("Traffic Between Countries")
    #     # Convert dictionary keys from tuples to strings for display
    #     # traffic_between_countries = {f"{key[0]} & {key[1]}": value for key, value in data['traffic_between_countries'].items()}
    #     df_traffic_between_countries = pd.DataFrame(list(data['country_traffic'].items()), columns=['Traffic Between Countries', 'Count'])
    #     traffic_between_countries_placeholder.bar_chart(df_traffic_between_countries.set_index('Traffic Between Countries'))
            
    #     # Pie chart for encrypted percentage
    #     encryption_percentage_placeholder.header("Encryption Percentage")
    #     encryption_data = {
    #             'Encrypted': data["encrypted_percentage"],
    #             'Unencrypted': 100 - data["encrypted_percentage"]
    #     }
    #     fig, ax = plt.subplots()
    #     ax.pie(encryption_data.values(), labels=encryption_data.keys(), autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#F44336'])
    #     ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    #     encryption_percentage_placeholder.pyplot(fig)


    #     link_rate_metrics_placeholder.header("Link Rate Metrics")
    #     link_rate_metrics = {
    #             'Bytes per Second': data["bytes_per_second"],
    #             'Bits per Second': data["bits_per_second"],
    #             'Megabits per Second': data["megabits_per_second"],  # Add Mbps to the metrics
    #             'Gigabits per Second': data["gigabits_per_second"],
    #             'Packets per Second': data["packets_per_second"],
    #             'Total Bytes': data["total_bytes"],
    #             'Total Packets': data["total_packets"],
    #             'Encrypted Percentage': data["encrypted_percentage"]
    #     }
    #     df_link_rate_metrics = pd.DataFrame(list(link_rate_metrics.items()), columns=['Metric', 'Value'])
    #     link_rate_metrics_placeholder.table(df_link_rate_metrics.set_index('Metric'))

    #     time.sleep(2)  # Refresh data every 5 seconds
    #     st.rerun()


def settings_page():
    st.title("IP Link Analyzer Dashboard")

    # Packet capture settings form
    with st.form("capture_settings"):
        st.header("Packet Capture Settings")
        capture_filter = st.text_input("Capture Filter", "ip")
        st.caption("Leave empty to apply no filter and capture all traffic.")
        # capture_interface = st.text_input("Capture Interface", "lo0")
        interfaces = get_network_interfaces()
        capture_interface = st.selectbox("Capture Interface", interfaces)
        capture_count = st.number_input("Capture Count (0 for infinite)", min_value=0, value=0, step=1)
        capture_timeout = st.number_input("Capture Timeout in seconds (0 for no timeout)", min_value=0, value=0, step=1)
        capture_timeout = None if capture_timeout == 0 else capture_timeout
        target_countries_input = st.text_area("Enter target countries pairs (comma-separated, e.g. 'United States, Canada')",
                                              "United States, Canada\nFrance, Germany")
        target_countries = [tuple(pair.split(", ")) for pair in target_countries_input.split("\n") if pair]
        submitted = st.form_submit_button("Save Configuration")

    if submitted:
        # Update the settings.py file
        st.session_state['capture_started'] = True
        print("flag capture started == true")
        
        new_settings = {
            "CAPTURE_FILTER": capture_filter,
            "CAPTURE_INTERFACE": capture_interface,
            "CAPTURE_COUNT": capture_count,
            "CAPTURE_TIMEOUT": capture_timeout,
            "TARGET_COUNTRIES": target_countries
        }
        update_settings(new_settings)
        print("settings updated")
        st.session_state['page'] = 'metrics'  # Navigate to metrics page
        print("flag for page set to metrics page")
        capture_thread = threading.Thread(target=capture_start)
        capture_thread.start()
        st.rerun() 

def main():
    # Initialize session state for page navigation
    # if 'capture_started' not in st.session_state:
    #     print("reachedddd 1")
    #     st.session_state['capture_started'] = False   

    if 'page' not in st.session_state:
        st.session_state['page'] = 'settings'

    # Page navigation
    if st.session_state['page'] == 'settings':
        settings_page()
    elif st.session_state['page'] == 'metrics':
        display_metrics_analysis()

    # if st.session_state['capture_started'] == True:
    #     print("reacheddddddd  2")
    #     capture_thread = threading.Thread(target=capture_start)
    #     capture_thread.start() 

if __name__ == "__main__":
    main()

# def main():
#     st.title("IP Link Analyzer Dashboard")

#     # Initialize session state
#     if 'submitted' not in st.session_state:
#         st.session_state['submitted'] = False

#     # Packet capture settings form
#     with st.form("capture_settings"):
#         st.header("Packet Capture Settings")
#         capture_filter = st.text_input("Capture Filter", "ip")
#         capture_interface = st.text_input("Capture Interface", "lo0")
#         capture_count = st.number_input("Capture Count (0 for infinite)", min_value=0, value=0, step=1)
#         capture_timeout = st.number_input("Capture Timeout in seconds (0 for no timeout)", min_value=0, value=0, step=1)
#         capture_timeout = None if capture_timeout == 0 else capture_timeout
#         target_countries_input = st.text_area("Enter target countries pairs (comma-separated, e.g. 'United States, Canada')",
#                                               "United States, Canada\nFrance, Germany")
#         target_countries = [tuple(pair.split(", ")) for pair in target_countries_input.split("\n") if pair]
#         submitted = st.form_submit_button("Save Configuration")

#     if submitted:
#         # Update the settings.py file
#         st.session_state['submitted'] = True
#         new_settings = {
#             "CAPTURE_FILTER": capture_filter,
#             "CAPTURE_INTERFACE": capture_interface,
#             "CAPTURE_COUNT": capture_count,
#             "CAPTURE_TIMEOUT": capture_timeout,
#             "TARGET_COUNTRIES": target_countries
#         }
#         update_settings(new_settings)
    
#     if st.session_state['submitted']:
#         # Display metrics analysis part
#         display_metrics_analysis()

# if __name__ == "__main__":
#     main()
