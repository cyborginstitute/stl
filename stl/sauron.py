#!/usr/bin/python

import argparse
import socket
import subprocess
import os 

## setting defaults
emacs_daemons = ['tychoish', 'work', 'hud']

def cmd_line_interface():
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
    if type(message) is str or unicode:
        parsed_message = message
    else:
        parsed_message = ''
        for word in message: 
            parsed_message += str(word) + ' '
            parsed_message = parsed_message[:-1]

    return parsed_message

def notify_send(message):
    if emacs_daemons is []: 
        command = ['emacsclient', '-e', '(sauron-add-event \'' + message.source +  
                   ' ' +  str(message.priority) + ' "' + parsed_message(message.message) + '")']
    else:
        command = ['emacsclient', '--server-file=' + message.target,  
                   '-e', '(sauron-add-event \'' + message.source  +  ' ' + 
                   str(message.priority) + ' "' + parse_message(message.message) + '")']

    with open(os.devnull, "w") as fnull:
        subprocess.call( command, stdout=fnull, stderr=fnull )

class NotificationMessage(object):
    def __init__(self, source=socket.gethostname(), target=emacs_daemons[0], priority=3, message=None):
        self.target = target
        self.priority = priority
        self.source = source
        self.message = message

    def send(self):
        notify_send(self)

def main():
    message = cmd_line_interface()
    notify_send(message) 

if __name__ == "__main__":
    main()
