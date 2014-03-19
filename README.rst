Python Base Webhook
====================

A simple start to create webhooks with Python

Getting started
----------------

.. code-block :: bash

    $ git clone git@github.com:dnmellen/python-base-webhook.git yourwebhook
    $ cd yourwebhook
    $ ./webhook.py -p 8000 -l /tmp/mywebhook.log


Example of output
-----------------

This was tested using Gitlab (https://www.gitlab.com/):

.. code-block :: bash

	$ ./webhook.py -p 8005
	March 19 17:33:43 webhook.py INFO Starting webhook server (untitled) on port 8005...
	{u'after': u'cf58c59f48f4dd5ed1d5b60cf5f6c862a807af86',
	 u'before': u'ae370610f0c46bfd8a110be37e0138e18b3bad6c',
	 u'commits': [{u'author': {u'email': u'john@yourdomain.com',
	                           u'name': u'John Smith'},
	               u'id': u'cf58c59f48f4dd5ed1d5b60cf5f6c862a807af86',
	               u'message': u'Another more line',
	               u'timestamp': u'2014-03-19T16:34:16+00:00',
	               u'url': u'http://yourgitserver.com/test-webhook/commit/cf58c59f48f4dd5ed1d5b60cf5f6c862a807af86'}],
	 u'project_id': 4,
	 u'ref': u'refs/heads/master',
	 u'repository': {u'description': u'',
	                 u'homepage': u'http://yourgitserver.com/john/test-webhook',
	                 u'name': u'test-webhook',
	                 u'url': u'git@yourgitserver.com:john/test-webhook.git'},
	 u'total_commits_count': 1,
	 u'user_id': 2,
	 u'user_name': u'John'}
	 ^CMarch 19 17:42:09 webhook.py INFO CTRL-C pressed, closing webhook...
