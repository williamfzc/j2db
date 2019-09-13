import typing

from json2db.request import JsonRequest


def json_invalid_error(
    origin_request: typing.Union[JsonRequest, typing.Dict[str, str]]
) -> typing.Dict[str, typing.Union[str, JsonRequest]]:
    return {
        "error": "json_invalid",
        "msg": "content in your request is not a valid json format",
        "request": origin_request,
        "stack": "",
    }


def tag_invalid_error(
    origin_request: typing.Union[JsonRequest, typing.Dict[str, str]]
) -> typing.Dict[str, typing.Union[str, JsonRequest]]:
    return {
        "error": "tag_invalid",
        "msg": "tag should match the table name",
        "request": origin_request,
        "stack": "",
    }


def db_operator_error(
    origin_request: typing.Union[JsonRequest, typing.Dict[str, str]], error: str
) -> typing.Dict[str, typing.Union[str, JsonRequest]]:
    return {
        "error": "db_operator",
        "msg": "operate failed",
        "request": origin_request,
        "stack": error,
    }


JsonInvalidError = json_invalid_error
TagInvalidError = tag_invalid_error
DBOperatorError = db_operator_error
