import logging
import time

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status

from .settings import block_ips
from .utility import send_response_to_websocket

logger = logging.getLogger('django')


class SendResponseToWebsocketUserMiddleware(MiddlewareMixin):

    def __call__(self, request, *args, **kwargs):
        start_time = time.time()
        response = self.get_response(request)

        send_response_to_websocket(response, request)

        end_time = time.time()
        duration = end_time - start_time

        logger.info(
            f"Request: {request.method} {request.path} | "
            f"Status: {response.status_code} | "
            f"Duration: {duration:.2f}s"
        )
        return response


class LogIpMiddleware(MiddlewareMixin):

    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip in block_ips:
            return HttpResponse("Access denied.", status=status.HTTP_403_FORBIDDEN)

        return None

