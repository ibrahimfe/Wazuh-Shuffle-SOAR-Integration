#!/usr/bin/env python3

import csv
import json
import subprocess
import sys
import time

from pathlib import Path
from datetime import datetime, timezone


# Konfigurasi eksperimen
EXPERIMENT_ID = sys.argv[1] if len(sys.argv) > 1 else "06"

DURATION = 150
INTERVAL = 2
BASELINE_DURATION = 30

OUTPUT_DIR = Path.home() / "skripsi_resource"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HOST_CSV = OUTPUT_DIR / f"experiment_{EXPERIMENT_ID}_host.csv"
DOCKER_CSV = OUTPUT_DIR / f"experiment_{EXPERIMENT_ID}_docker.csv"


def timestamp_utc():
    return datetime.now(timezone.utc).isoformat(
        timespec="milliseconds"
    ).replace("+00:00", "Z")


def read_cpu():
    with open("/proc/stat") as f:
        values = list(map(int, f.readline().split()[1:9]))

    idle = values[3] + values[4]
    total = sum(values)

    return idle, total


def calculate_cpu(previous, current):
    idle_delta = current[0] - previous[0]
    total_delta = current[1] - previous[1]

    if total_delta <= 0:
        return 0.0

    return 100 * (1 - idle_delta / total_delta)


def read_memory():
    info = {}

    with open("/proc/meminfo") as f:
        for line in f:
            key, value = line.split(":", 1)
            info[key] = int(value.strip().split()[0])

    total_kb = info["MemTotal"]
    available_kb = info["MemAvailable"]

    used_kb = total_kb - available_kb
    used_percent = used_kb / total_kb * 100

    return round(used_kb / 1024, 2), round(used_percent, 3)


def docker_stats():
    command = [
        "docker",
        "stats",
        "--no-stream",
        "--format",
        "{{json .}}"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=15,
        check=True
    )

    containers = []

    for line in result.stdout.splitlines():
        if line.strip():
            containers.append(json.loads(line))

    return containers


print("\n=== MONITORING CPU DAN RAM ===")
print(f"Experiment ID : {EXPERIMENT_ID}")
print(f"Duration      : {DURATION} seconds")
print(f"Interval      : {INTERVAL} seconds")
print(f"Baseline      : {BASELINE_DURATION} seconds")
print(f"Host CSV      : {HOST_CSV}")
print(f"Docker CSV    : {DOCKER_CSV}")
print()

with HOST_CSV.open("w", newline="") as host_file, \
     DOCKER_CSV.open("w", newline="") as docker_file:

    host_writer = csv.writer(host_file)
    docker_writer = csv.writer(docker_file)

    host_writer.writerow([
        "timestamp_utc",
        "elapsed_seconds",
        "phase",
        "host_cpu_percent",
        "host_ram_used_mib",
        "host_ram_percent"
    ])

    docker_writer.writerow([
        "timestamp_utc",
        "elapsed_seconds",
        "phase",
        "container_name",
        "container_cpu_percent",
        "container_mem_usage",
        "container_mem_percent"
    ])

    start = time.monotonic()
    previous_cpu = read_cpu()
    baseline_announced = False

    try:
        while True:
            elapsed = time.monotonic() - start

            if elapsed >= DURATION:
                break

            if elapsed < BASELINE_DURATION:
                phase = "baseline"
            else:
                phase = "observation"

                if not baseline_announced:
                    print("\n*** BASELINE SELESAI ***")
                    print("*** JALANKAN PENGUJIAN EICAR SEKARANG ***\n")
                    baseline_announced = True

            sample_time = timestamp_utc()

            current_cpu = read_cpu()
            cpu_percent = calculate_cpu(
                previous_cpu,
                current_cpu
            )
            previous_cpu = current_cpu

            ram_mib, ram_percent = read_memory()

            host_writer.writerow([
                sample_time,
                round(elapsed, 3),
                phase,
                round(cpu_percent, 3),
                ram_mib,
                ram_percent
            ])

            try:
                containers = docker_stats()

                for container in containers:
                    docker_writer.writerow([
                        sample_time,
                        round(elapsed, 3),
                        phase,
                        container["Name"],
                        container["CPUPerc"].replace("%", ""),
                        container["MemUsage"],
                        container["MemPerc"].replace("%", "")
                    ])

            except Exception as e:
                print(f"Docker stats error: {e}")

            host_file.flush()
            docker_file.flush()

            print(
                f"[{sample_time}] "
                f"{phase} | "
                f"CPU: {cpu_percent:.2f}% | "
                f"RAM: {ram_percent:.2f}%"
            )

            # Interval minimum antarsampel.
            # Perintah Docker dapat menambah waktu aktual.
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nMonitoring dihentikan oleh pengguna.")

print("\n=== MONITORING SELESAI ===")
print(f"Host data   : {HOST_CSV}")
print(f"Docker data : {DOCKER_CSV}")
