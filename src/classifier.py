import re
import geoip2.database
import os
import sys

root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_directory)

import settings
def classify_application_protocol(parsed_data):
    protocol = parsed_data.get('protocol')
    src_port = parsed_data.get('source_port')
    dst_port = parsed_data.get('destination_port')
    payload = parsed_data.get('payload', b'')

    # Ensure the payload is bytes
    if isinstance(payload, str):
        payload = payload.encode('utf-8', errors='ignore')

    # Classify based on TCP ports
    if protocol == 6:  # TCP
        if src_port == 443 or dst_port == 443:
            if payload.startswith(b'\x17\x03\x03'):
                return 'HTTPS (TLS Application Data)'
            return 'HTTPS'
        elif src_port == 993 or dst_port == 993:
            return 'IMAPS'
        elif src_port == 22 or dst_port == 22:
            return 'SSH'
        elif src_port == 80 or dst_port == 80:
            return 'HTTP'
        elif src_port == 21 or dst_port == 21:
            return 'FTP'
        elif src_port == 25 or dst_port == 25:
            return 'SMTP'
        elif src_port == 110 or dst_port == 110:
            return 'POP3'
        elif src_port == 143 or dst_port == 143:
            return 'IMAP'
        elif src_port == 53 or dst_port == 53:
            return 'DNS'
        elif src_port == 5060 or dst_port == 5060:
            return 'SIP'
        # Add more port-based classifications as needed

    # Classify based on UDP ports
    elif protocol == 17:  # UDP
        if src_port == 5060 or dst_port == 5060:
            return 'SIP'
        elif src_port == 53 or dst_port == 53:
            return 'DNS'
        elif src_port >= 16384 and dst_port <= 32767:
            return 'RTP'
        elif (src_port == 67 and dst_port == 68) or (src_port == 68 and dst_port == 67):
            return 'DHCP'
        # Add more port-based classifications as needed

    # Classify based on payload patterns for TLS
    tls_patterns = [
        b'\x16\x03[\x00-\x03]',  # TLS Handshake
        b'\x17\x03[\x00-\x03]',  # TLS Application Data
        b'\x14\x03[\x00-\x03]',  # TLS Change Cipher Spec
    ]
    for pattern in tls_patterns:
        if re.search(pattern, payload):
            return 'TLS'

    return 'Unknown'


def classify_protocol(parsed_data):
    protocol_mapping = {
        6: 'TCP',
        17: 'UDP',
        1: 'ICMP',
        2: 'IGMP',
        89: 'OSPF',
        50: 'ESP',
        51: 'AH',
        47: 'GRE',
        # Add more protocol numbers and their corresponding names as needed
    }
    protocol_number = parsed_data.get('protocol')
    return protocol_mapping.get(protocol_number, 'Unknown')

def classify_encryption(parsed_data):
    protocol = parsed_data.get('protocol')
    src_port = parsed_data.get('source_port')
    dst_port = parsed_data.get('destination_port')
    payload = parsed_data.get('payload', b'')

    # Ensure the payload is bytes
    if isinstance(payload, str):
        payload = payload.encode('utf-8', errors='ignore')

    # Classify based on TCP ports
    if protocol == 6:  # TCP
        encrypted_ports = [443, 993, 995, 22, 6697]  # Add more encrypted ports as needed
        if src_port in encrypted_ports or dst_port in encrypted_ports:
            return 'Encrypted'

        # Additional payload analysis for TLS
        tls_patterns = [
            b'\x16\x03[\x00-\x03]',  # TLS Handshake
            b'\x17\x03[\x00-\x03]',  # TLS Application Data
            b'\x14\x03[\x00-\x03]',  # TLS Change Cipher Spec
        ]
        for pattern in tls_patterns:
            if payload.startswith(pattern):
                return 'Encrypted'

    # Add more classification logic as needed

    return 'Unencrypted'

# Initialize the GeoIP2 reader with the path to the database file
geoip_reader = geoip2.database.Reader(settings.GEOLITE2_DB_PATH)

def classify_country(parsed_data):
    source_ip = parsed_data.get('source_ip')
    destination_ip = parsed_data.get('destination_ip')
    try:
        # Look up the source IP address in the GeoIP2 database
        source_country = geoip_reader.country(source_ip).country.name
    except Exception:
        source_country = 'Unknown'

    try:
        # Look up the destination IP address in the GeoIP2 database
        destination_country = geoip_reader.country(destination_ip).country.name
    except Exception:
        destination_country = 'Unknown'

    return f"{source_country}-{destination_country}"

def classify_port(parsed_data):
    port_mapping = {
        20: 'FTP (Data)',
        21: 'FTP (Control)',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        465: 'SMTPS',
        853: 'DNS over TLS (DoT)',
        989: 'FTP over TLS/SSL (FTPS)',
        993: 'IMAPS',
        995: 'POP3S',
        1433: 'Microsoft SQL Server',
        3306: 'MySQL',
        3389: 'RDP',
        3391: 'RDP over SSL',
        5060: 'SIP',
        5432: 'PostgreSQL',
        8080: 'HTTP Alternate',
        27017: 'MongoDB',
        # Add more port numbers and their corresponding service names as needed
    }
    src_port = parsed_data.get('source_port')
    dst_port = parsed_data.get('destination_port')

    src_port_classification = port_mapping.get(src_port, f'Unknown')
    dst_port_classification = port_mapping.get(dst_port, f'Unknown')

    return f'{src_port_classification}-{dst_port_classification}'


def classify_traffic_between_countries(parsed_data, target_countries):
    source_ip = parsed_data.get('source_ip')
    destination_ip = parsed_data.get('destination_ip')

    try:
        # Look up the source and destination IP addresses in the GeoIP2 database
        source_country = geoip_reader.country(source_ip).country.name
        destination_country = geoip_reader.country(destination_ip).country.name
    except Exception:
        # If there's an error (e.g., IP address not found in the database), default to 'Unknown'
        source_country = 'Unknown'
        destination_country = 'Unknown'

    # Check if the traffic is between the target countries
    if source_country in target_countries and destination_country in target_countries:
        return f'Traffic between {source_country} & {destination_country}'
    else:
        return 'Traffic not between target countries'

def classify_packet(parsed_data):
    classifications = {
        'protocol': classify_protocol(parsed_data),
        'application_protocol': classify_application_protocol(parsed_data),
        'encryption': classify_encryption(parsed_data),
        'country': classify_country(parsed_data),
        'port': classify_port(parsed_data),
        'traffic_between_countries': classify_traffic_between_countries(parsed_data, ['Country1', 'Country2']),
    }
    return classifications
