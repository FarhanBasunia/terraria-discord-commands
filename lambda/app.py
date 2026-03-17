import base64
import json
import logging
import os
import traceback

from lib.util.make_response import make_response
from lib.util.verify_signature import verify_signature
from lib.command_handler import command_handler
from lib.logger import Logger

logger = Logger(__name__)
DISCORD_PUBLIC_KEY = os.environ["DISCORD_PUBLIC_KEY"]
EC2_INSTANCE_ID = os.environ["EC2_INSTANCE_ID"]


def lambda_handler(event, context):
    status = False
    try:
        logger.info(f"Event: {event}")

        signature_verification, body = verify_signature(event, DISCORD_PUBLIC_KEY)

        if not signature_verification:
            return make_response(401, {"error": "Invalid signature"})

        body = json.loads(body)
        interaction_type = body.get("type")
        # Discord ping
        if interaction_type == 1:
            logger.debug("returning ping")
            status = True
            return make_response(200, {"type": 1})

        elif interaction_type == 2:
            command_name = body["data"]["name"]
            app_id = body["application_id"]
            token = body["token"]
            interaction_id = body["id"]
            

            status = True
            command_handler(command_name, app_id, token, interaction_id, EC2_INSTANCE_ID)

        logger.info(f"Unknown interaction type: {body.get('type')}")
        return make_response(400, {"error": "Unknown request"})

    except Exception as exp:
        logger.error(f"Exception encountered: {str(exp)}")
        logger.error(traceback.format_exc())
        return make_response(500, {"type": 4, "data": {"content": "Internal error"}})
    finally:
        logger.write(status)
