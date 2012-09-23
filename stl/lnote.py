#!/usr/bin/python

import sauron
import argparse
import wc_track
import socket

def cmd_line_interface():
    parser = argparse.ArgumentParser(description='Create a log message.')
    
    if sauron.emacs_daemons is not []: 
        parser.add_argument('--target', '-t', default=sauron.emacs_daemons[0],
                            choices=sauron.emacs_daemons,
                            help='Target emacs instance.')

    parser.add_argument('--message', '-m', default='default message', nargs='*',
                        help='Default.')
    
    return parser.parse_args()

def send_message(note, target):
    import datetime 
    ts = datetime.datetime.now().strftime('[%m-%d %H:%M] ')
    pnote = note[0]

    message = sauron.NotificationMessage(source='note', message=pnote, target=target)
    message.send()

    if target == 'work':
        logfile = open('/home/' + username + '/work/stats-' + socket.gethostname() + '.log', 'a')
    elif target in ('hud', 'tychoish'):
        logfile = open('/home/' + username + '/tychoish/projects/stats-' + socket.gethostname() + '.log', 'a')

    logfile.write(ts + pnote + '\n')
    logfile.close()

def main():
    input = cmd_line_interface()
    send_message(input.message, input.target)

if __name__ == "__main__":
    main()
