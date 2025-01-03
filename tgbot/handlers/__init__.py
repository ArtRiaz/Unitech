"""Import all routers and add them to routers_list."""
from .admin import admin_router
from .user import user_router
from .about import about_router
from .contacts import contacts_router
from .register import register_router
from .catalog import catalog_router
from .count import count_router

routers_list = [
    admin_router,
    user_router,
    about_router,
    contacts_router,
    register_router,
    catalog_router,
    count_router,
]

__all__ = [
    "routers_list",
]
