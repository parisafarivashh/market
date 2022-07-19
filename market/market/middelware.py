import jwt
from admins.models import Admin
from user.models import Token, User
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from market.settings import SECRET_KEY, SIMPLE_JWT


@database_sync_to_async
def get_user(token_key: str) -> any:
    try:
        user: User = Token.objects.get(key=token_key).user
        return user if user.is_authenticated is True else None
    except Token.DoesNotExist:
        try:
            user_id: int = jwt.decode(token_key, SECRET_KEY, algorithms=[SIMPLE_JWT['ALGORITHM']]).get(SIMPLE_JWT['USER_ID_CLAIM'])
        except jwt.exceptions.DecodeError:
            return None
        except jwt.exceptions.ExpiredSignatureError:
            return None
        try:
            return None if user_id is None else Admin.objects.get(id=user_id)
        except Admin.DoesNotExist:
            return None


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
        scope['user'] = None if token_key is None else await get_user(token_key)
        return await super().__call__(scope, receive, send)
