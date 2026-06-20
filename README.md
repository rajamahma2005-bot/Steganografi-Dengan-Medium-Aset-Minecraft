# Multi-Image LSB Steganography (Minecraft Asset Edition)

Implementasi steganografi LSB (*Least Significant Bit*) yang menyisipkan satu pesan rahasia ke **sekumpulan file PNG** sekaligus, bukan ke satu gambar saja. Dibuat sebagai tugas makalah mata kuliah II4021 Kriptografi, Institut Teknologi Bandung.

Medium yang dipakai adalah aset gambar dari **Minecraft** (skin karakter, tekstur objek, dll). Resolusi aset Minecraft yang relatif kecil (umumnya 64×64 piksel) membuat kapasitas LSB per gambar terbatas — inilah yang memotivasi pendekatan *multi-image*, di mana pesan didistribusikan ke beberapa file sekaligus alih-alih dipaksakan ke satu gambar.

## Fitur

- **DFS folder traversal** — menyusuri folder target secara rekursif untuk menemukan semua file `.png`, termasuk yang berada di subfolder.
- **Pengurutan deterministik** — hasil traversal diurutkan secara alfabetis (dengan tie-break pada full path) agar urutan file selalu konsisten antara proses penyisipan dan ekstraksi.
- **Length-header bitstream** — pesan di-encode UTF-8, lalu diberi header 32-bit berisi panjang pesan, sehingga proses ekstraksi tahu persis kapan harus berhenti membaca bit (sisa kapasitas gambar tidak ikut terbaca sebagai pesan).
- **Capacity check** — total kapasitas LSB seluruh gambar divalidasi terhadap panjang bitstream *sebelum* proses penyisipan dimulai.
- **Distribusi sequential-fill** — satu gambar diisi penuh (atau sampai pesan habis) sebelum pindah ke gambar berikutnya, sesuai urutan pada file `daftar_png.txt`.
- **Deteksi stego-image** — proses ekstraksi dapat membedakan PNG hasil sisipan program ini dari PNG biasa tanpa perlu hash pembanding, dengan menangkap kegagalan baca bit/decode secara graceful.

## Cara Kerja Singkat

### Proses Penyisipan

1. Input path folder target.
2. DFS rekursif untuk menemukan seluruh file `.png` di dalam folder (termasuk subfolder).
3. Urutkan path hasil DFS secara alfabetis, tulis ke `daftar_png.txt`.
4. Pesan rahasia di-encode jadi bitstream (header 32-bit + isi UTF-8).
5. Validasi kapasitas total gambar terhadap panjang bitstream.
6. Sisipkan bit ke channel R, G, B tiap piksel (alpha tidak disentuh), urut sesuai `daftar_png.txt`, satu gambar diisi sampai penuh/pesan habis sebelum lanjut ke gambar berikutnya.
7. Gambar di-*overwrite* langsung menjadi stego-image.

### Proses Ekstraksi

1. Input path file `daftar_png.txt` (acuan urutan yang sama dipakai saat penyisipan).
2. Baca bit LSB dari tiap gambar sesuai urutan tersebut.
3. Parse 32 bit pertama sebagai header panjang pesan.
4. Baca sisanya sebanyak panjang pesan, decode UTF-8.
5. Jika gambar bukan stego-image (kapasitas tidak cukup / hasil decode tidak valid), proses gagal dengan pesan error yang jelas — bukan *crash*.

> **Penting:** `daftar_png.txt` adalah satu-satunya sumber urutan yang sah untuk kedua proses. Ekstraksi tidak melakukan DFS ulang ke folder, karena urutan hasil `os.scandir` bersifat *OS-dependent* dan berisiko berbeda antar waktu/environment.

## Struktur Proyek

```
.
├── stego.py        # Proses penyisipan: DFS, sort, txt, bitstream, embed
├── Ekstraksi.py     # Proses ekstraksi: baca txt, baca LSB, decode pesan
└── README.md
```

## Requirements

- Python 3.10+
- [Pillow](https://pypi.org/project/Pillow/)

```bash
pip install Pillow
```

## Cara Pakai

### 1. Penyisipan pesan

```bash
python stego.py
```

Program akan meminta:
- Path folder yang berisi PNG (boleh ada subfolder).
- Pesan rahasia yang ingin disisipkan.

Output: seluruh PNG di folder ter-*overwrite* menjadi stego-image (sebagian, sesuai kapasitas yang terpakai), serta file `daftar_png.txt` yang mencatat urutan file.

### 2. Ekstraksi pesan

```bash
python Ekstraksi.py
```

Program akan meminta path ke `daftar_png.txt` yang dihasilkan pada langkah penyisipan, lalu menampilkan pesan rahasia hasil ekstraksi.

## Keterbatasan & Pengembangan Lanjutan

- Distribusi bit antar gambar bersifat *sequential-fill*, bukan rata (*even distribution*) — lebih sederhana, namun secara steganalysis lebih mudah dicurigai karena perubahan menumpuk di gambar-gambar awal saja.
- Belum ada enkripsi pesan sebelum disisipkan — pesan hanya disembunyikan (steganografi), belum dirahasiakan secara kriptografis.
- Rencana pengembangan: pengambilan aset Minecraft secara otomatis dari sumber daring, serta mekanisme proteksi stego-image (kunci akses, pembatasan rename/copy) menggunakan password yang digenerate sistem.

## Author

Dikembangkan untuk Tugas Makalah II4021 Kriptografi, Program Studi Sistem dan Teknologi Informasi, Institut Teknologi Bandung
