#!/usr/bin/python

import stl 
import socket
import os.path
import argparse 

projects = {
  'stl' : { 
        'path' : '/home/' + username + '/projects/stl/docs/source/',
        'target' : 'tychoish',
        'emacs' : True,
        'quiet' : False, 
        'log' : '/home/' + username + '/projects/stats-' + socket.gethostname() + '.log',
        'ext': 'txt'
    },
  'meta-driver' : {
        'path' : '/home/' + username + '/work/meta-driver/docs/source', 
        'target' : 'work',
        'emacs' : True,
        'quiet' : False,
        'log' : '/home/' + username + '/work/stats-' + socket.gethostname() + '.log',
        'ext': 'txt'
    },
}

def main():
    parser = argparse.ArgumentParser(description='Batch word count notifaction')
    parser.add_argument('--force', '-f', help='Run even if cached values are current.', action='store_true', default=False)
    parser.add_argument('--project', help='Specify project to report on. Otherwise, report on all projects.', default=None, choices=projects.keys() )
    
    input = parser.parse_args()

    if input.project is None:
        for project in projects.items():
            stl.generate_events( project[0], project[1]['path'], 
                                 project[1]['target'], quiet=project[1]['quiet'],
                                 log=project[1]['log'], emacs=project[1]['emacs'], 
                                 force=input.force, extension=project[1]['ext'] )
    else:
        stl.generate_events( input.project, projects[input.project]['path'], 
                             projects[input.project]['target'], quiet=projects[input.project]['quiet'],
                             log=projects[input.project]['log'], emacs=projects[input.project]['emacs'], 
                             force=input.force, extension=projects[input.project]['ext'] )

if __name__ == "__main__":
    main()
