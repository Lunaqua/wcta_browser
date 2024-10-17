import time

line = ["|", "/", "—", "\\"]
spin = ["↺", "↻"]
arrows = ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"]
# Define symbols to loop through

def load():
    pos=0
    print(" ", end="")
    while True:
        time.sleep(0.1)
        print("" + line[pos], end="", flush=True)
        pos = (pos + 1) % 3
