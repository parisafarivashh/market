from rest_framework.exceptions import APIException


class BlockUserException(APIException):
    status_code = 403
    default_code = '403'
    default_detail = {"code": 403, "message": "Forbidden request"}

