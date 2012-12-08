#!/usr/bin/python

import datetime
import argparse
import socket
import subprocess
import os

# setting defaults:
personal_emacs_daemons = []
work_emacs_daemons = []

# Implementation:
emacs_daemons = personal_emacs_daemons + work_emacs_daemons

def cli():
    parser = argparse.ArgumentParser(description='Create a Notification')

    if emacs_daemons is not []:
        parser.add_argument('--target', '-t', default=emacs_daemons[0],
                            choices=emacs_daemons,
                            help='Target emacs instance.')

    parser.add_argument('--priority', '-p', default="3",
                        help='Set the priority for the notification.')
    parser.add_argument('--source', '-s', default=socket.gethostname(),
                        help='Set the source for the notification.')
    parser.add_argument('--message', '-m', default='default message', nargs='*',
                        help='Notifaction text.')

    return parser.parse_args()

def parse_message(message):
    if type(message) in (str, 'unicode'):
        parsed_message = message
    else:
        parsed_message = ''
        for word in message:
            parsed_message += str(word) + ' '
            parsed_message = parsed_message[:-1]

    return parsed_message

class NotificationMessage(object):
    def __init__(self, source=socket.gethostname(), target=emacs_daemons[0], priority=3, message=None):
        self.target = target
        self.priority = priority
        self.source = source
        self.message = message

    def send(self):
        if emacs_daemons is []:
            command = ['emacsclient', '-e', '(sauron-add-event \'' + self.source +
                       ' ' +  str(self.priority) + ' "' + parsed_message(self.message) + '")']
        else:
            command = ['emacsclient', '--server-file=' + self.target,
                       '-e', '(sauron-add-event \'' + self.source  +  ' ' +
                       str(self.priority) + ' "' + parse_message(self.message) + '")']

        with open(os.devnull, "w") as fnull:
            subprocess.call( command, stdout=fnull, stderr=fnull )

    def log(self):
        ts = datetime.datetime.now().strftime('[%m-%d %H:%M] ')

        if self.target in work_emacs_daemons:
            try:
                from wc_track import work_log
            except ImportError:
                print('Log file not specified. Message "' + self.message + '" not logged.')
            else:
                with open(work_log, 'a') as f:
                    f.write(ts + self.message + '\n')
        elif self.target in personal_emacs_daemons:
            try:
                from wc_track import personal_log
            except ImportError:
                print('Log file not specified. Message "' + self.message + '" not logged.')
            else:
                with open(personal_log, 'a') as f:
                    f.write(ts + self.message + '\n')
        else:
            print('No log file specified. Message: "' + self.message + '"')

def main():
    i = cli()

    message = NotificationMessage(source=i.source,
                                  target=i.target,
                                  priority=i.priority,
                                  message=i.message)
    message.send()

if __name__ == "__main__":
    main()
