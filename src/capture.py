from scapy.all import sniff, wrpcap
import time
import os
import parser, classifier, analyser, aggregator
import sys
import os

root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_directory)

import settings


analyzer = analyser.LinkRateAnalyzer()
traffic_aggregator = aggregator.TrafficAggregator()  # Create an instance of TrafficAggregator

def packet_handler(packet):
    parsed_data = parser.parse_packet(packet)
    classifications = classifier.classify_packet(parsed_data)  # Get all classifications at once
    is_encrypted = classifications['encryption'] == 'Encrypted'
    packet_size = parsed_data.get('packet_size', 0)
    analyzer.update(packet_size, is_encrypted)
    traffic_aggregator.aggregate_packet(classifications, packet_size, is_encrypted)  # Aggregate packet data

    print(f"Packet: {parsed_data}, Classifications: {classifications}")
def start_capture():
    analyzer.start()
    print("Starting packet capture...")
    filter = settings.CAPTURE_FILTER
    count = settings.CAPTURE_COUNT
    save_to_file = settings.CAPTURE_SAVE_TO_FILE
    file_path = settings.CAPTURE_FILE_PATH
    timeout = settings.CAPTURE_TIMEOUT
    export_interval = 5  # Interval in seconds for exporting data

    start_time = time.time()

    def custom_action(packet):
        packet_handler(packet)
        if save_to_file and file_path:
            wrpcap(file_path, packet, append=True)
        if time.time() - start_time >= export_interval:
            metrics = analyzer.get_metrics()
            aggregated_data = traffic_aggregator.get_aggregated_data()
            print(f"Traffic metrics: {metrics}")
            print(f"Aggregated data: {aggregated_data}")
            traffic_aggregator.export_to_json('aggregated_data.json')
            analyzer.start()  # Reset the analyzer for the next interval

    sniff(prn=custom_action, filter=filter, count=count, timeout=timeout)

    # Export any remaining data at the end of the capture
    metrics = analyzer.get_metrics()
    aggregated_data = traffic_aggregator.get_aggregated_data()
    print(f"Final traffic metrics: {metrics}")
    print(f"Final aggregated data: {aggregated_data}")
    traffic_aggregator.export_to_json('aggregated_data.json')

    analyzer.stop()

if __name__ == "__main__":
    start_capture()