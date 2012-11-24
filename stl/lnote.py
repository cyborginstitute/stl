#!/usr/bin/python

## core stl stuff
import sauron

## standard library stuff
import argparse
import datetime

def cli():
    parser = argparse.ArgumentParser(description='Create a log message.')

    if sauron.emacs_daemons is not []:
        parser.add_argument('--target', '-t', default=sauron.emacs_daemons[0],
                            choices=sauron.emacs_daemons,
                            help='Target emacs instance.')

    parser.add_argument('--message', '-m', default='default message', nargs='*',
                        help='Default.')

    return parser.parse_args()

def send_message(note, target):
    note = ' '.join(note)
    message = sauron.NotificationMessage(source='note', message=note, target=target)

    message.send()
    message.log()

def main():
    input = cli()
    send_message(input.message, input.target)

if __name__ == "__main__":
    main()
