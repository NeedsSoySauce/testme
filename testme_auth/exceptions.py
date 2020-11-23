from rest_framework.exceptions import APIException


class UsernameUnavailableException(APIException):
    status_code = 200
    default_detail = 'This username is unavailable.'
    default_code = 'username_unavailable'


class EmailInUseException(APIException):
    status_code = 200
    default_detail = 'This email is already linked to another account.'
    default_code = 'email_in_use'
