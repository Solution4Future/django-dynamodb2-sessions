from boto.dynamodb.exceptions import DynamoDBKeyNotFoundError
from boto.dynamodb2.table import Table
from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError
from django.core.exceptions import SuspiciousOperation
import logging
import time
from boto.regioninfo import RegionInfo
from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2 import connect_to_region

logger = logging.getLogger(__name__)



def dynamodb2_connection_factory():
    from django.conf import settings
    if getattr(settings,'AWS_ACCESS_KEY_ID', '') and getattr(settings,'AWS_SECRET_ACCESS_KEY', ''):
        logger.info("Creating a DynamoDB connection.")
        connection_data = {
                           'region_name': settings.AWS_REGION_NAME,
                           'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
                           'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
                           }
        conn = connect_to_region(**connection_data)
        setattr(settings, 'DYNAMODB_CONNECTION', conn)
    else:
        logger.error("Settings is not configured properly, missing AWS access data")
        
class SessionStore(SessionBase):
    """
    Implements DynamoDB session store.
    """
    
    def __init__(self, session_key=None):
        """
        Connect to sessions table in DynamoDB 
        """
        super(SessionStore, self).__init__(session_key)
        dynamodb2_connection_factory()        
        if getattr(settings,'DYNAMODB_SESSIONS_TABLE_NAME'):
            self.table = Table(table_name = settings.DYNAMODB_SESSIONS_TABLE_NAME,
                                       connection = getattr(settings, 'DYNAMODB_CONNECTION', None))
            logger.info("Initialization of SessionStore.")
        else:
            logger.info("No Session table name for DynamoDB")

    def load(self):
        """
        Get session data from DynamoDB, runs it through the session
        data de-coder (base64->dict), sets ``self.session``.

        :rtype: dict
        :returns: The de-coded session data, as a dict.
        """
        #TODO: ugly
#         import ipdb; ipdb.set_trace()
        item = self.table.get_item(session_key = self.session_key, 
                                   consistent = getattr(settings, 'DYNAMODB_SESSIONS_ALWAYS_CONSISTENT', False))
        if item.items():
            try:
                logger.info("Item got successfully")
                return self.decode(item['data'])
            except SuspiciousOperation:
                self.create()
                return {}
        self.create()
        return {}

    def exists(self, session_key):
        """
        Checks to see if a session currently exists in DynamoDB.

        :rtype: bool
        :returns: ``True`` if a session with the given key exists in the DB,
            ``False`` if not.
        """
        if self.table.get_item(session_key = session_key, consistent = getattr(settings, 'DYNAMODB_SESSIONS_ALWAYS_CONSISTENT', False)).items():
            logger.info("Item exists")
            return True
        else:
            logger.info("Item doesn't exist")
            return False
        
    def create(self):
        """
        Creates a new entry in DynamoDB. This may or may not actually
        have anything in it.
        """
        while True:
            try:
                self.save(must_create=True)
            except CreateError:
                continue
            self.modified = True
            self._session_cache = {}
            return

    def save(self, must_create=False):
        """
        Saves the current session data to the database.

        :keyword bool must_create: If ``True``, a ``CreateError`` exception will
            be  raised if the saving operation doesn't create a *new* entry
            (as opposed to possibly updating an existing entry).
        :raises: ``CreateError`` if ``must_create`` is ``True`` and a session
            with the current session key already exists.
        """
        if must_create:
            self._session_key = None
        
        self._get_or_create_session_key()
        data = {'session_key': self._session_key, 'data': self.encode(self._get_session(no_load=must_create))}
        if must_create:
            data['created'] = int(time.time())
            try:
                self.table.put_item(data=data)
                logger.info("Item created successfully")
            except CreateError:
                logger.info("Item creation failed")
        else:
            item = self.table.get_item(session_key = self._session_key, 
                                       consistent = getattr(settings, 'DYNAMODB_SESSIONS_ALWAYS_CONSISTENT', False))
            if not item.items():
                item['session_key'] = data['session_key']
            item['data'] = data['data'] 
            item.save()
                
            
            
    def delete(self, session_key=None):
        """
        Deletes the current session, or the one specified in ``session_key``.

        :keyword str session_key: Optionally, override the session key
            to delete.
        """
        
        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key
        item = self.table.get_item(session_key = session_key, 
                                       consistent = getattr(settings, 'DYNAMODB_SESSIONS_ALWAYS_CONSISTENT', False))
        if item.items():
            item.delete()