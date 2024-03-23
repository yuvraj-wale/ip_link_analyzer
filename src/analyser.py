import time

class LinkRateAnalyzer:
    def __init__(self):
        self.start_time = None
        self.total_bytes = 0
        self.total_packets = 0
        self.encrypted_packets = 0
        self.unencrypted_packets = 0

    def start(self):
        self.start_time = time.time()
        self.total_bytes = 0
        self.total_packets = 0
        self.encrypted_packets = 0
        self.unencrypted_packets = 0

    def update(self, packet_size, is_encrypted):
        self.total_bytes += packet_size
        self.total_packets += 1
        if is_encrypted:
            self.encrypted_packets += 1
        else:
            self.unencrypted_packets += 1

    def get_metrics(self):
        elapsed_time = time.time() - self.start_time
        bytes_per_second = self.total_bytes / elapsed_time
        packets_per_second = self.total_packets / elapsed_time
        encrypted_percentage = (self.encrypted_packets / self.total_packets) * 100 if self.total_packets > 0 else 0
        unencrypted_percentage = (self.unencrypted_packets / self.total_packets) * 100 if self.total_packets > 0 else 0
        return {
            'bytes_per_second': bytes_per_second,
            'packets_per_second': packets_per_second,
            'total_bytes': self.total_bytes,
            'total_packets': self.total_packets,
            'encrypted_percentage': encrypted_percentage,
            'unencrypted_percentage': unencrypted_percentage
        }

    def stop(self):
        self.start_time = None
        self.total_bytes = 0
        self.total_packets = 0
        self.encrypted_packets = 0
        self.unencrypted_packets = 0
