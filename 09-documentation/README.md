# Backup Project Skripsi

## 1. Identitas Backup

Nama project:
Rancang Bangun Sistem Otomatisasi Deteksi dan Remediasi Malware
Terintegrasi Wazuh SIEM dan Shuffle SOAR pada Lingkungan Jaringan IPv6

Tanggal backup:
[Isi tanggal dan waktu]

Host:
[Isi hostname dan OS]

## 2. Arsitektur

Wazuh Manager:
[Container name, image, versi]

Wazuh Indexer:
[Container name, image, versi]

Wazuh Dashboard:
[Container name, image, versi]

Shuffle:
[Daftar service dan versi]

Ubuntu Victim:
[Hostname, Ubuntu version, Wazuh Agent version]

Wazuh Agent ID:
002

## 3. Jaringan

Bridge default:
virbr0

Subnet:
192.168.122.0/24

Bridge IPv6 lab:
virbr1

Subnet IPv6 lab:
fd00:1111:2222:3333::/64

Gateway:
fd00:1111:2222:3333::1

Ubuntu Victim:
fd00:1111:2222:3333::100

## 4. Deteksi

FIM:
Memantau /tmp

YARA:
[Isi versi dan lokasi rules]

Rule deteksi:
108001

Level:
12

## 5. Remediasi

Orkestrator:
Shuffle SOAR

Wazuh API:
[Isi alamat layanan, tanpa password/token]

Agent tujuan:
002

Skrip endpoint:
delete-malware.sh

## 6. Backup yang Tersedia

Ubuntu Victim:
[Path arsip]

Wazuh Manager:
[Path backup]

Wazuh Indexer:
[Path backup]

Wazuh Dashboard:
[Path backup]

Shuffle:
[Path ekspor workflow dan catatan]

Docker:
[Path Compose/stack dan inventaris]

libvirt:
[Path XML VM dan network]

Host IPv6:
[Path backup konfigurasi jaringan]

## 7. Batasan Backup

Backup ini mencakup konfigurasi dan definisi deployment.

Backup ini belum otomatis mencakup seluruh isi disk VM,
data indeks Wazuh, dan database persisten Shuffle.

## 8. Validasi

Checksum:
[Path file SHA256SUMS]

Status pemeriksaan:
[Belum diperiksa / Sudah diperiksa]

Catatan:
[Tambahkan error atau komponen yang belum tersimpan]
