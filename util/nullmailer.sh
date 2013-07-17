#!/bin/bash

# Starts a local smtp daemon that prints mails to stdout,
# in order to test the mail setup in development

python -m smtpd -n -c DebuggingServer localhost:${1:-4000}
