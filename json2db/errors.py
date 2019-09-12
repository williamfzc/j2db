import typing

from json2db.server import JsonRequest


def json_invalid_error(origin_request: JsonRequest) -> typing.Dict[str, typing.Union[str, JsonRequest]]:
    return {
        'error': 'json_invalid',
        'msg': 'content in your request is not a valid json format',
        'request': origin_request,
    }


JsonInvalidError = json_invalid_error
