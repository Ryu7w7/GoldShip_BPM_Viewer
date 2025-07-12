# Gold Dance

GIF in sync with osu! music BPM using StreamCompanion
![](https://i.imgur.com/UnHoFzL.gif)

---

## Features

- Reads current BPM via StreamCompanion WebSocket
- GIF animation synced to the music beat
- Toggle BPM display on/off
- Can be compiled into a console-free `.exe`

---

## Requirements

- StreamCompanion running locally
- Python 3.10+ (only if running the script)
- Python libraries:
  - pygame
  - Pillow
  - websockets

No Python needed if you use the compiled `.exe`.

---

## How to Run

### Run with Python

```bash
pip install pygame pillow websockets
python goldship_dance.py
```
### Run with Release

```bash
To run:
- Download GoldShip_BPM_Viewer.exe
- Double-click to start!
```
⚠️ Note:
Windows Defender or some antivirus software may flag the EXE as unknown or unsafe because it’s unsigned. This is a false positive—the app is safe.
