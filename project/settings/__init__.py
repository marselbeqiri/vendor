import os

if os.environ.get("ENV_NAME") == 'production':
    from .production import *
elif os.environ.get("ENV_NAME") == 'staging':
    from .staging import *
elif os.environ.get("ENV_NAME") == 'development':
    from .development import *
else:
    from .local import *
