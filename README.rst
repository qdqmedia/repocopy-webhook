Repocopy webhook
====================

Webhook to forward commit pushes to another git repository

.. image :: https://raw.github.com/qdqmedia/repocopy-webhook/master/assets/diagram.png

Getting started
----------------

.. code-block :: bash

    $ git clone git@github.com:qdqmedia/repocopy-webhook.git
    $ cd repocopy-webhook
    $ ./webhook.py --repo-from git@server1:project.git --repo-to git@server2:project.git
    March 26 16:52:08 webhook.py INFO Starting webhook server (repocopy) on port 8000...

Command line options
--------------------

======================== ======================================================================== ========
Argument                 Description                                                              Required
======================== ======================================================================== ========
``--repo-from``          GIT Repository URL to copy from                                          Yes
``--repo-to``            GIT Repository URL to copy to                                            Yes
``-p, --port``           Server port (8000 by default)                                            No
``-l, --log``            Path to log file (otherwise stdout will be used)                         No
``--log-level``          Logging level (INFO by default)                                          No
``--log-max-size``       Log max size (52428800 bytes by default)                                 No
``--log-backup-count``   Number of historical data logs (4 by default)                            No
``--tmp-dir-root``       Path where temporary repository will be created                          No
======================== ======================================================================== ========

