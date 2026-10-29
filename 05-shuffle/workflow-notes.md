# Workflow: EICAR Malware Detection and Remediation

## Tujuan
Menerima alert malware dari Wazuh dan mengorkestrasi remediasi
pada Ubuntu Victim melalui Wazuh API.

## Trigger
Wazuh webhook, dengan alert JSON.

## Node 1: Webhook
Menerima alert deteksi malware dari Wazuh.

## Node 2: Repeat Back to Me
Digunakan untuk verifikasi struktur alert yang diterima.

## Node 3: Wazuh Authentication
HTTP POST ke endpoint autentikasi Wazuh API.

## Node 4: Active Response
HTTP PUT untuk mengirim perintah Active Response ke Agent 002.

## Node 5: Email
Notifikasi hasil remediasi, jika digunakan.

## Kriteria keberhasilan
File target benar-benar tidak ada setelah skrip remediasi dijalankan,
dan hasilnya dikonfirmasi melalui bukti pada endpoint.