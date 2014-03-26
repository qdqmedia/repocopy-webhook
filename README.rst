Repocopy webhook
====================

Webhook to forward commit pushes to another git repository

Getting started
----------------

.. code-block :: bash

    $ git clone git@github.com:qdqmedia/repocopy-webhook.git
    $ cd repocopy-webhook
    $ ./webhook.py --repo-from git@oldserver:project.git --repo-to git@newserver:project.git


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

