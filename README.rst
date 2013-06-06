django-dynamodb2-sessions
=========================

:Info: Sessions backend dedicated for Django uses Amazon `DynamoDB` v.2 for data storage.
:Author: Justine Żarna

If You need backend uses Amazon DynamoDB v. 1 see `Greg Taylor github`

.. _DynamoDB: http://aws.amazon.com/dynamodb/
.. _Greg Taylor github: https://github.com/gtaylor/django-dynamodb-sessions

First step: create DynamoDB Table
--------------------------

Visit your `DynamoDB tab`_ in the AWS Management Console and follow instructions:

* Choose the *Create Table* option.
* Enter your sessions table name (example: ``sessions``).
* Select Primary Key Type = ``Hash``.
* Select Hash Attribute Type as ``String``.
* Enter ``session_key`` for *Hash Attribute Name*.
* Choose the *Continue* option twice.
* Fill Provisioned Throughput Capacity (only for tests: ``read`` - 10 units, ``write`` - 5 units).
* Choose the *Continue* option.
* Choose the *Create* option.

.. _DynamoDB tab: https://console.aws.amazon.com/dynamodb/home

Second step: installation
-------------

Install django-dynamodb2-sessions using ``pip`` or ``easy_install``::

    pip install django-dynamodb2-sessions

In your ``settings.py`` file, you'll need set variables::

    AWS_ACCESS_KEY_ID = '' # set Your AWS key
    AWS_SECRET_ACCESS_KEY = '' # set Your AWS secret key
    AWS_REGION_NAME = '' # set Your AWS region
    DYNAMODB_SESSIONS_TABLE_NAME = '' # set Your sessions table name

Set your session backend to::

    SESSION_ENGINE = 'dynamodb_sessions.backends.cached_dynamodb'

or::

    SESSION_ENGINE = 'dynamodb_sessions.backends.dynamodb'
    
Optional you can set always consistent parametr.
If you are not using cache to this sessions backend you can force all reads from Dynamodb by setting True.
Default: False::

    DYNAMODB_SESSIONS_ALWAYS_CONSISTENT = False

Versions
-------

0.1
^^^

* Initial release.

License
-------

django-dynamodb2-sessions is licensed under the BSD License.
