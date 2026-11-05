# Dokumentasi dan Backup Sistem Penelitian Skripsi

**Judul skripsi:**  
RANCANG BANGUN SISTEM OTOMATISASI REMEDIASI MALWARE MENGGUNAKAN INTEGRASI SIEM WAZUH DAN SHUFFLE SOAR BERBASIS PENGUKURAN MTTR DI LINGKUNGAN IPV6

**Peneliti:** Ibrahim · **NIM:** 3337220054  
**Program studi:** Informatika, Universitas Sultan Ageng Tirtayasa  
**Repositori:** [Wazuh-Shuffle-SOAR-Integration](..) · [Daftar artefak utama](../00-inventory/)

Dokumen ini merupakan **catatan konfigurasi dan inventaris backup penelitian** untuk memudahkan dosen pembimbing memeriksa sistem yang dibangun. Sistem mengintegrasikan deteksi file uji EICAR melalui Wazuh FIM/YARA dengan orkestrasi Shuffle SOAR dan penghapusan file menggunakan Wazuh Active Response. Lingkungan menggunakan **IPv6 pada komunikasi agent–host** dan **IPv4 pada integrasi layanan Docker**, bukan IPv6 *end-to-end*.

## 1. Identitas dan ruang lingkup backup

| Parameter | Data tercatat | Status |
|---|---|---|
| Waktu pembuatan backup | **Belum dapat dipastikan** dari artefak baseline yang tersedia | Periksa metadata arsip/manifest pada repositori |
| Hostname Ubuntu Host | **Belum terkonfirmasi** | Periksa inventaris host |
| Perangkat | Axioo Hype 7 AMD X8 | Baseline implementasi |
| Sistem operasi host | Ubuntu 24.04.5 LTS, x86_64 | Snapshot pemeriksaan |
| CPU host | AMD Ryzen 7 6800H, 8 core/16 thread | Baseline implementasi |
| RAM yang dilaporkan OS | 13.705 MiB (sekitar 13,4 GiB) | Bukan kapasitas fisik terpasang yang diverifikasi |
| Docker Engine / Compose | 29.9.1 / v5.6.0 | Versi saat pemeriksaan, bukan versi historis setiap uji |
| Platform virtualisasi | Docker dan KVM/libvirt | Terkonfirmasi |
| Rentang pengujian utama | 13–18 Oktober 2026 | Bukan tanggal pembuatan backup |

> Catatan versi: identitas image, versi, dan status container di bawah mengacu pada pemeriksaan lingkungan yang terdokumentasi; bukan *snapshot bit-exact* dari seluruh percobaan.

## 2. Arsitektur dan komponen

| Komponen | Identitas / image / versi | Lokasi arsip |
|---|---|---|
| Wazuh Manager | `single-node-wazuh.manager-1` · `wazuh/wazuh-manager:4.14.6` | [02-wazuh-manager](../02-wazuh-manager/) |
| Wazuh Indexer | `single-node-wazuh.indexer-1` · `wazuh/wazuh-indexer:4.14.6` | [03-wazuh-indexer/config](../03-wazuh-indexer/config/) |
| Wazuh Dashboard | `single-node-wazuh.dashboard-1` · `wazuh/wazuh-dashboard:4.14.6` | [04-wazuh-dashboard/config](../04-wazuh-dashboard/config/) |
| Shuffle SOAR | Dashboard versi **2.2.1**; frontend, backend, Orborus, worker, aplikasi pendukung | [05-shuffle](../05-shuffle/) |
| Ubuntu Victim | VM `ubuntu-victim` · Ubuntu Server 24.04 · 2 vCPU, RAM 512 MiB, disk 20 GiB | [01-ubuntu-victim](../01-ubuntu-victim/) · [07-libvirt](../07-libvirt/) |
| Wazuh Agent | Nama `ubuntu-server` · Agent ID **002** · versi agent **belum dikonfirmasi secara terpisah** | [01-ubuntu-victim](../01-ubuntu-victim/) |

**Image aplikasi Shuffle yang tercatat pada snapshot Docker:** `frikky/shuffle:http_1.4.0`, `frikky/shuffle:email_1.3.0`, `frikky/shuffle:shuffle-ai_1.1.0`, `frikky/shuffle:shuffle-tools_1.2.0`, `frikky/shuffle:shuffle-subflow_1.1.0`, `frikky/shuffle:shufflehealthcheck_1.1.0`, serta `ghcr.io/shuffle/shuffle-worker:latest`. Tag `latest` tidak menetapkan versi immutable.

