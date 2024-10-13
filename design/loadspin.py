import time
from primePy import primes

symbols = ["|", "/", "—", "\\"]

def load():
    pos=0
    print(" ", end="")
    while True:
        time.sleep(0.1)
        print("" + symbols[pos], end="", flush=True)
        pos = (pos + 1) % 3
        
def primesGet():
    return primes.first(10000)

def test():
    print("Loading... ",end="")
    p = Process(target=load)
    p.start()
    r = primesGet()
    p.kill()

    print("\nDone!")
