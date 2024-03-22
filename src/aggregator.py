from collections import defaultdict
import json
import time
from collections import defaultdict
import json
import time

class TrafficAggregator:
    def __init__(self):
        self.protocol_counts = defaultdict(int)
        self.application_protocol_counts = defaultdict(int)  # Add this line
        self.encryption_counts = defaultdict(int)
        self.country_traffic = defaultdict(int)
        self.port_traffic = defaultdict(int)
        self.traffic_between_countries = defaultdict(int)
        self.total_bytes = 0
        self.total_packets = 0
        self.encrypted_packets = 0
        self.start_time = time.time()

    def aggregate_packet(self, classifications, packet_size, is_encrypted):
        self.protocol_counts[classifications['protocol']] += 1
        self.application_protocol_counts[classifications['application_protocol']] += 1  # Add this line
        self.encryption_counts[classifications['encryption']] += 1
        self.country_traffic[classifications['country']] += 1
        self.port_traffic[classifications['port']] += 1
        self.traffic_between_countries[classifications['traffic_between_countries']] += 1
        self.total_bytes += packet_size
        self.total_packets += 1
        if is_encrypted:
            self.encrypted_packets += 1

    def get_aggregated_data(self):
        elapsed_time = time.time() - self.start_time
        bytes_per_second = self.total_bytes / elapsed_time if elapsed_time > 0 else 0
        bits_per_second = bytes_per_second * 8  # Calculate bits per second
        megabits_per_second = bits_per_second / 1_000_000  # Convert to Mbps
        gigabits_per_second = bits_per_second / 1_000_000_000  # Convert to Gbps
        packets_per_second = self.total_packets / elapsed_time if elapsed_time > 0 else 0
        encrypted_percentage = (self.encrypted_packets / self.total_packets) * 100 if self.total_packets > 0 else 0
        return {
            'protocol_counts': dict(self.protocol_counts),
            'application_protocol_counts': dict(self.application_protocol_counts),
            'encryption_counts': dict(self.encryption_counts),
            'country_traffic': dict(self.country_traffic),
            'port_traffic': dict(self.port_traffic),
            'traffic_between_countries': dict(self.traffic_between_countries),
            'bytes_per_second': bytes_per_second,
            'bits_per_second': bits_per_second,
            'megabits_per_second': megabits_per_second,  # Add Mbps to the metrics
            'gigabits_per_second': gigabits_per_second,  # Add Gbps to the metrics
            'packets_per_second': packets_per_second,
            'total_bytes': self.total_bytes,
            'total_packets': self.total_packets,
            'encrypted_percentage': encrypted_percentage
        }

    def reset(self):
        self.protocol_counts.clear()
        self.application_protocol_counts.clear()  # Add this line
        self.encryption_counts.clear()
        self.country_traffic.clear()
        self.port_traffic.clear()
        self.traffic_between_countries.clear()
        self.total_bytes = 0
        self.total_packets = 0
        self.encrypted_packets = 0
        self.start_time = time.time()

    def export_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.get_aggregated_data(), f, indent=4)
        self.total_bytes = 0
        self.total_packets = 0
        self.encrypted_packets = 0
        self.start_time = time.time()