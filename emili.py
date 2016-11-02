#!/usr/bin/env python
# -*- encoding: utf8 -*-

"""
TODO:
- Check address format
- Format markdown as nice text
- Strip ansi codes for text version
- Combining markdown intro with ansi output
"""

htmltemplate = u"""\
<html>
<meta charset="utf-8" />
<head>
<style>
{style}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def _unicode(string):
     if hasattr(str, 'decode'):
         return string.decode('utf8')
     return string
try:
    from consolemsg import step, success
except ImportError:
    import sys
    step = lambda msg: sys.stderr.write(":: "+msg+'\n')
    success = lambda msg: sys.stderr.write(">> "+msg+'\n')


def sendMail(
        sender,
        to,
        subject,
        text=None,
        html=None,
        md=None,
        ansi=None,
        cc=[],
        bcc=[],
        replyto=[],
        attachments = [],
        template=None,
        config=None,
        stylesheets = [],
        dump = None,
        verbose=True
        ):

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.encoders import encode_base64
    from email.utils import formataddr, parseaddr
    if not config:
        from config import smtp
    else:
        import imp
        smtp=imp.load_source('config',config).smtp

    def formatAddress(address):
        return formataddr(parseaddr(address))
    def formatAddresses(addresses):
        return ', '.join(formatAddress(a) for a in addresses)

    # Headers
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = formatAddress(sender)
    msg['To'] = formatAddresses(to)
    if cc: msg['CC'] = formatAddresses(cc)
    if bcc: msg['BCC'] = formatAddresses(bcc)
    if replyto: msg['Reply-To'] = formatAddresses(replyto)

    recipients = to + (cc if cc else []) + (bcc if bcc else [])

    # Attachments

    for filename in attachments:
        step("Attaching {}...".format(filename))
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(filename, "rb").read())
        encode_base64(part)
        import os
        part.add_header(
            'Content-Disposition',
            'attachment; filename="{}"'.format(
                os.path.basename(filename.replace('"', ''))))

        msg.attach(part)

    # Content formatting

    style=''
    for stylesheet in stylesheets or []:
        with open(stylesheet) as stylefile:
            style+=stylefile.read()

    if md:
        step("Formating markdown input...")
        import markdown
        text = md # TODO: Format plain text
        html = htmltemplate.format(
            style = style,
            body = markdown.markdown(md, output_format='html')
            )

    if ansi:
        step("Formating ansi input...")
        import deansi
        text = ansi # TODO: Clean ansi sequences
        html = htmltemplate.format(
            style = deansi.styleSheet()+style,
            body = "<div class='ansi_terminal'>"+deansi.deansi(ansi)+"</div>",
            )

    content = MIMEMultipart('alternative')

    if text:
        content.attach(MIMEText(text,'plain','utf8'))

    if html:
        step("Adapting html to mail clients...")
        import premailer
        html = premailer.transform(html)
        content.attach(MIMEText(html,'html','utf8'))

        import sys
        #sys.stdout.write(html)

    msg.attach(content)

    if dump:
        with open(dump,'w') as dumpfile:
            dumpfile.write(msg.as_string())
        success("Email dumped as {}".format(dump))
        return
    return
    # Sending
    step("Connecting to {host}:{port} as {user}...".format(**smtp))
    server = smtplib.SMTP(smtp['host'], smtp['port'])
    server.starttls()
    server.login(smtp['user'], smtp['password'])
    step("\tSending...")
    server.sendmail(sender, recipients, msg.as_string())
    success("\tMail sent")
    server.quit()



def parseArgs():
    import argparse
    parser = argparse.ArgumentParser(
        description="Sends an email.",
        )
    parser.add_argument(
        '-f',
        '--from',
        required=True,
        dest='sender',
        help="Message sender ('From:' header)",
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

    parser.add_argument(
        '--body',
        metavar="TEXT",
        help="Message body (defaults to stdin)",
        )

    parser.add_argument(
        '--bodyfile',
        metavar="BODYFILE",
        help="File containing the message body (defaults to stdin)",
        )
    parser.add_argument(
        '-C',
        '--config',
        dest='config',
        metavar="CONFIG.PY",
        help="Python Module with smtp configuration defined."
        )
    parser.add_argument(
        '-c',
        '--cc',
        dest='cc',
        action='append',
        help="Message copy recipient ('CC:' header) (multiple)",
        )

    parser.add_argument(
        '-b',
        '--bcc',
        dest='bcc',
        action='append',
        help="Message hidden copy recipient ('BCC:' header) (multiple), other recipients won't see this header",
        )

    parser.add_argument(
        '-r',
        '--replyto',
        dest='replyto',
        action='append',
        help="Default address to reply at ('Reply-To:' header) (multiple)",
        )

    parser.add_argument(
        '--format',
        choices = "html md text ansi".split(),
        default = 'text',
        metavar='FORMAT',
        help="Format for the body. "
            "'md' takes markdown and generates both html and text. "
            "'ansi' does the same, turning ANSI color codes in html or stripping them for text."
            ,
        )

    parser.add_argument(
        '--style',
        metavar='CSSFILE',
        action='append',
        help="Style sheet for the html output, (multiple)",
        )

    parser.add_argument(
        '--template',
        help="Alternative template for the html body.",
        )

    parser.add_argument(
        dest='attachments',
        metavar="FILE",
        nargs='*',
        help="File to attach",
        )

    parser.add_argument(
        '--dump',
        metavar='OUTPUTFILE.eml',
        help="Instead of sending, dump the email into a file",
        )
    args = parser.parse_args()
    return args


def main():
    import sys

    args = parseArgs()

    if args.body is not None:
        content = _unicode(args.body)
    elif args.bodyfile is not None:
        step("Loading body from stdin...")
        with open(args.bodyfile) as f:
            content = _unicode(f.read())
    else:
        content = _unicode(sys.stdin.read())

    #sys.stdout.write(content)

    sendMail(
        sender = args.sender,
        to = args.to,
        subject = args.subject,
        cc = args.cc,
        bcc = args.bcc,
        replyto = args.replyto,
        config = args.config,
        attachments = args.attachments,
        template = args.template,
        stylesheets = args.style,
        dumpfile = args.dump,
        **{args.format: content}
        )


if __name__ == '__main__':
    main()

# vim: et ts=4 sw=4
