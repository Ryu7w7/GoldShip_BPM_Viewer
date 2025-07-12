import pygame
import time
import os
import threading
import re
from PIL import Image
import asyncio
import websockets
import json
import sys

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS

else:
    base_path = os.path.dirname(os.path.abspath(__file__))

GIF_PATH = os.path.join(base_path, "goldship.gif")

WINDOW_SIZE = (480, 480)
FPS = 60

bpm = 120.0
beats_per_loop = 2
fondo_verde = True
mostrar_bpm = True

def iniciar_websocket():
    asyncio.run(websocket_main())

async def websocket_main():
    global bpm
    url = "ws://localhost:20727/tokens"
    try:
        async with websockets.connect(url) as websocket:
            print("Conectado a StreamCompanion WebSocket.")

            tokens_to_watch = ["currentBpm"]
            await websocket.send(json.dumps(tokens_to_watch))
            print("Suscrito a tokens:", tokens_to_watch)

            while True:
                message = await websocket.recv()
                data = json.loads(message)
                if "currentBpm" in data:
                    try:
                        bpm_value = float(data["currentBpm"])
                        if bpm_value > 0:
                            bpm = bpm_value
                            print("Nuevo BPM:", bpm)
                    except Exception as e:
                        print("Error al convertir BPM:", e)
    except Exception as e:
        print("Error conectando al WebSocket:", e)

threading.Thread(target=iniciar_websocket, daemon=True).start()

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Gold Ship BPM Viewer")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

gif = Image.open(GIF_PATH)
frames = []

try:
    while True:
        frame = gif.copy().convert("RGBA")
        mode = frame.mode
        size = frame.size
        data = frame.tobytes()
        py_image = pygame.image.fromstring(data, size, mode)
        frames.append(py_image)
        gif.seek(gif.tell() + 1)
except EOFError:
    pass

num_frames = len(frames)
loop_start_time = time.time()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                fondo_verde = not fondo_verde
            elif event.key == pygame.K_h:
                mostrar_bpm = not mostrar_bpm

    beat_duration = 60.0 / bpm if bpm > 0 else 0.5
    loop_duration = beats_per_loop * beat_duration
    frame_duration = loop_duration / num_frames

    elapsed = time.time() - loop_start_time

    if elapsed >= loop_duration:
        loop_start_time = time.time()
        elapsed = 0

    progress = elapsed / loop_duration
    frame_index = int(progress * num_frames) % num_frames

    if fondo_verde:
        screen.fill((0, 255, 0))
    else:
        screen.fill((0, 0, 0))

    gif_frame = frames[frame_index]
    screen.blit(gif_frame, gif_frame.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2)))

    if mostrar_bpm:
        bpm_text = font.render(f"BPM: {bpm:.2f}", True, (0, 0, 0) if fondo_verde else (255, 255, 255))
        screen.blit(bpm_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
