#!/usr/bin/python

import datetime
import argparse
import socket
import subprocess
import os.path

import sauron
from sauron import emacs_daemons

def shell_word_count(directory, extension='txt'):
    command = ('wc -w `find ' + directory + ' -readable -name "*.' + extension +
               '"` | grep " total" | sed -e "s/^ //" -e "s/ total//"')

    p = subprocess.Popen( command,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          shell=True )

    output = p.communicate()

    return output[0].decode().rstrip()

def wc_message(word_count, project):
    return project + ': ' + word_count + " words"

def wc_message_builder(project, directory, force=None, extension=None):
    if extension is None:
        word_count = str(shell_word_count(directory))
    else:
        word_count = str(shell_word_count(directory, extension))

    if force is None:
        input = cmd_line_interface()
        force = input.force

    if os.path.isdir('/tmp/stl') is False:
        os.mkdir('/tmp/stl')
        ndir = sauron.NotificationMessage(source='stl', message=socket.gethostname() + ' rebooted')
        ndir.send()
        ndir.log()

    if os.path.isfile('/tmp/stl/' + project) is False:
        with open('/tmp/stl/' + project, 'w') as f:
            f.write(word_count)

        return wc_message(word_count, project)
    else:
        cache = open('/tmp/stl/' + project, 'r')
        # print(project + ' cached: ' + cache.readline())
        if word_count == cache.readline():
            if force is True:
                return wc_message(word_count, project)
            else:
                return None
            cache.close()
        else:
            with open('/tmp/stl/' + project, 'w') as f:
                f.write(word_count)
            cache.close()
            return wc_message(word_count, project)


def generate_events(project, directory, target, quiet=False, log=False, emacs=True, force=False, extension=None):
    if extension is None:
        event_message = wc_message_builder(project, directory, force)
    else:
        event_message = wc_message_builder(project, directory, force, extension)

    ts = datetime.datetime.now().strftime('[%m-%d %H:%M] ')

    if event_message is None:
        pass
    else:
        test = sauron.NotificationMessage(source="stl",
                                          message=event_message,
                                          target=target)
        if emacs is True:
            test.send()
        if log is not False:
            test.log()
        if quiet is False:
            print(ts + event_message)

def cli():
    parser = argparse.ArgumentParser(description='Create a Notification')

    if emacs_daemons is not []:
        parser.add_argument('--target', '-t', default=emacs_daemons[0],
                            choices=emacs_daemons,
                            help='Target emacs instance.')
    parser.add_argument('--project', '-p', help='Project name.')
    parser.add_argument('--directory', '-d', help='Project directory.')
    parser.add_argument('--extension', '-e', help='File extension. Default is .txt', default='txt')
    parser.add_argument('--quiet', '-q', help='Silence most output.', action='store_true', default=False)
    parser.add_argument('--force', '-f', help='Run even if cached values are current.', action='store_true', default=False)
    parser.add_argument('--log', '-l', help='.', action='store_true', default=False)

    return parser.parse_args()

def main():
    input = cli()

    if input.directory is None:
        exit("Error: specify a directory")

    generate_events( input.project,
                     input.directory,
                     input.target,
                     quiet=input.quiet,
                     log=input.logfile,
                     extension=input.extension )

if __name__ == "__main__":
    main()
