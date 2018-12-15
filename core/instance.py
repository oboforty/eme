from core.ctx import dbctx

from core.caches import ServerRepository, FileRepository, ServerStore

# Static config

# Redis entities

# Repositories
from core.services import settings

files = FileRepository(dbctx)

if settings.get('servers.store_method') == 'db':
    servers = ServerRepository(dbctx)
else:
    servers = ServerStore()
