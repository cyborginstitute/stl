=============================
Personal Status Logger README
=============================

See full `documentation and project site <http://cyborginstitute.com/projects/stl>`_
for more explanation of the use and operation of ``stl``. This
repository contains the full code and documentation. Notable
components:

- The ``stl`` script, written in ``zsh``, at "``bin/stl``"

- The ``xmpp-notify`` script, for sending notification messages using
  a "bot" account. ``xmpp-notify`` operates like a remote ``echo``.

- The source for the documentation is in the ``docs/`` directory. If
  install `Sphinx <http://sphinx.pocoo.org/>` and run "``make
  install``" to build the documentation

- The ``configure`` script in the top level of the repository
  provides a rudimentary configuration interface for ``xmpp-notify``.

I'm thinking about rewriting ``stl`` in something a bit more efficient
and robust, and as a learning exercise. If I chose to do that it will
appear in the ``dev/`` directory.

Feel free to send patches/pull requests/branch notifications if you do
something cool with this and want me merge, and I probably will.

-- `tychoish <http://tychoish.com>`_

(``stl`` is a `Cyborg Institute <http://cyborginstitute.com/>`_
project/thing.)
