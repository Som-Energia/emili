# Emili

Simple interface for sending mails. Turns input formats
such as Markdown or console outputs using ANSI colors
into nice dual plaintext/html messages.
You may specify an html skeleton and a css file
which are turn mail compatible.

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
    subject = "About this email"
    md = content,
    attachments = [ 'onefile.pdf' ],
	config = '../config.py',
    )
```


Right now a config.py file is required containing the configuration options
for the SMTP connection in a dictionary named `smtp`:

```python
smtp=dict(
    host='smtp.acme.cat',
    port=465,
    user='roadrunner@acme.cat',
    password='mecmec',
)
```


## Command line usage

```
usage: emili.py [-h] -f SENDER -s SUBJECT -t recipient [--body TEXT]
                [--bodyfile BODYFILE] [-C CONFIG.PY] [-c CC] [-b BCC]
                [-r REPLYTO] [--format FORMAT] [--style CSSFILE]
                [--template TEMPLATE] [--dump OUTPUTFILE.eml]
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
  -C CONFIG.PY, --config CONFIG.PY
                        Python Module with smtp configuration defined.
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
  --dump OUTPUTFILE.eml
                        Instead of sending, dump the email into a file
```

## reportrun

```
usage: reportrun [-h] -s SUBJECT -t RECIPIENT [-f SENDER] [-C CONFIG.PY]
                [FILE [FILE ...]] -- COMMAND [COMMAND_ARG ...]

reportrun wraps the execution of a command and sends an email
whenever the command fails. The mail sending is processed by
emili so that ansi codes and spacing are shown properly.

positional arguments:
  FILE                  File to attach
  COMMAND               Command to run
  COMMAND_ARG           Argument for COMMAND

optional arguments:
  -f SENDER, --from SENDER
                        Message sender ('From:' header)
  -s SUBJECT, --subject SUBJECT
                        Message subject ('Subject:' header)
  -t recipient, --to recipient
                        Message recipient ('To:' header) (multiple)
  -C CONFIG.PY, --config CONFIG.PY
                        Python Module with smtp configuration defined.
  -a, --always
                        Sends even if the command does not fail.
  --
                        Marks the start of the command to execute.
```

## Changelog

### 1.7 (UNRELEASED)

- Removed `execute_send_mail.py`

### 1.6 (2019-10-09)

- Fix: reportrun ignored endlines
- reportrun accepts attatchment
- reportrun --help option and documented in README

### 1.5 (2018-10-15)

- Added `reportrun` script

### 1.4 (2017-07-02)

- Fix: dump does not require configuration

### 1.3 (2016-11-02)

- `--dump` option to dump the resulting email as file instead of sending it
- Fix: Better processing addresses in the format `Me <me@here.org>`
- Fix: Do not take the full path as attachment name
- `activate_wrapper.sh` moved to `somenergia-utils` repo

### 1.2 (2016-03-28)

- Option `-c`/`--config` to explicit configuration file
- Added wrapper `execute_send_mail.sh`
- Added wrapper `activate_wrapper.sh`

### 1.1 (2016-01-12)

- Available on PyPi

### 1.0 (2016-01-12)

- First version

