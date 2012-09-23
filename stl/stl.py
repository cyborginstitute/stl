#!/usr/bin/python

import argparse 
import sauron
import subprocess
import os.path

def cmd_line_interface():
    from sauron import emacs_daemons as emacs_daemons
    parser = argparse.ArgumentParser(description='Create a Notification')

    if emacs_daemons is not []: 
        parser.add_argument('--target', '-t', default=emacs_daemons[0],
                            choices=emacs_daemons,
                            help='Target emacs instance.')
    parser.add_argument('--project', '-p', help='Project name.')
    parser.add_argument('--directory', '-d', help='Project directory.')
    parser.add_argument('--extension', '-e', help='File extension. Default is .txt', default='txt')
    parser.add_argument('--quiet', '-q', help='Project name.', action='store_true', default=False)
    parser.add_argument('--force', '-f', help='Run even if cached values are current.', action='store_true', default=False)

    return parser.parse_args()

def shell_word_count(directory, extension='txt'):

    command = 'wc -w `find ' + directory + ' -readable -name "*.' + extension + '"` | grep " total" | sed -e "s/^ //" -e "s/ total//"'

    p = subprocess.Popen( command, 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE, 
                          shell=True )
    output = p.communicate()

    return output[0].decode().rstrip()

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

    if os.path.isfile('/tmp/stl/' + project) is False:
        cachefile = open('/tmp/stl/' + project, 'w')
        cachefile.write(word_count)
        cachefile.close()
        return wc_message(word_count, project)
    else: 
        cache = open('/tmp/stl/' + project, 'r')
        # print(project + ' cached: ' + cache.readline())
        if word_count == cache.readline():
            if force is True:
                return wc_message(word_count, project) 
            else: 
                return None
        else: 
            cachefile = open('/tmp/stl/' + project, 'w')
            cachefile.write(word_count)
            cachefile.close()
            return wc_message(word_count, project) 

def wc_message(word_count, project):
    output = project + ': ' + word_count + " words"        

    return output

def generate_events(project, directory, target, quiet=False, log=None, emacs=True, force=False, extension=None):
    if extension is None: 
        event_message = wc_message_builder(project, directory, force)
    else: 
        event_message = wc_message_builder(project, directory, force, extension)

    import datetime 
    ts = datetime.datetime.now().strftime('[%m-%d %H:%M] ')

    if event_message is None:
        pass 
    else:
        if emacs is True: 
            test = sauron.NotificationMessage(source="stl", 
                                              message=event_message, 
                                              target=target)
            test.send()
        if log is not None: 
            logfile = open(log, 'a')
            logfile.write(ts + event_message + '\n')
            logfile.close()
            
        if quiet is False:
            print(ts + event_message)

def main():
    input = cmd_line_interface()

    if input.directory is None: 
        print("Error: specify a directory")
        exit(1)

    generate_events( input.project, 
                     input.directory, 
                     input.target, 
                     quiet=input.quiet, 
                     extension=input.extension )


if __name__ == "__main__":
    main()
