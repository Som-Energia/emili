# Emili

Simple interface for sending mails. Turns input formats
such as Markdown or console outputs using ANSI colors
into nice dual plaintext/html messages.


## Module usage


```python
import emili

content = """
# this is a title

Read **this** is very _important_!!

"""

emili.sendmail(
    from  = "me@acme.cat",
    to = [ "abe@acme.cat", "bill@acme.cat" ],
    bcc = [ "me@acme.cat" ],
    subject = []
    md = content,
    attachments = [ 'onefile.pdf' ],
    )
```

Right now a config.py file is required containing the configuration options
for the SMTP connection in a dictionary named `smtp`:

```python
smtp={
    host='smtp.acme.cat',
    port='',
    user='roadrunner@acme.cat',
    password='mecmec',
}
```


## Command line usage

```
usage: emili.py [-h] -f SENDER -s SUBJECT -t recipient [--body TEXT]
                [--bodyfile BODYFILE] [-c CC] [-b BCC] [-r REPLYTO]
                [--format FORMAT] [--style CSSFILE] [--template TEMPLATE]
                [FILE [FILE ...]]

Sends an email.

positional arguments:
  FILE                  File to attach

optional arguments:
  -h, --help            show this help message and exit
  -f SENDER, --from SENDER
                        Message sender ('From:' header)
  -s SUBJECT, --subject SUBJECT
                        Message subject ('Subject:' header)
  -t recipient, --to recipient
                        Message recipient ('To:' header) (multiple)
  --body TEXT           Message body (defaults to stdin)
  --bodyfile BODYFILE   File containing the message body (defaults to stdin)
  -c CC, --cc CC        Message copy recipient ('CC:' header) (multiple)
  -b BCC, --bcc BCC     Message hidden copy recipient ('BCC:' header)
                        (multiple), other recipients won't see this header
  -r REPLYTO, --replyto REPLYTO
                        Default address to reply at ('Reply-To:' header)
                        (multiple)
  --format FORMAT       Format for the body. 'md' takes markdown and generates
                        both html and text. 'ansi' does the same, turning ANSI
                        color codes in html or stripping them for text.
  --style CSSFILE       Style sheet for the html output, (multiple)
  --template TEMPLATE   Alternative template for the html body.
```
