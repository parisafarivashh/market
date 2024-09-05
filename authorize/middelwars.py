from django.utils.deprecation import MiddlewareMixin

from authorize.exceptions import BlockUserException


class NotAllowedBlockUser(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated is True and \
                request.user.is_blocked is True:
            raise BlockUserException()

