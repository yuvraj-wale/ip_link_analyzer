# settings.py

# Packet capture settings
CAPTURE_FILTER = "ip"
CAPTURE_COUNT = 0 # number of packets, set to 0 for infinite capture
CAPTURE_SAVE_TO_FILE = True
CAPTURE_FILE_PATH = "captures/capture.pcap"
CAPTURE_TIMEOUT = None  # No timeout by default for infinite capture
GEOLITE2_DB_PATH = '/Users/yuvraj/Downloads/GeoLite2-Country_20240312/GeoLite2-Country.mmdb' # download and set path/to/GeoLite2-Country database
TARGET_COUNTRIES = [('United States', 'Canada'), ('France', 'Germany')] # configurable target countries

