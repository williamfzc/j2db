import typing

from json2db.request import JsonRequest


def json_invalid_error(
    origin_request: typing.Union[JsonRequest, typing.Dict[str, str]]
) -> typing.Dict[str, typing.Union[str, JsonRequest]]:
    return {
        "error": "json_invalid",
        "msg": "content in your request is not a valid json format",
        "request": origin_request,
    }


JsonInvalidError = json_invalid_error
