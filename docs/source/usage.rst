===================
``stl`` Manual Page
===================

EDIT file

Synopsis
--------

This document provides an overview of ``stl`` from the perspective of
the user concerning both the `script itself <#TODO>`_ as it exists in
"stock" format, and how many will choose to customize the script. See
":doc:`internals`" for more information on the underlying functions,
operation, and code paths of the script.

.. _stl-usage:

Basic Usage
-----------

This section describes the invocation and purpose of various ``stl``
commands, ignoring most of the internals of the script.

.. note::

   While you may want to set up interfaces for calling ``stl``
   directly, in most cases ``stl`` will run fairly regularly as a cron
   job.

``stl`` commands take the following basic form: ::

     stl [domain] [worker] [project] [options]

- "``[domain]`` - You may ommit this layer in some cases, but is
  useful if you need to maintain two separate log files, with two
  separate sets of projects.

  If this term does not match one of the defined commands, then the
  program exits with help text.

- "``[worker]``" - In the default implementation this is either
  "``make``", "``stats``", ``report``", or "``output``" and defines
  the major fork in the behavior of the program. "``make``" will build
  a project, while "``stats``" provides access to word count and
  latest build times, "``report``" displays the output of the
  last build, while "``output``" is responsible for modifying the
  default output style.

  The default worker option is "``stats``".

- "``[project]``" - A key word that defines each project. This option
  is required for successful output. The ``make`` worker only accepts
  one argument, while ``stats`` can handle multiple ``projects``, in
  some cases.

- "``[options]``" - Some workers, accept additional arguments or
  messages.

  Workers in the ``stats`` group:

  - ``build-report``, which displays the contents of the output of the
    most recent build process.

  Workers in the ``entry`` group, which makes it possible to record an
  arbitrary message to the log accept "``start``", "``stop``", and
  "``note``", followed by the contents of the message.

  Workers in the ``make`` group:

  - ``spinx-builder``, which orchestrates the build process for Sphinx
    projects takes an argument which mirrors the arguments to the
    default Sphinx Makefile.

    *No special or additional arguments for this builder*.

  - ``ikiwiki-builder`` which commits and builds Ikiwiki wikis, takes
    as an argument the commit message. for the git commit.

    *No special or additional arguments for this builder*.

  Workers in the ``report`` group accept an output format or
  interface, including:

  - ``less`` opens the build report file using the :command:`less` command.

  - ``more`` opens the build report file using the :command:`more` command.

  - ``cat``  outputs the build report file using :command:`cat`.

  - ``emacs-new`` opens the log file in a new graphical :command:`emacsclient`
    window.

  - ``emacs`` opens the log file in an existing :command:`emacsclient`
    instance.

  - ``emacs-term`` opens the log file in a  terminal :command:`instance`
    emacsclient.

  - ``term`` opens the build report in a new terminal window
    (i.e. :command:`urxvtcd`) using the :command:`less` command.

.. _stl-customization:

Customizing ``stl``
-------------------

The example ``stl`` included here is reasonably generic, but all users
will need to customize the code at least a little to be able to use
it. All user customizable code resides at the bottom of the
file. Continue for more detail on these customizations.

At the very end of the file the following "``main``" function, which
is the user's entry into the code. It looks like:

.. code-block:: sh

   main(){
      ARG=($@)

      case $ARG[2] in
          ( make ) ACTION=make ;;
          ( stat* ) ACTION=stats ;;
          ( entry* ) ACTION=entry ;;
          ( report ) ACTION=report ;;
          ( * ) ACTION=stats ;;
      esac

      domain=$ARG[1]
      ARG[1]=()

      case $domain in
         ( tycho ) tycho-worker $ARG; exit 0 ;;
         ( job ) job-worker $ARG; exit 0 ;;
         ( * ) echo "help text"; exit 1 ;;
      esac
   }
   main $@

The first ``case`` statement sets a variable that the
``action-handler`` function uses. The second ``case`` statement
selects the ``domain``.

