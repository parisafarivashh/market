from collections import defaultdict

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the custom 'error' key in the response data.
    if response is not None and response.data:
        errors = defaultdict(list)
        for key, values in response.data.items():
            if isinstance(values, list):
                errors[key] = [str(value) for value in values]
            else:
                errors[key] = [str(values)]

        response.data = {'error': dict(errors)}

    return response
