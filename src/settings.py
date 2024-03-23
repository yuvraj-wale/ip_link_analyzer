# settings.py
import os

# Packet capture settings
CAPTURE_FILTER = "ip"
CAPTURE_INTERFACE = "lo0"
CAPTURE_COUNT = 0 # number of packets, set to 0 for infinite capture
CAPTURE_TIMEOUT = None  # No timeout by default for infinite capture
TARGET_COUNTRIES = [('United States', 'Canada'), ('France', 'Germany')] # configurable target countries
GEOLITE2_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'GeoLite2-Country.mmdb')

