# MacOS Performance Monitoring Scripts
# Overview
This folder contains a collection of Python scripts designed to monitor and capture system performance metrics on macOS systems. 


## mac_local_tests.py
`mac_local_tests.py` is a Python script designed to capture performance metrics on macOS systems. It monitors system metrics such as CPU usage, memory usage, and network performance, logging the results for analysis. The script has been tested in MacOSX Ventura (13.3)

#### Features

- **CPU Usage Monitoring**: Logs the current CPU usage percentage.
- **Memory Usage Monitoring**: Reports active and total memory usage in MB.
- **Network I/O Monitoring**: Tracks incoming and outgoing network bytes.
- **Download Speed Test**: Measures download speed using http://ipv4.download.thinkbroadband.com 100MB sample file.
- **Latency Measurement**: Measures latency to specified DNS servers (e.g., AWS and Google).
- **Ping Utility**: Pings a specified host (e.g., google.com) and logs the results.
- **Logging**: All metrics are logged to a timestamped file for easy reference.

#### Usage


```bash
python mac_local_tests.py
```

#### Logging
The script will generate a log file named `system_and_network_performance_log_<timestamp>.txt`, where `<timestamp>` represents the date and time of execution. This file will contain all logged metrics.

#### Stopping the Script
To stop the script at any time, press Ctrl+C. The script will finalize logging and exit gracefully. It is important to close the script using Ctrl+C to ensure proper logging.


#### Example Output
The log file will contain entries similar to:

```
2024-11-08 14:00:00 - INFO - System Stats: CPU Usage: 15.0% | RAM Usage: 2048.00MB / 8192.00MB | Network I/O: In: 102400 bytes, Out: 51200 bytes
2024-11-08 14:00:05 - INFO - Speed Test Results: Download Time: 2.50 seconds | File Size: 100.00 MB | Average Download Speed: 32.00 Mbps
2024-11-08 14:00:10 - INFO - Latency to AWS DNS: Average: 12.34 ms | Minimum: 10.00 ms | Maximum: 15.00 ms
```