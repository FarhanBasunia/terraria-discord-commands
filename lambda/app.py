import base64
import json
import logging
import os
import traceback

from lib.make_response import make_response
from lib.logger import Logger

logger = Logger(__name__)


def lambda_handler(event, context):
    status = False
    try:
        body_raw = event.get("body") or "{}"
        if event.get("isBase64Encoded"):
            body_raw = base64.b64decode(body_raw).decode("utf-8")

        body = json.loads(body_raw)

        logger.info(f"Event: {event}")
        if body.get("type") == 1:
            logger.debug("returning ping")
            status = True
            return make_response(200, {"type": 1})

        if body.get("type") == 2:
            status = True
            return make_response(200, {"type": 4, "data": {"content": "test_success"}})

        logger.info(f"Unknown interaction type: {body.get('type')}")
        # Respond with a PONG for any unrecognized payload to keep Discord happy.
        return make_response(200, {"type": 1})

    except Exception as exp:
        logger.error(f"Exception encountered: {str(exp)}")
        logger.error(traceback.format_exc())
        # Ensure we still send a valid JSON response to avoid failures during endpoint verification
        return make_response(500, {"type": 4, "data": {"content": "Internal error"}})
    finally:
        logger.write(status)
