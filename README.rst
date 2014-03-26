Repocopy webhook
====================

Webhook to forward commit pushes to another git repository

Getting started
----------------

.. code-block :: bash

    $ git clone git@github.com:qdqmedia/repocopy-webhook.git
    $ cd repocopy-webhook
    $ ./webhook.py -p 8005 --repo-from git@yourgitserver:john/test-webhook.git --repo-to git@yourgitserver:john/synced-repo.git