## 3. Jaringan penelitian

| Segmen / komponen | Interface / subnet / endpoint | Keterangan |
|---|---|---|
| Libvirt default | `virbr0` · `192.168.122.0/24` | Jaringan IPv4 default VM |
| Libvirt lab IPv6 | `virbr1` · `fd00:1111:2222:3333::/64` | Jaringan ULA endpoint–host |
| Ubuntu Host pada `virbr1` | `fd00:1111:2222:3333::1/64` | Tujuan koneksi Wazuh Agent |
| Ubuntu Victim pada `enp1s0` | `fd00:1111:2222:3333::100/64` | Alamat pada sesi agent yang teramati; VM juga memiliki alamat IPv6 lain |
| Ubuntu Victim pada jaringan default | `192.168.122.50/24` | Interface `enp7s0` pada snapshot |
| Komunikasi Wazuh Agent | `[fd00:1111:2222:3333::1]:1514` · TCP/IPv6 | Bukti sesi `ESTAB` dan paket dua arah |
| Docker Wazuh | `single-node_default` · `172.18.0.0/16` | Bridge IPv4 |
| Docker Shuffle | `shuffle_shuffle` · `172.19.0.0/16` | Bridge IPv4 |
| Shuffle execution overlay | `shuffle_swarm_executions` · `10.224.224.0/24` | Endpoint IPv4 teramati |
| Webhook Shuffle | `http://172.18.0.1:3001/…` | Endpoint IPv4; ID Webhook tidak dicantumkan |
| Wazuh API | `https://172.18.0.1:55000` | Endpoint IPv4; tanpa informasi autentikasi |

**Arsip jaringan:** [07-libvirt](../07-libvirt/) · [08-host-network](../08-host-network/) · dokumentasi verifikasi topologi yang tersimpan dalam kumpulan artefak penelitian.

## 4. Konfigurasi deteksi

| Item | Nilai terverifikasi | Arsip terkait |
|---|---|---|
| Direktori FIM utama | `/tmp/`, *realtime* | [01-ubuntu-victim](../01-ubuntu-victim/) |
| Custom rule FIM *added* | **100301**, level **7** | [02-wazuh-manager](../02-wazuh-manager/) |
| Custom rule FIM *modified* | **100300**, level **7** | [02-wazuh-manager](../02-wazuh-manager/) |
| Alert YARA positif | **108001**, level **12** | [02-wazuh-manager](../02-wazuh-manager/) |
| Rule pengelompokan YARA | **108000**, level **0** | [02-wazuh-manager](../02-wazuh-manager/) |
| Signature EICAR yang tercatat | `SUSP_Just_EICAR_RID2C24` pada **VALHALLA YARA RULE SET – DEMO** | Arsip ruleset pada bahan penelitian |
| Versi binary YARA / path scanner saat eksperimen | **Belum terverifikasi dari baseline yang tersedia** | Perlu diperiksa bila dibutuhkan untuk reproduksi |

File `eicar.yar` yang memuat aturan `eicar_av_test` **bukan** ruleset yang dikonfirmasi melalui koreksi inventaris; bukti yang relevan adalah `yara_rules(1).yar`. Ruleset demo memiliki atribusi dan ketentuan lisensi sumber yang perlu dipatuhi bila didistribusikan ulang.

## 5. Orkestrasi dan remediasi

| Tahapan | Implementasi terdokumentasi |
|---|---|
| Sumber alert | Wazuh FIM dan YARA pada Agent **002** |
| Penerusan alert | Wazuh → Webhook Shuffle; payload JSON |
| Pemrosesan workflow | Trigger Webhook → pemrosesan alert → autentikasi API → Active Response; cabang Telegram pada konfigurasi lebih baru |
| Autentikasi Wazuh API | HTTP POST `/security/user/authenticate` melalui HTTPS/IPv4 |
| Perintah remediasi | HTTP PUT `/active-response` dengan command `!delete-malware.sh` dan argument lokasi file |
| Script endpoint | `delete-malware.sh`, terbatas pada file target yang memenuhi validasi path `/tmp` |
| Bukti tindakan | Log Active Response dan pemeriksaan keberadaan file pada Ubuntu Victim |
| Event FIM penghapusan | Rule ID **553** |

