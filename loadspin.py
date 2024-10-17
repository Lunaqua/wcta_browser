# <loadspin.py> v1.0.1
# A basic library for showing a loading spinner
# 
# The MIT License (MIT)
# 
# Copyright © 2024 Navi4205 <lunaqua@proton.me>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the “Software”), to 
# deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import time                 # Required to delay the script.

line = ["|", "/", "—", "\\"]
spin = ["↺", "↻"]
arrows = ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"]
# Define symbols to loop through

def load(s=0.1):
    pos=0                   # Set up a pointer to a position in the list
    print(" ", end="")      # Print a blank space to ensure the next print 
                            #  statement does not
                            #  overwrite a previous printed character.
    m = len(line) - 1       # Calculate modulo value, save to variable to save
                            #  recalculating.
    while True:
        time.sleep(s)
        print("" + line[pos], end="", flush=True)
        pos = (pos + 1) % m
    
    # Sets up an infinite loop to print the loading spinner.
    # The speed of the animation can be controlled via the sleep duration
    # The print statement firstly prints a backspace, before printing the
    # current symbol pointed to by "pos" in the list.
    # end="" removes any newline
    # flush=True, flushes the print buffer, which is required to display
    # the character when using time.sleep
    # the pointer "pos" is iterated in a loop.