If you modify the first statement, add corresponding code to the
``action-handler`` function. ``action-handler`` calls the function s
that *does something* (i.e. "actions"_, so you'll probably want to add
one of those functions as well. The second case statement simply
passes arguments to the next user customizeable function, which is the
"domain-selector."

In the first case, it's important to set a good default
(i.e. ``stats``) as most invocations of the program will be
"``stats``" operations. The worst thing that can happen is the command
will be invalid and there will be no output. In the second it's
important to produce an error, because without a domain there's no way
to proceed.

See "``tycho-selector``", which is an example "domain-selector" function:

.. code-block:: sh

   tycho-selector(){
       PROJECT=projects
       LOG_TAG=tycho

       for argument in $ARG; do
           case "$argument" in
               ( ae ) queue=($queue al-edarian); shift ;;
               ( mars ) queue=($queue knowing-mars); shift ;;
               ( admin ) queue=($queue cyborg-admin); shift ;;
               ( gmg|mg ) queue=($queue mediagoblin);
                       WC_PATH=~/projects/mediagoblin/docs/source
                       shift ;;
               ( rhizome ) queue=($queue rhizome); shift
                           PROJECT_PATH=~/assemblage/rhizome/
                           WC_PATH=$PROJECT_PATH
                           BUILD_TYPE=wiki; EXTENSION=mdwn
               ;;
               ( assemblage|ass ) queue=($queue assemblage); shift
                                  PROJECT_PATH=~/assemblage/
                                  WC_PATH=$PROJECT_PATH
                                  BUILD_TYPE=wiki; EXTENSION=mdwn
               ;;
               ( wikish|wiki )   queue=($queue wikish); shift
                                 PROJECT_PATH=~/wikish/
                                 WC_PATH=$PROJECT_PATH
                                 BUILD_TYPE=wiki; EXTENSION=mdwn
               ;;
               ( * ) # continue silently ;;
           esac
       done

       action-handler $@;
   }

The "domain-selector" functions just set variables that describe the
sub-projects in the domain that the "actions" use. The main reason
to have separate projects is to be able to log statistics into
separate files.

There are two constants set at the beginning of the "domain-selector."
Consider them and their purpose:

- ``$PROJECT`` describes the domain and unless overridden the
  directory in which all sub-projects reside.

- ``$LOG_TAG`` describes the string that prefixes log items when
  sending the log via XMPP.

The initial version of the script assumed each "domain" would refer to
a group of projects that were sub-directories of a single "domain"
folder. This is why the "``ae``", "``mars``", and "``admin``" projects
only set the ``$queue`` variable. However, it's not practical to force
projects into such a rigid hierarchy, and as a result, these defaults
can be overridden, which is what happens in the other sub-projects.

The key variables here are:

- ``$queue`` is an array that holds lists of sub-projects. For many
  workers, as long as you don't mix Sphinx and Ikiwiki builds, you can
  specify multiple projects and, and ``stl`` will report or act on all
  of them.

  While script uses this basic "queue" structure in a number of
  places, given the way that the shell (and I) have set up the
  variables, means that this functionality is not as robust as it
  ought to be. In the interests of reliability over correctness, the
  script should always "*do the right thing*" if you only specify one
  project in an invocation.

- ``$WC_PATH`` is the location of the source files. By default, the
  script will look for source files in "``$PROJECT/source/$queue.item``"
  (where ``$queue.item`` is an element in the ``$queue`` array.) Set
  ``WC_PATH`` to override this.

- ``$PROJECT_PATH`` is the path of the project files. Unless set this
  defaults to "``~/project``".

- ``$BUILD_TYPE`` specifies which "build method" to use. Current
  options are ``wiki`` for Ikiwiki instances (stored using git), and
  ``sphinx``. The default is ``sphinx``.

- ``$EXTENSION`` specifies the file extension of the files. Defaults
  to ``rst``. Used to ensure that the word counts do not include
  extraneous files.

Set any or all of these variables in each case statement. You may now
begin using ``stl`` to track your tasks. 
