
import importlib.metadata 
import logging
mediawiki_session_logger = logging.getLogger(__name__)

__version__ =  importlib.metadata.version('mediawiki_session') 
from mediawiki_session.wsession import MediaWikiSession


