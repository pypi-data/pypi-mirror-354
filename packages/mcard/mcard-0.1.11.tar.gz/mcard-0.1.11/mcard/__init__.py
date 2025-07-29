# MCard package initialization
__version__ = "0.1.11"

import os
from .config.logging_config import setup_logging, get_logger
from .model.card import MCard
from .model.card_collection import CardCollection
from .engine.sqlite_engine import SQLiteConnection, SQLiteEngine
from .config.env_parameters import EnvParameters
from .mcard_utility import MCardUtility

# No optional engines currently available

# Initialize logging
setup_logging()
logger = get_logger('init')
logger.debug('Logging initialized in __init__.py')

# Define the most commonly used classes in __all__
__all__ = [
    'MCard',
    'CardCollection',
    'SQLiteConnection',
    'SQLiteEngine',
    'EnvParameters',
    'MCardUtility',
    'setup_logging',
    'get_logger'
]

# No optional engines to add to __all__

# Get engine type from environment variable or use 'sqlite' as default
engine_type = os.environ.get('MCARD_ENGINE_TYPE', 'sqlite')
logger.info(f"Using {engine_type} as the default engine type")


# Create a default utility instance for quick access
default_utility = MCardUtility(engine_type=engine_type)

# Log creation
logger.debug(f"Created default utility with engine type: {engine_type}")
