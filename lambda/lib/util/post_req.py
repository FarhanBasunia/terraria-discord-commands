import json
import urllib.error
import urllib.parse
import urllib.request

from lib.util.make_response import make_response


def _open_request(req: urllib.request.Request):
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode("utf-8")
    except urllib.error.HTTPError as exp:
        response_body = exp.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Discord request failed: {exp.code} {exp.reason}; body={response_body}"
        ) from exp


def post_deferred_callback(interaction_id, interaction_token):
    safe_interaction_id = urllib.parse.quote(str(interaction_id), safe="")
    safe_interaction_token = urllib.parse.quote(str(interaction_token), safe="")

    url = f"https://discord.com/api/v10/interactions/{safe_interaction_id}/{safe_interaction_token}/callback"

    data = make_response(200, {"type": 5})

    req = urllib.request.Request(
        url,
        data=data['body'].encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "TerrariaDiscordCommands/1.0",
        },
        method="POST",
    )
    _open_request(req)


def patch_original_response(application_id, interaction_token, msg):
    safe_application_id = urllib.parse.quote(str(application_id), safe="")
    safe_interaction_token = urllib.parse.quote(str(interaction_token), safe="")

    url = f"https://discord.com/api/v10/webhooks/{safe_application_id}/{safe_interaction_token}/messages/@original"

    payload = {"content": msg}
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "TerrariaDiscordCommands/1.0",
        },
        method="PATCH",
    )
    _open_request(req)
