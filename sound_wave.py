from pygame import *
import sounddevice as sd

fs = 22050
chunk = 1024
WIDTH, HEIGHT = 800, 400

init()
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Sound Wave")
clock = time.Clock()

data = [0.0] * chunk

def audio_callback(indata, frames, time_info, status):
    global data
    if status:
        print(status)
    data = [sample * (HEIGHT // 2) for sample in indata[:, 0].tolist()]

stream = sd.InputStream(
    callback=audio_callback, 
    channels=1, 
    samplerate=fs, 
    blocksize=chunk, 
    dtype="float32"
)
stream.start()

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    screen.fill((0, 0, 0))

    points = []
    for i, sample in enumerate(data):
        x = int(i * WIDTH / chunk)
        y = int(HEIGHT // 2 + sample)
        points.append((x, y))

    if len(points) > 1:
        draw.lines(screen, (0, 255, 0), False, points, 2)

    display.update()
    clock.tick(60)

stream.stop()
quit()