**Bukti fungsional utama:** `FUNC-E2E-01` (ID **101**, 24 Oktober 2026) memuat korelasi alert, respons API, log script, dan keluaran `FILE_ABSENT`. HTTP `200` pada API **bukan** bukti tunggal keberhasilan penghapusan.

## 6. Indeks direktori backup

Tautan di bawah menggunakan path relatif **dari `09-documentation/README.md`**.

| Folder | Isi yang perlu diperiksa |
|---|---|
| [00-inventory](../00-inventory/) | Inventaris dan manifest backup |
| [01-ubuntu-victim](../01-ubuntu-victim/) | Konfigurasi endpoint dan Wazuh Agent |
| [02-wazuh-manager](../02-wazuh-manager/) | Konfigurasi Manager, rules, dan integrasi |
| [03-wazuh-indexer/config](../03-wazuh-indexer/config/) | Konfigurasi Wazuh Indexer |
| [04-wazuh-dashboard/config](../04-wazuh-dashboard/config/) | Konfigurasi Wazuh Dashboard |
| [05-shuffle](../05-shuffle/) | Ekspor workflow dan konfigurasi Shuffle yang telah disamarkan |
| [06-docker](../06-docker/) | Definisi deployment dan inventaris container |
| [07-libvirt](../07-libvirt/) | Definisi mesin virtual dan jaringan libvirt |
| [08-host-network](../08-host-network/) | Pengalamatan dan konfigurasi jaringan host |
| [09-documentation](./) | Dokumen ini serta bukti/dokumentasi sistem yang tersimpan di folder tersebut |

> **Status pemeriksaan:** nama direktori berasal dari struktur repositori yang diberikan peneliti. Isi direktori GitHub tidak berhasil diakses langsung saat README ini disusun, sehingga **nama file backup individual dan keberadaan `SHA256SUMS` di dalam repo tidak diasumsikan**.

## 7. Data pengujian yang menjadi rujukan skripsi

| Kumpulan bukti | Identitas resmi | Keterangan |
|---|---|---|
| Respons otomatis utama | ID **01–05** dan **07–11**; 10 percobaan | Sebelum integrasi Telegram |
| Respons manual utama | ID **12–21**; 10 percobaan | Deteksi FIM/YARA; remediasi oleh operator |
| Monitoring CPU/RAM | ID **07–11**; 5 monitoring | Bagian dari percobaan otomatis, bukan percobaan independen tambahan |
| Validasi fungsional tambahan | **FUNC-E2E-01 / ID 101** | Tidak digabungkan ke dataset statistik utama |

Dokumentasi pengembangan, *troubleshooting*, dan percobaan di luar manifest resmi tidak digunakan sebagai pengganti dataset utama. Dataset mentah, script pengujian, dan audit statistik merupakan **artefak penelitian terpisah dari backup konfigurasi**; penempatannya dalam repositori harus mengikuti inventaris aktual.

## 8. Batasan, integritas, dan keamanan backup

- Arsip konfigurasi dan definisi deployment **tidak otomatis berarti** seluruh disk VM (`qcow2`), volume/index Wazuh, database persisten Shuffle, atau seluruh log historis telah dibackup.
- **Checksum SHA-256:** lokasi berkas manifest dan hasil verifikasi checksum **belum dapat dipastikan** dari daftar artefak GitHub yang dapat diperiksa saat penyusunan README. Jangan menganggap checksum sudah diverifikasi hanya karena backup tersedia.
- Arsip yang dipublikasikan tidak boleh memuat password, access token, API key, Telegram bot token, ataupun URL Webhook rahasia yang masih berlaku. Konfigurasi yang disamarkan perlu ditandai sebagai **salinan dokumentasi**, bukan file siap pakai untuk deployment.
- Alamat IP internal, versi image, dan status container adalah bukti pemeriksaan pada waktu tertentu. Kondisi runtime saat demonstrasi dapat berbeda.
- Sistem diuji menggunakan **file uji EICAR**, bukan beragam malware aktif; tindakan remediasi yang dibuktikan adalah **penghapusan file**.

**Status dokumentasi:** ringkasan sistem dan baseline penelitian telah dikonfirmasi dari artefak yang tersimpan; **kelengkapan setiap file backup dan validasi checksum repositori perlu diperiksa terhadap inventaris GitHub aktual**.
