#!/usr/bin/env python3
"""Membuat sampel EICAR untuk eksperimen remediasi manual.

Script ini HANYA membuat file dan mencatat T0; tidak melakukan polling,
menjalankan remediasi, atau menghapus file. T1/T2 diambil dari alert Wazuh.
Jalankan di Ubuntu Victim setelah cabang penghapusan otomatis Shuffle dimatikan.
"""

import csv
import os
import time
from datetime import datetime, timezone
from pathlib import Path

experiment_id = input("ID percobaan manual (contoh: 12): ").strip()
if not experiment_id.isdigit():
    raise SystemExit("ID harus berupa angka, contoh: 12")
experiment_id = experiment_id.zfill(2)
filepath = Path("/tmp") / f"eicar-exp-{experiment_id}.txt"
csv_path = Path.home() / "malware_manual_t0.csv"

if filepath.exists():
    raise SystemExit(f"File sudah ada: {filepath}. Periksa pengujian sebelumnya.")

# Sama persis dengan payload yang digunakan dalam pengujian otomatis.
payload = (
    b"X5O!P%@AP[4\\PZX54(P^)7CC)7}"
    b"$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
)

fd = os.open(filepath, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
try:
    os.write(fd, payload)
    os.fsync(fd)
finally:
    os.close(fd)

t0_ns = time.time_ns()
seconds, nanos = divmod(t0_ns, 1_000_000_000)
t0_utc = datetime.fromtimestamp(seconds, timezone.utc).strftime("%Y-%m-%dT%H:%M:%S") + f".{nanos:09d}Z"

# Simpan T0 secepat mungkin; proses manual tidak menunggu script selesai.
need_header = not csv_path.exists() or csv_path.stat().st_size == 0
with csv_path.open("a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    if need_header:
        writer.writerow(["experiment_id", "file_path", "t0_utc", "t0_epoch_ns", "method"])
    writer.writerow([experiment_id, str(filepath), t0_utc, t0_ns, "manual"])

print("\n=== PENGUJIAN REMEDIASI MANUAL ===")
print(f"ID               : {experiment_id}")
print(f"File             : {filepath}")
print(f"T0 UTC           : {t0_utc}")
print(f"T0 Epoch ns      : {t0_ns}")
print(f"Data T0 tersimpan: {csv_path}")
print("\nTunggu notifikasi YARA. Operator harus memverifikasi alert")
print("sebelum menghapus file secara manual via SSH IPv6.")
print("Script TIDAK menghapus file dan tidak memiliki batas waktu 120 detik.")
print("Gunakan timestamp alert YARA (T1) dan FIM deleted (T2) dari Wazuh.")
