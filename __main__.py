# Run on a file and fix license

import argparse
from __init__ import Fix

parser = argparse.ArgumentParser(
    description="Change license of maya file.")
parser.add_argument("license", help="License name.", type=str)
parser.add_argument("input", help="File for processing.", type=str)
args = parser.parse_args()
Fix(args.license).fixfile(args.input)
