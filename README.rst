django-dynamodb2-sessions
=========================

:Info: Sessions backend dedicated for Django uses Amazon `DynamoDB`_ v.2 for data storage.
:Author: Justine Żarna

If You need backend uses Amazon DynamoDB v. 1 see `Greg Taylor github`_

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

Install django-dynamodb2-sessions using ``pip``::

    pip install django-dynamodb2-sessions

Export your AWS key and secret key as environment variables because of security::

   export AWS_ACCESS_KEY_ID='YourKey'
   export AWS_SECRET_ACCESS_KEY='YourSecretKey'
   export AWS_REGION_NAME = 'YourRegion'

In your ``settings.py`` file, you'll need set variables::
     
    import os
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '') # set Your AWS key
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '') # set Your AWS secret key
    AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME', '') # set Your AWS region
    
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

0.2
^^^

* Added removing expired sessions command management.

0.3
^^^

* Added new version of boto to requirements

License
-------

django-dynamodb2-sessions is licensed under the BSD License.
