from urllib.parse import parse_qs

from channels.auth import BaseMiddleware, AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from jwt import decode

from authorize.models import User
from market import settings


class JWTAuthMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            token = parse_qs(scope["query_string"].decode("utf8")).get('token', None)[0]
            data = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            scope['user'] = await self.get_user(data['user_id'])
        except Exception as exp:
            scope['user'] = AnonymousUser()
        return await self.inner(scope, receive, send)


    @database_sync_to_async
    def get_user(self, user_id):
        """Return the user based on user id."""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()


def JWTAuthMiddlewareStack(app):
    """This function wrap channels authentication stack with JWTAuthMiddleware."""
    return JWTAuthMiddleware(AuthMiddlewareStack(app))


