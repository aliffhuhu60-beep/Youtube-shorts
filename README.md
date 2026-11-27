# 🌍 Wondrift — Projek Channel YouTube Faceless (English)

Projek lengkap untuk membina channel YouTube **faceless** dalam **Bahasa Inggeris** (audiens global),
fokus pada **YouTube Shorts** dan disusuli video panjang. Semua dokumen panduan ditulis dalam Bahasa
Melayu; semua kandungan video (skrip, tajuk, deskripsi) dalam Bahasa Inggeris.

> **Nama channel cadangan utama: `Wondrift`** — *Wonder + Drift* — "drift through the world's wonders". Nama ciptaan baharu: carian web tidak menjumpai sebarang channel/jenama lain dengan nama ini (Nov 2026).
> Alternatif ada dalam [docs/02-jenama-channel.md](docs/02-jenama-channel.md).

## Struktur projek

| Fail | Isi |
|---|---|
| [docs/01-kajian-niche.md](docs/01-kajian-niche.md) | Kajian format Shorts/video faceless yang famous, kenapa ia viral, niche dipilih |
| [docs/02-jenama-channel.md](docs/02-jenama-channel.md) | Nama channel, logo, banner, gaya seni unik, prompt AI untuk gambar |
| [docs/03-undang-undang-copyright.md](docs/03-undang-undang-copyright.md) | Syarat legal YouTube, copyright, AI disclosure, senarai semak sebelum upload |
| [docs/04-aliran-kerja-produksi.md](docs/04-aliran-kerja-produksi.md) | Cara buat 1 Short dari idea → upload (alat percuma / murah) |
| [docs/05-monetisasi.md](docs/05-monetisasi.md) | Pelan jana duit: YPP, affiliate, digital product, sponsor |
| [content/skrip-30-hari.md](content/skrip-30-hari.md) | 30 idea Short + 5 skrip penuh siap rakam |
| [templates/](templates/) | Templat skrip, tajuk & deskripsi |
| [assets/](assets/) | Logo (`logo.svg`) & banner (`banner.svg`) asal — milik anda sepenuhnya |
| [tools/make_short.py](tools/make_short.py) | Skrip Python + ffmpeg: gabung gambar + suara + sari kata → video 9:16 |
| [tools/voice_kokoro.py](tools/voice_kokoro.py) | Suara AI percuma (Kokoro, lesen Apache-2.0) + sari kata bermasa. Suara jenama: `bm_george` |
| [tracker/video-tracker.csv](tracker/video-tracker.csv) | Jejak setiap video & prestasinya |

## Mula dalam 7 hari

1. **Hari 1** — Baca `docs/02` & `docs/03`. Cipta akaun Google baharu khas untuk channel, buat channel `Wondrift`, pasang 2-Step Verification.
2. **Hari 2** — Upload `assets/logo.png` (800×800) & `assets/banner.png` (2560×1440). Isi About, link, keyword.
3. **Hari 3** — Pilih 3 skrip dari `content/skrip-30-hari.md`. Jana suara & visual ikut `docs/04`.
4. **Hari 4–5** — Hasilkan 3 Short pertama dengan `tools/make_short.py` atau CapCut.
5. **Hari 6** — Semak senarai semak legal (`docs/03`) → upload. 
6. **Hari 7** — Isi `tracker/video-tracker.csv`. Ulang: sasaran **1 Short sehari**, 1 video panjang seminggu selepas bulan ke-2.

## Peraturan emas
- **Original setiap kali**: skrip sendiri, visual sendiri/berlesen, suara sendiri/TTS berlesen.
- **Jangan reupload** klip orang lain, filem, anime, TV, muzik popular, atau "Reddit story + Minecraft parkour" generik.
- **Nilai tambah**: setiap video mesti ada fakta yang disemak + sudut pandangan / humor channel sendiri.
- **Konsisten** > sempurna. Data (retention, swipe rate) menentukan apa yang dibuat seterusnya.
