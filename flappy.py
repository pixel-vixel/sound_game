from pygame import *
from random import randint
import sounddevice as sd
import numpy as np

fr = 16000
block = 256 #^ менше значення = швидша реакція
mic_level = 0.0

def audio_cb(indata, frames, time, status):
    global mic_level
    if status:
        return
    rms = float(np.sqrt(np.mean(indata**2)))
    mic_level = 0.85 * mic_level + 0.15 * rms

init()
window_size = 1200, 800
window = display.set_mode(window_size)
clock = time.Clock()

player_rect = Rect(150, window_size[1]//2 - 50, 100, 100)

main_font = font.SysFont("Comic Sans MC", 100)

def generate_pipes(count, pipe_width=140, gap=280, min_h=50, 
                   max_h=450, dist=650):
    pipes = []
    start_x = window_size[0]
    for i in range(count):
        h = randint(min_h, max_h)
        top_p = Rect(start_x, 0, pipe_width, h)
        bottom_p = Rect(start_x, h + gap, pipe_width, window_size[1] - h - gap)
        pipes.extend([top_p, bottom_p])
        start_x += dist
    return pipes

pipes = generate_pipes(100)
wait = 40
score = 0
y_vel = 0.0
gravity = 0.6
THRESH = 0.001
IMPULSE = -8.0

loose = False

with sd.InputStream(samplerate=fr, channels=1, blocksize=block, callback=audio_cb):
    while True:
        for e in event.get():
            if e.type == QUIT:
                quit()

        if mic_level > THRESH:
            y_vel = IMPULSE
        y_vel += gravity
        player_rect.y += int(y_vel)

        window.fill('blue')
        draw.rect(window, 'gold', player_rect)

        

        for p in pipes[:]:
            if not loose:
                p.x -= 10
            draw.rect(window, "green", p)
            if p.x <= -100:
                score += 1
                pipes.remove(p)
            if player_rect.colliderect(p):
                loose = True
        if len(pipes) < 8:
            pipes += generate_pipes(100)

        score_text = main_font.render(f"{int(score)}", 1, 'black')
        window.blit(score_text, (window_size[0]//2 - score_text.get_rect().w//2, 40))

        display.update()
        clock.tick(60)
        
        keys = key.get_pressed()
        if keys[K_r] and loose:
            loose = False
            pipes = generate_pipes(100)
            player_rect.y = window_size[1]//2 - 100
            y_vel = 0
        
        if player_rect.bottom > window_size[1]:
            player_rect.bottom = window_size[1]
            y_vel = 0.0

        if player_rect.top < 0:
            player_rect.top = 0
            if y_vel < 0:
                y_vel = 0

        if loose and wait > 1:
            for pipe in pipes:
                pipe.x += 8
            wait -= 1
        else:
            loose = False
            wait = 40

        