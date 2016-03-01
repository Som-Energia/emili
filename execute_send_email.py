#! /usr/bin/env python2
# -*- encoding: utf8 -*-
# Execute this: ./execute_send_email.py -c SMTP_CONFIG.PY_PATH  -s SUBJECT -t RECIPIENT [-t RECIPIENT2] [-t RECIPIENT3] -- "pip freeze | wc -l" (Command within quotes and after "--"]
import argparse

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
        '-C',
        '--config',
        dest='config',
        help="SMTP config.py file",
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
    parser.add_argument(
        '-e',
        '--only-if-errors',
        action="store_true",
        dest='onlyerrors',
        help="Send email only if there are errors"
        )
    parser.add_argument("command", nargs=argparse.REMAINDER)    

    args = parser.parse_args()
    command = " ".join(args.command[1:])
    if args.onlyerrors:
        from subprocess import call
        output = call(command+">/tmp/buffer_emili.txt 2>&1",shell=True)
        if output:
            call('echo "\\nError "'+str(output)+'>>/tmp/buffer_emili.txt',shell=True)
            cmd = "emili.py -f sender@example.org -s "+args.subject+" "
            cmd += " ".join(["-t "+arg for arg in args.to])
            if args.config:
                cmd+=" -C "+args.config
            cmd += " --bodyfile /tmp/buffer_emili.txt >>/tmp/output_emili.txt 2>&1"
            call(cmd,shell=True)
    else:
        from os import system
        cmd = command+" 2>&1 | emili.py -f sender@example.org"
        cmd+=" -s "+args.subject+" "+" ".join(["-t "+arg for arg in args.to])
        if args.config:
            cmd+=" -C "+args.config
        cmd+=" >>/tmp/output_emili.txt 2>&1"
        system(cmd)
if __name__ == '__main__':
    main()
