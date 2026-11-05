# Rancang Bangun Sistem Otomatisasi Remediasi Malware Menggunakan Integrasi SIEM Wazuh dan Shuffle SOAR Berbasis Pengukuran MTTR di Lingkungan IPv6

Repositori ini merupakan **lampiran digital skripsi** yang menyimpan arsip konfigurasi, inventaris lingkungan, dokumentasi jaringan, bukti implementasi dan pengujian, serta data dan berkas pengolahan penelitian integrasi Wazuh SIEM–Shuffle SOAR. Pengujian menggunakan file uji EICAR pada lingkungan laboratorium **hybrid IPv6–IPv4**: komunikasi Wazuh Agent menuju host menggunakan IPv6, sedangkan integrasi internal Docker menggunakan IPv4.

## Struktur direktori

```text
.
├── 00-inventory/
├── 01-ubuntu-victim/
├── 02-wazuh-manager/
├── 03-wazuh-indexer/
│   └── config/
├── 04-wazuh-dashboard/
│   └── config/
├── 05-shuffle/
├── 06-docker/
├── 07-libvirt/
├── 08-host-network/
└── 09-documentation/
```

## Navigasi artefak

| Jenis data atau bukti | Direktori untuk penelusuran | Keterangan |
|---|---|---|
| Inventaris dan spesifikasi lingkungan | [`00-inventory/`](00-inventory/) | Inventaris arsip dan identitas lingkungan penelitian |
| Arsitektur, dokumentasi, dan bukti implementasi | [`09-documentation/`](09-documentation/) | Dokumentasi pendukung penelitian; path file spesifik perlu dikonfirmasi |
| Konfigurasi Wazuh Agent dan endpoint Ubuntu Victim | [`01-ubuntu-victim/`](01-ubuntu-victim/) | Artefak endpoint pengujian |
| Konfigurasi Wazuh Manager, deteksi FIM/YARA, dan Active Response | [`02-wazuh-manager/`](02-wazuh-manager/) dan [`01-ubuntu-victim/`](01-ubuntu-victim/) | Lokasi file konfigurasi/ruleset spesifik perlu dikonfirmasi |
| Konfigurasi Wazuh Indexer dan Dashboard | [`03-wazuh-indexer/config/`](03-wazuh-indexer/config/) dan [`04-wazuh-dashboard/config/`](04-wazuh-dashboard/config/) | Konfigurasi layanan Wazuh |
| Workflow dan artefak integrasi Shuffle SOAR | [`05-shuffle/`](05-shuffle/) | Berkas workflow, Webhook, dan integrasi; path file spesifik perlu dikonfirmasi |
| Container, image, dan konfigurasi Docker | [`06-docker/`](06-docker/) | Inventaris serta konfigurasi lingkungan container |
| Mesin virtual dan jaringan libvirt | [`07-libvirt/`](07-libvirt/) | Konfigurasi Ubuntu Victim dan virtualisasi |
| Konfigurasi dan bukti jaringan IPv6–IPv4 | [`08-host-network/`](08-host-network/), [`07-libvirt/`](07-libvirt/), dan [`09-documentation/`](09-documentation/) | Interface, routing, dan bukti konektivitas; path bukti spesifik perlu dikonfirmasi |
| Pengujian fungsional dan bukti penghapusan file (FUNC-E2E-01) | [`09-documentation/`](09-documentation/) dan [`05-shuffle/`](05-shuffle/) | Lokasi file log, tangkapan layar, dan pemeriksaan filesystem **belum terverifikasi** |
| Dataset waktu respons otomatis dan manual | [`00-inventory/`](00-inventory/) | **Path dataset perlu dikonfirmasi**; terdiri atas 20 percobaan utama |
| Dataset monitoring CPU/RAM | [`00-inventory/`](00-inventory/) | **Path dataset perlu dikonfirmasi**; mencakup monitoring ID 07–11 |
| Script pengujian, monitoring, dan analisis | [`00-inventory/`](00-inventory/) | **Path masing-masing script perlu dikonfirmasi** |
| Hasil pengolahan statistik tervalidasi | [`00-inventory/`](00-inventory/) | **Path berkas hasil audit/statistik perlu dikonfirmasi** |
