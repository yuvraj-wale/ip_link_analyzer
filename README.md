# IP Link Analyzer/Classifier

## Description
This project is a software-based tool designed to analyze and classify data transacted over IP links. It captures network traffic, computes link rate metrics, and classifies traffic based on protocols, encryption status, country-specific flow, and port numbers. The results are presented in a real-time dashboard.

## Features
- Real-time packet capture and analysis
- Classification of traffic by protocols, encryption, country, and port numbers
- Calculation of link rate metrics (bytes/sec, packets/sec, etc.)
- Real-time dashboard visualization using Streamlit

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ip-link-analyzer.git
   cd ip-link-analyzer
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. (macOS) Install additional dependencies for packet capture:
   ```bash
   brew install libpcap  # Required for Scapy
   ```

4. Download the GeoLite2 database:
   - Go to the [MaxMind GeoLite2 page](https://dev.maxmind.com/geoip/geoip2/geolite2/).
   - Sign up for a free account and download the GeoLite2 City database.
   - Extract the downloaded file and note the path to the `GeoLite2-Country.mmdb` file.

5. Configure the `settings.py` file:
   - go to `settings.py` file in the root directory of the project.
   - Add the following line to specify the path to the GeoLite2 database:
     ```python
     GEOLITE2_DB_PATH = '/path/to/GeoLite2-Country.mmdb'
     ```

## Usage

1. Start the IP Link Analyzer:
   ```bash
   python main.py
   ```

2. The Streamlit dashboard will open in your default web browser, displaying real-time analysis results.

## Dependencies
- Python 3
- Scapy
- Streamlit
- Pandas
- Matplotlib
- GeoIP2

## License
This project is licensed under the [MIT License](LICENSE).
