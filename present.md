
---

### ✅ 1. `GET /` - Root
```powershell
curl.exe --% -X GET http://localhost:8000/s
```

---

### ✅ 2. `POST /tts` - Teks ke Suara (gTTS)
```powershell
curl.exe --% -X POST http://localhost:8000/tts -H "Content-Type: application/json" -d "{\"text\": \"Di sebuah desa kecil di kaki gunung, hiduplah seorang anak bernama Bima. Ia senang bermain di sawah bersama teman-temannya setiap sore. Suatu hari, Bima menemukan seekor burung kecil yang terluka di pinggir jalan. Dengan hati-hati, ia membawanya pulang dan merawatnya hingga sembuh. Setiap pagi, burung itu berkicau merdu di jendela kamarnya. Berkat kebaikan hatinya, Bima dikenal sebagai anak yang penyayang binatang. Ia pun bercita-cita menjadi dokter hewan saat besar nanti. Kisah Bima menjadi inspirasi bagi anak-anak lain di desanya.\", \"lang\": \"id\", \"slow\": false}" --output tts_test.mp3
```

---

### ✅ 3. `POST /stt` - Suara ke Teks  
> *Catatan: File `input/speech.mp3` harus tersedia*
```powershell
curl.exe --% -X POST http://localhost:8000/stt
```

---

### ✅ 4. `POST /sts` - Suara ke Suara  
> *Catatan: File `input/speech.mp3` juga harus tersedia*
```powershell
curl.exe --% -X POST "http://localhost:8000/sts?lang=id&slow=false" --output sts.mp3
```

---

### ✅ 5. `POST /tts/zyphra` - TTS via Zyphra
```powershell
curl.exe --% -X POST http://localhost:8000/tts/zyphra -H "Content-Type: application/json" -d "{\"text\": \"Di sebuah desa kecil di kaki gunung, hiduplah seorang anak bernama Bima. Ia senang bermain di sawah bersama teman-temannya setiap sore. Suatu hari, Bima menemukan seekor burung kecil yang terluka di pinggir jalan. Dengan hati-hati, ia membawanya pulang dan merawatnya hingga sembuh. Setiap pagi, burung itu berkicau merdu di jendela kamarnya. Berkat kebaikan hatinya, Bima dikenal sebagai anak yang penyayang binatang. Ia pun bercita-cita menjadi dokter hewan saat besar nanti. Kisah Bima menjadi inspirasi bagi anak-anak lain di desanya.\", \"speaking_rate\": 15, \"model\": \"zonos-v0.1-transformer\", \"fmax\": 22050, \"pitch_std\": 45.0, \"language_iso_code\": \"id\", \"mime_type\": \"audio/mpeg\", \"emotion\": {\"happiness\": 0.6, \"sadness\": 0.05, \"disgust\": 0.05, \"fear\": 0.05, \"surprise\": 0.05, \"anger\": 0.05, \"other\": 0.5, \"neutral\": 0.6}}" --output tts_zyphra_test.mp3
```

---

### ✅ 6. `POST /tts/clone` - Clone Suara  
> *Catatan: File `input/clone_test.wav` harus tersedia*
```powershell
curl.exe --% -X POST http://localhost:8000/tts/clone -H "Content-Type: application/json" -d "{\"text\": \"Ini adalah suara hasil cloning\"}" --output clone.mp3
```

---
