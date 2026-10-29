import os
import time
import csv
from pathlib import Path
from datetime import datetime, timezone

# Identitas percobaan
experiment_id = input("ID percobaan (contoh: 01): ").strip()

if not experiment_id.isdigit():
    raise SystemExit("ID percobaan harus berupa angka, contoh: 01")

experiment_id = experiment_id.zfill(2)
filename = f"eicar-exp-{experiment_id}.txt"
filepath = Path("/tmp") / filename
csv_path = Path.home() / "malware_experiment_times.csv"

# Pastikan file percobaan sebelumnya tidak tertimpa
if filepath.exists():
    raise SystemExit(
        f"File {filepath} sudah ada. "
        "Pastikan status pengujian sebelumnya sebelum melanjutkan."
    )

def utc_iso(ns):
    seconds, nanos = divmod(ns, 1_000_000_000)
    dt = datetime.fromtimestamp(seconds, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + f".{nanos:09d}Z"

# EICAR standard antivirus test string
payload = (
    b"X5O!P%@AP[4\\PZX54(P^)7CC)7}"
    b"$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
)

print("\n=== PENGUJIAN DETEKSI DAN REMEDIASI ===")
print(f"Experiment ID : {experiment_id}")
print(f"File          : {filepath}")
print("Membuat file uji...")

# Membuat file secara eksklusif agar tidak menimpa file lain
fd = os.open(filepath, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)

try:
    os.write(fd, payload)
    os.fsync(fd)
finally:
    os.close(fd)

# Timestamp setelah penulisan file selesai
t0_ns = time.time_ns()

print(f"T0 UTC        : {utc_iso(t0_ns)}")
print(f"T0 Epoch ns   : {t0_ns}")
print("\nFile uji berhasil dibuat.")
print("Menunggu workflow menghapus file...")
print("Jangan membuat file uji lain selama percobaan ini.\n")

# Polling hanya mengamati keberadaan file; tidak menghapusnya.
timeout_seconds = 120
poll_interval = 0.02
deadline = time.monotonic() + timeout_seconds

while filepath.exists():
    if time.monotonic() >= deadline:
        print("TIMEOUT: File belum terhapus setelah 120 detik.")
        print("Jangan hapus file secara manual untuk percobaan ini.")
        print("Periksa workflow dan log sebelum melanjutkan.")
        break
    time.sleep(poll_interval)

if not filepath.exists():
    t2_observed_ns = time.time_ns()
    elapsed = (t2_observed_ns - t0_ns) / 1_000_000_000

    print("File sudah tidak ditemukan.")
    print(f"T2 Observed UTC: {utc_iso(t2_observed_ns)}")
    print(f"Waktu teramati : {elapsed:.3f} detik")
    outcome = "file_absent_observed"
else:
    t2_observed_ns = None
    elapsed = None
    outcome = "timeout"

# Simpan hasil lokal sebagai CSV
write_header = not csv_path.exists()

with csv_path.open("a", newline="") as f:
    writer = csv.writer(f)

    if write_header:
        writer.writerow([
            "experiment_id",
            "file_path",
            "t0_utc",
            "t0_epoch_ns",
            "t2_observed_utc",
            "t2_observed_epoch_ns",
            "elapsed_observed_seconds",
            "outcome"
        ])

    writer.writerow([
        experiment_id,
        str(filepath),
        utc_iso(t0_ns),
        t0_ns,
        utc_iso(t2_observed_ns) if t2_observed_ns else "",
        t2_observed_ns if t2_observed_ns else "",
        f"{elapsed:.6f}" if elapsed is not None else "",
        outcome
    ])

print(f"\nData lokal disimpan di: {csv_path}")
print("Gunakan timestamp event Wazuh untuk menentukan T1 dan T2 final.")