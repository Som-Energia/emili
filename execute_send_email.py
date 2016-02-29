#! /usr/bin/env python2
# -*- encoding: utf8 -*-
# Execute this: ./execute_send_email.py -c SMTP_CONFIG.PY_PATH  -s SUBJECT -t RECIPIENT [-t RECIPIENT2] [-t RECIPIENT3] -- "pip freeze | wc -l" (Command within quotes and after "--"]
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
        '-c',
        '--config',
        required=True,
        dest='config',
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
    os.system(command+" 2>&1 | PYTHONPATH=$PYTHONPATH:"+args.config+" emili.py -f sender@example.org -s "+args.subject+" "+" ".join(["-t "+arg for arg in args.to])+" >>/tmp/output_emili.txt 2>&1")
if __name__ == '__main__':
    main()
