import streamlit as st
import json
import pandas as pd
import time
import matplotlib.pyplot as plt  # Add this import


def load_data():
    with open('aggregated_data.json', 'r') as f:
        data = json.load(f)
    return data

def main():
    st.title("IP Link Analyzer Dashboard")

    while True:
        data = load_data()

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
        traffic_between_countries = {f"{key[0]} & {key[1]}": value for key, value in data['traffic_between_countries'].items()}
        df_traffic_between_countries = pd.DataFrame(list(traffic_between_countries.items()), columns=['Traffic Between Countries', 'Count'])
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
        st.experimental_rerun()

if __name__ == "__main__":
    main()
