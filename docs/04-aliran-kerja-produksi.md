# 04 — Aliran Kerja Produksi (1 Short ≈ 60–90 minit)

## Peralatan (bajet RM0 → RM100/bulan)

| Langkah | Percuma | Naik taraf (pilihan) |
|---|---|---|
| Kajian & skrip | ChatGPT/Claude (draf) + Wikipedia → sumber asal | — |
| Suara | Suara sendiri (telefon + selimut = "studio"), CapCut TTS | ElevenLabs Starter (lesen komersial) |
| Visual | Canva, Ideogram/Leonardo (kuota percuma), Pexels/NASA | Canva Pro, Midjourney / Firefly |
| Suntingan | CapCut Desktop, DaVinci Resolve, `tools/make_short.py` | — |
| Sari kata | Auto-caption CapCut, atau fail `.srt` sendiri | — |
| Thumbnail video panjang | Canva | — |
| Analitik | YouTube Studio, vidIQ (percuma) | vidIQ Boost |

> Tip suara: suara manusia sendiri (walaupun beraksen) membina kepercayaan & mengurangkan risiko "inauthentic". Jika guna TTS, pilih **satu** suara dan kekalkan sebagai "suara jenama".

## Langkah demi langkah

1. **Idea (5 min)** — pilih dari `content/skrip-30-hari.md` atau kajian mingguan.
2. **Penyelidikan (15 min)** — cari 2 sumber (NASA, National Geographic, Britannica, jurnal, muzium). Tulis link dalam tracker.
3. **Skrip (15 min)** — guna `templates/script-template.md`. 70–110 patah perkataan ≈ 30–45 saat.
   - Baris 1 = hook. Baris akhir = loop ke baris 1.
   - Baca kuat-kuat; buang setiap perkataan yang tidak perlu.
4. **Suara (10 min)** — rakam/eksport `voice.mp3`. Buang senyap di awal.
5. **Visual (20 min)** — 8–15 gambar 1080×1920 gaya *Paper Atlas* (satu setiap 2–3 saat). Namakan `01.png, 02.png…`
6. **Pemasangan (10 min)** — 
   ```bash
   python3 tools/make_short.py --images shorts/ep01/img --audio shorts/ep01/voice.mp3 --srt shorts/ep01/subs.srt --out shorts/ep01/final.mp4
   ```
   Atau buat dalam CapCut: tambah zoom perlahan (Ken Burns), sari kata besar, whoosh kertas.
7. **Muzik** — latar belakang -25 dB hingga -30 dB di bawah suara (Audio Library).
8. **Semakan** — tonton di telefon. Hook kuat? Sari kata tidak ditutup UI YouTube (elak 15% bawah & kanan)?
9. **Upload** — guna `templates/upload-template.md`. Senarai semak legal `docs/03`.
10. **Rekod** — isi tracker. Selepas 48 jam catat views, % "viewed vs swiped away", avg % viewed.

## Jadual mingguan cadangan
| Hari | Tugas |
|---|---|
| Ahad | Kajian trend + tulis 7 skrip (batching) |
| Isnin | Rakam 7 suara + jana visual |
| Selasa–Rabu | Sunting 7 Shorts |
| Setiap hari | Upload 1 Short (jadual: 7–9 pagi waktu New York = 7–9 malam MYT) + balas komen 10 min |
| Sabtu | Semak analitik → 2 topik terbaik dijadikan Part 2 / video panjang |

## Membaca data (selepas 48 jam)
- **Viewed vs swiped away < 60%** → hook / visual pertama lemah. Uji hook baharu.
- **Average % viewed < 70%** → skrip terlalu panjang/meleret. Potong.
- **Average % viewed > 100%** → loop berjaya — buat lebih banyak format ini.
- **Subs dari Short** tinggi → topik itu calon siri / video panjang.
