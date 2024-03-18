from scapy.all import IP, TCP, UDP, ICMP

def parse_packet(packet):
    parsed_data = {
        'source_ip': None,
        'destination_ip': None,
        'protocol': None,
        'source_port': None,
        'destination_port': None,
        'packet_size': len(packet),
        'payload_size': None,
        'payload': None
    }

    # Extract IP layer information
    if IP in packet:
        ip_layer = packet[IP]
        parsed_data['source_ip'] = ip_layer.src
        parsed_data['destination_ip'] = ip_layer.dst
        parsed_data['protocol'] = ip_layer.proto

    # Extract TCP layer information
    if TCP in packet:
        tcp_layer = packet[TCP]
        parsed_data['source_port'] = tcp_layer.sport
        parsed_data['destination_port'] = tcp_layer.dport
        parsed_data['payload_size'] = len(tcp_layer.payload)
        parsed_data['payload'] = bytes(tcp_layer.payload).decode('utf-8', 'ignore')

    # Extract UDP layer information
    elif UDP in packet:
        udp_layer = packet[UDP]
        parsed_data['source_port'] = udp_layer.sport
        parsed_data['destination_port'] = udp_layer.dport
        parsed_data['payload_size'] = len(udp_layer.payload)
        parsed_data['payload'] = bytes(udp_layer.payload).decode('utf-8', 'ignore')

    # Extract ICMP layer information (for example, ping packets)
    elif ICMP in packet:
        icmp_layer = packet[ICMP]
        parsed_data['payload_size'] = len(icmp_layer.payload)
        parsed_data['payload'] = bytes(icmp_layer.payload).decode('utf-8', 'ignore')

    return parsed_data

