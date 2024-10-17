#!/bin/python3

import loadspin as ls
# Used to display a fancy little loading animation
import argparse as ap
# ArgumentParser

__VERSION__ = "0.0.1"
__SETTINGS__ = "settings.json"
# Define basic information

def arginit():
    parser = ap.ArgumentParser(
        prog="WCTA Browser")
    
    parser.add_argument("-I", "--interactive", 
                        action="store_true")
    
    return parser.parse_args()

def main():
    args = arginit()
    if args.interactive:
        print("WCTA Browser v{}".format(__VERSION__))

if __name__ == "__main__":
    main()
