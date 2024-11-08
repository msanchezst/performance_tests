import subprocess
import time
import logging
from datetime import datetime
import signal
import sys
import socket
import statistics
import platform
import contextlib
import os

# Generate a timestamp for the log file name
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f'system_and_network_performance_log_{timestamp}.txt'

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

@contextlib.contextmanager
def logging_context():
    try:
        yield
    except Exception as e:
        logging.exception("An error occurred: %s", str(e))
    finally:
        logging.info("Logging complete. Closing log handlers.")
        for handler in logging.root.handlers:
            handler.close()

def get_cpu_usage():
    cmd = "top -l 1 | grep -E '^CPU'"
    output = subprocess.check_output(cmd, shell=True).decode().strip()
    return output.split(': ')[1]

def get_memory_usage():
    cmd = "vm_stat | grep 'Pages active'"
    output = subprocess.check_output(cmd, shell=True).decode().strip()
    active_memory = int(output.split()[2].strip('.')) * 4096 / 1024 / 1024  # Convert to MB
    
    cmd = "sysctl hw.memsize"
    output = subprocess.check_output(cmd, shell=True).decode().strip()
    total_memory = int(output.split()[1]) / 1024 / 1024  # Convert to MB
    
    return f"{active_memory:.2f}MB / {total_memory:.2f}MB"

def get_network_io():
    cmd = "netstat -ib | grep -e 'en0' -m 1"
    output = subprocess.check_output(cmd, shell=True).decode().strip()
    stats = output.split()
    return f"In: {stats[6]} bytes, Out: {stats[9]} bytes"

def log_system_stats():
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    network_io = get_network_io()
    
    log_message = (
        f"System Stats: "
        f"  CPU Usage: {cpu_usage} |"
        f"  RAM Usage: {memory_usage} |"
        f"  Network I/O: {network_io}"
    )
    logging.info(log_message)

def measure_download_speed():
    command = 'curl -s -S -n http://ipv4.download.thinkbroadband.com/100MB.zip -o /dev/null -w "%{time_total},%{size_download},%{speed_download}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    return result.stdout.strip()

def bytes_to_megabits(bytes_value):
    return (float(bytes_value) * 8) / 1_000_000


def log_system_profile():    
    command = 'system_profiler SPSoftwareDataType SPHardwareDataType'
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    # removing serial numbers and hardware UUIDs
    keywords = ["Serial Number", "UUID", "UDID"]
    filtered_lines = [
        line for line in result.stdout.splitlines()
        if not any(keyword in line for keyword in keywords)
    ]
    result_string = "\n".join(filtered_lines)
    logging.info(result_string)

def log_speed_test():
    try:
        speed_data = measure_download_speed()
        time_total, size_download, avg_speed_download = speed_data.split(',')
        
        time_total = float(time_total)
        size_download = float(size_download)
        avg_speed_download = float(avg_speed_download)
        
        avg_speed_mbps = bytes_to_megabits(avg_speed_download)
        
        log_message = (f"{platform.node()} speed Test Results: "
                       f"  Download Time: {time_total:.2f} seconds |"
                       f"  File Size: {size_download / 1_000_000:.2f} MB |"
                       f"  Average Download Speed: {avg_speed_mbps:.2f} Mbps")
        logging.info(log_message)
    except Exception as e:
        logging.error(f"Error during speed test: {e}")

def measure_latency(host, port=53, runs=3):
    latencies = []
    
    for _ in range(runs):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            start_time = time.time()
            sock.connect((host, port))
            end_time = time.time()
            latency = (end_time - start_time) * 1000
            latencies.append(latency)
            sock.close()
        except socket.error as e:
            logging.error(f"Error connecting to {host}:{port} - {e}")
    
    return latencies

def log_latency_stats(host, results):
    if results:
        avg_latency = statistics.mean(results)
        min_latency = min(results)
        max_latency = max(results)
        
        log_message = (f"Latency to {host}: "
                       f"  Average: {avg_latency:.2f} ms|"
                       f"  Minimum: {min_latency:.2f} ms|"
                       f"  Maximum: {max_latency:.2f} ms")
        logging.info(log_message)
    else:
        logging.warning(f"No successful latency measurements were made for {host}.")

def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    try:
        output = subprocess.check_output(command).decode().strip()
        lines = output.split('\n')
        return lines[-1].split('=')[-1].strip()
    except Exception as e:
        logging.error(f"Error pinging {host}: {e}")
        return "Error"

def signal_handler(sig, frame):
    logging.info("Program interrupted. Cleaning up and exiting...")
    logging.info(f"Logging complete. File output: {log_filename}")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    aws_dns_server = "169.254.169.253"
    google_dns = "8.8.8.8"

    log_system_profile()
    print("=== Starting initial speed test. Downloading 100MB file. Please wait... ===")
    log_speed_test()
    print("=== Speed test completed. Starting continuous monitoring. Press Ctrl+C to stop. ===")
    
    with logging_context():
        while True:
            # Log system stats
            log_system_stats()
            
            # Measure latency to AWS DNS
            aws_results = measure_latency(aws_dns_server)
            log_latency_stats(aws_dns_server, aws_results)
            
            # Measure latency to Google DNS
            google_results = measure_latency(google_dns)
            log_latency_stats(google_dns, google_results)
            
            # Ping google.com
            ping_result = ping("google.com")
            logging.info(f"Ping to google.com: {ping_result}")
            
            # Small wait before next iteration
            time.sleep(0.5)

if __name__ == "__main__":
    main()
