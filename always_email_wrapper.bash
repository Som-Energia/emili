#! /bin/bash
source $VIRTUALENV_PATH/bin/activate
"$@" 2>&1 | emili.py -f prueba@example.com -s $SUBJ_EMAIL -t $RCPT_EMAIL >/tmp/salida_emili.txt 2>&1

