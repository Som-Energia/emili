#! /bin/bash
source $VIRTUALENV_PATH/bin/activate

"$@" > /tmp/buffer.txt 2>&1 
if [ $? -ne 0 ]; then
  emili.py  -f prueba@example.com -s $SUBJ_EMAIL -t $RCPT_EMAIL --bodyfile /tmp/buffer.txt >>/tmp/salida_emili.txt 2>&1
fi
