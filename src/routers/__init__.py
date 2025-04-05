from .admin_router import admin_router
from .users_router import user_router
routers=[admin_router, user_router]
__all__= ["routers"]