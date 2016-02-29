#! /usr/bin/env python2
# -*- encoding: utf8 -*-

import argparse
import subprocess
import os

def main():
    parser = argparse.ArgumentParser(
        description="Execute a command and send an email with its output"
        )
    parser.add_argument(
        '-s',
        '--subject',
        required=True,
        dest='subject',
        help="Message subject ('Subject:' header)",
        )
    parser.add_argument(
        '-t',
        '--to',
        dest='to',
        required=True,
        metavar='recipient',
        action='append',
        help="Message recipient ('To:' header) (multiple)",
        )
    parser.add_argument("command", nargs=argparse.REMAINDER)    

    args = parser.parse_args()
    command = " ".join(args.command[1:])
    os.system(command)

if __name__ == '__main__':
    main()
