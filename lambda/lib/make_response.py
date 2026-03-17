import json


def make_response(status_code: int, payload: dict) -> dict:
    if payload.get("data") is not None:
        payload['data']['flags'] = 64

    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(payload)
    }
