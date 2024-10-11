import psutil

"""
    Checks disk usage for all mounted partitions. If any partition exceeds the threshold, prints an alert.        
    Returns a list of partitions exceeding the threshold.
"""
def check_disk_usage(threshold):
    
    alerts = []
    for partition in psutil.disk_partitions(all=False):  # Exclude pseudo filesystems
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            usage_percent = usage.percent
            if usage_percent > threshold:
                alerts.append((partition.device, partition.mountpoint, usage_percent))
        except PermissionError:
            # Skip partitions where permission is denied
            continue
    
    return alerts

# Usage
threshold = 80  # Set your threshold here
alerts = check_disk_usage(threshold)

if alerts:
    for device, mountpoint, usage in alerts:
        print(f"Alert! Disk usage on '{device}' ({mountpoint}) is at {usage}%.")
else:
    print("All partitions are within acceptable usage limits.")
