from scapy.all import sniff, wrpcap, conf
import time
from src import parser, classifier, analyser, aggregator, settings

analyzer = analyser.LinkRateAnalyzer()
traffic_aggregator = aggregator.TrafficAggregator()  # Create an instance of TrafficAggregator

should_continue_capture = True

def packet_handler(packet):
    parsed_data = parser.parse_packet(packet)
    classifications = classifier.classify_packet(parsed_data)  # Get all classifications at once
    is_encrypted = classifications['encryption'] == 'Encrypted'
    packet_size = parsed_data.get('packet_size', 0)
    analyzer.update(packet_size, is_encrypted)
    traffic_aggregator.aggregate_packet(classifications, packet_size, is_encrypted)  # Aggregate packet data

    # print(f"Packet: {parsed_data}, Classifications: {classifications}")

def start_capture():

    global should_continue_capture
    should_continue_capture = True

    analyzer.start()
    print("Starting packet capture...")
    filter = settings.CAPTURE_FILTER
    count = settings.CAPTURE_COUNT
    timeout = settings.CAPTURE_TIMEOUT
    export_interval = 5  # Interval in seconds for exporting data
    iface = settings.CAPTURE_INTERFACE

    print(f"Capturing on interface: {iface}")  # Display the interface being used

    start_time = time.time()

    def custom_action(packet):
        if not should_continue_capture:
            raise Exception("Capture stopped.")  # Raise an exception to stop sniffing
        packet_handler(packet)
        if time.time() - start_time >= export_interval:
            metrics = analyzer.get_metrics()
            aggregated_data = traffic_aggregator.get_aggregated_data()
            # print(f"Traffic metrics: {metrics}")
            # print(f"Aggregated data: {aggregated_data}")
            traffic_aggregator.export_to_json('aggregated_data.json')
            analyzer.start()  # Reset the analyzer for the next interval

    sniff_kwargs = {
        'prn': custom_action,
        'count': count,
        'timeout': timeout
    }
    if iface:
        sniff_kwargs['iface'] = iface
        print(f"Capturing on interface: {iface}")  # Display the interface being used
    if filter:
        sniff_kwargs['filter'] = filter

    try:
        # print("sniffinggg")
        sniff(**sniff_kwargs)
    except Exception as e:
        if str(e) != "Capture stopped.":
            raise  # Reraise the exception if it's not the expected one

    # Export any remaining data at the end of the capture
    metrics = analyzer.get_metrics()
    aggregated_data = traffic_aggregator.get_aggregated_data()
    # print(f"Final traffic metrics: {metrics}")
    # print(f"Final aggregated data: {aggregated_data}")
    traffic_aggregator.export_to_json('aggregated_data.json')

    analyzer.stop()

def stop_capture():
    """
    Stops the packet capture process.
    """

    global should_continue_capture
    should_continue_capture = False

if __name__ == "__main__":
    start_capture()