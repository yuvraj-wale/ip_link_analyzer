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
   git clone https://github.com/yuvraj-wale/ip_link_analyzer.git
   cd ip_link_analyzer
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
    sudo python main.py
   ```

2. The Streamlit dashboard will open in your default web browser, displaying real-time analysis results.

## Testing with iperf3

1. Install `iperf3` on your machine:
   - On macOS: `brew install iperf3`
   - On Linux: `sudo apt-get install iperf3`
   - On Windows: Download from [iperf.fr](https://iperf.fr/iperf-download.php)

2. Start the `iperf3` server in a separate terminal:
   ```bash
   iperf3 -s
   ```

3. Run the `iperf3` client to generate traffic (adjust the parameters as needed):
   ```bash
   iperf3 -c 127.0.0.1 -t 240 -b 10G
   ```
   This command generates 10 Gbps of traffic for 240 seconds to the localhost, where the IP Link Analyzer is running.

4. Observe the traffic analysis results in the Streamlit dashboard.

## Dependencies
- Python 3
- Scapy
- Streamlit
- Pandas
- Matplotlib
- GeoIP2

## License
This project is licensed under the [MIT License](LICENSE).
