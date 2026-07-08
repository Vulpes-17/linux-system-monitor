import platform
import socket
from datetime import datetime

import psutil


def print_header():
    print("=" * 60)
    print("           Linux System Monitor v1.0")
    print("=" * 60)


def get_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    return str(uptime).split(".")[0]


def get_health_status(cpu, memory, disk):
    if cpu >= 90 or memory >= 90 or disk >= 90:
        return "CRITICAL"
    elif cpu >= 75 or memory >= 75 or disk >= 75:
        return "WARNING"
    return "HEALTHY"


def print_system_info():
    hostname = socket.gethostname()
    os_info = f"{platform.system()} {platform.release()}"

    print(f"Hostname:      {hostname}")
    print(f"OS:            {os_info}")
    print(f"Uptime:        {get_uptime()}")


def print_resource_usage():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    print("\nResource Usage")
    print("-" * 60)
    print(f"CPU Usage:     {cpu}%")
    print(f"Memory Usage:  {memory}%")
    print(f"Disk Usage:    {disk}%")

    return cpu, memory, disk


def print_top_processes(limit=5):
    print("\nTop Processes by Memory")
    print("-" * 60)
    print(f"{'PID':<8}{'Name':<25}{'Memory %':>10}")

    processes = []

    for process in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            processes.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes.sort(
        key=lambda p: p["memory_percent"] if p["memory_percent"] is not None else 0,
        reverse=True
    )

    for process in processes[:limit]:
        pid = process["pid"]
        name = process["name"][:24]
        memory = round(process["memory_percent"] or 0, 2)

        print(f"{pid:<8}{name:<25}{memory:>10}%")


def main():
    print_header()
    print_system_info()

    cpu, memory, disk = print_resource_usage()

    print_top_processes()

    health = get_health_status(cpu, memory, disk)

    print("\nSystem Health")
    print("-" * 60)
    print(f"Status:        {health}")
    print("=" * 60)


if __name__ == "__main__":
    main()
