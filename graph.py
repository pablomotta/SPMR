import pandas as pd
import matplotlib.pyplot as plt
import re
import os

# Ensure the graphs directory exists
GRAPH_DIR = "./graphs"
os.makedirs(GRAPH_DIR, exist_ok=True)

# Function to parse the log file and extract CPU and GPU data
def parse_log_file(log_file_path):
    data = {'Timestamp': [], 'CPU_Usage': [], 'CPU_Temp': [], 'GPU_Temp': [], 'GPU_Load': []}
    
    # Regex to capture log data
    timestamp_pattern = r"Timestamp: (.*)"
    cpu_usage_pattern = r"CPU Usage: (\d+)%"
    cpu_temp_pattern = r"CPU Temperature: (\d+\.?\d*)°C"
    gpu_temp_pattern = r"Temperature: (\d+\.?\d*)°C"
    gpu_load_pattern = r"Load: (\d+\.?\d*)%"

    with open(log_file_path, 'r') as file:
        gpu_section = False
        for line in file:
            # Extract timestamp
            if re.search(timestamp_pattern, line):
                data['Timestamp'].append(re.search(timestamp_pattern, line).group(1))

            # Extract CPU Usage
            if re.search(cpu_usage_pattern, line):
                data['CPU_Usage'].append(float(re.search(cpu_usage_pattern, line).group(1)))

            # Extract CPU Temperature
            if re.search(cpu_temp_pattern, line):
                data['CPU_Temp'].append(float(re.search(cpu_temp_pattern, line).group(1)))

            # Identify GPU section and extract GPU details
            if 'GPU' in line:
                gpu_section = True

            if gpu_section and re.search(gpu_temp_pattern, line):
                data['GPU_Temp'].append(float(re.search(gpu_temp_pattern, line).group(1)))
                gpu_section = False

            if gpu_section and re.search(gpu_load_pattern, line):
                data['GPU_Load'].append(float(re.search(gpu_load_pattern, line).group(1)))
                gpu_section = False
    
    # Fill missing GPU data with NaN (in case no GPU info was logged)
    max_length = max(len(data['CPU_Temp']), len(data['GPU_Temp']))
    for key in data:
        data[key] = data[key] + [None] * (max_length - len(data[key]))

    return pd.DataFrame(data)

# Function to plot the data and save to a file
def plot_data(df, log_file_name):
    plt.figure(figsize=(10, 6))
    
    # Plot CPU Usage and Temp
    plt.subplot(2, 1, 1)
    plt.plot(df['Timestamp'], df['CPU_Usage'], label="CPU Usage (%)", color='blue')
    plt.plot(df['Timestamp'], df['CPU_Temp'], label="CPU Temperature (°C)", color='red')
    plt.xticks(rotation=45)
    plt.title(f'CPU Usage and Temperature - {log_file_name}')
    plt.ylabel('Percentage / Temperature (°C)')
    plt.legend()
    
    # Plot GPU Usage and Temp
    plt.subplot(2, 1, 2)
    plt.plot(df['Timestamp'], df['GPU_Temp'], label="GPU Temperature (°C)", color='green')
    plt.plot(df['Timestamp'], df['GPU_Load'], label="GPU Load (%)", color='orange')
    plt.xticks(rotation=45)
    plt.title(f'GPU Usage and Temperature - {log_file_name}')
    plt.ylabel('Percentage / Temperature (°C)')
    plt.legend()

    plt.tight_layout()

    # Save the figure to the graphs directory
    output_path = os.path.join(GRAPH_DIR, f"{log_file_name.replace('.log', '')}.png")
    plt.savefig(output_path)
    plt.close()  # Close the figure to free memory

    print(f"Saved graph for {log_file_name} to {output_path}")

if __name__ == "__main__":
    # Specify the logs directory
    logs_dir = "./logs"

    # Loop through all files in the logs directory
    for log_file_name in os.listdir(logs_dir):
        log_file_path = os.path.join(logs_dir, log_file_name)

        # Check if it's a file (and not a subdirectory or other type)
        if os.path.isfile(log_file_path) and log_file_name.endswith('.log'):
            print(f"Processing log file: {log_file_name}")

            # Parse the log file
            df = parse_log_file(log_file_path)

            # Plot the data and save the graph
            plot_data(df, log_file_name)
