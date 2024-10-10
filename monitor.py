import psutil
import GPUtil
import datetime
import time
import os

# Directory to store log files
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Function to get the CPU temperature (handle gracefully if not available)
def get_cpu_temperature():
    try:
        if hasattr(psutil, 'sensors_temperatures'):
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                return temps['coretemp'][0].current
        return None
    except Exception as e:
        print(f"Error getting CPU temperature: {e}")
        return None

# Function to get GPU information (using GPUtil)
def get_gpu_info():
    try:
        gpus = GPUtil.getGPUs()
        gpu_info = []
        for gpu in gpus:
            gpu_info.append({
                'id': gpu.id,
                'name': gpu.name,
                'temperature': gpu.temperature,
                'load': gpu.load * 100  # Convert to percentage
            })
        return gpu_info
    except Exception as e:
        print(f"Error getting GPU info: {e}")
        return []

# Function to log CPU and GPU information
def log_cpu_gpu_info():
    while True:
        # Generate a new log file for each day
        log_file_name = os.path.join(LOG_DIR, f"{datetime.datetime.now().strftime('%Y-%m-%d')}.log")
        with open(log_file_name, 'a') as log_file:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # CPU info
            cpu_temp = get_cpu_temperature()
            cpu_usage = psutil.cpu_percent(interval=1)

            # GPU info
            gpu_info = get_gpu_info()

            # Prepare log entry
            log_entry = f"Timestamp: {timestamp}\n"
            log_entry += f"CPU Usage: {cpu_usage}%\n"
            log_entry += f"CPU Temperature: {cpu_temp if cpu_temp else 'N/A'}°C\n"

            # GPU details
            for gpu in gpu_info:
                log_entry += f"GPU {gpu['id']} - {gpu['name']}: \n"
                log_entry += f"\tTemperature: {gpu['temperature']}°C\n"
                log_entry += f"\tLoad: {gpu['load']}%\n"

            log_entry += "-" * 40 + "\n"

            # Write log entry to the file
            log_file.write(log_entry)

        # Wait for 20 seconds before the next log
        time.sleep(20)

if __name__ == "__main__":
    log_cpu_gpu_info()
