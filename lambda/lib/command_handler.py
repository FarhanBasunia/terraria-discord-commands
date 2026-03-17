from lib.util.post_req import patch_original_response
from lib.util.post_req import post_deferred_callback
from lib.util.make_response import make_response
from lib.logger import Logger

import boto3


logger = Logger()


def command_handler(command_name, app_id, token, interaction_id, ec2_instanceid):
    logger.info(f"command_name: {command_name}")
    logger.info(f"app_id: {app_id}")
    logger.info(f"token: {token}")
    logger.info(f"interaction_id: {interaction_id}")

    post_deferred_callback(interaction_id, token)

    ec2_client = boto3.client('ec2')

    if command_name == "terraria-status":
        terraria_status(ec2_client, ec2_instanceid, app_id, token)
    elif command_name == "terraria-start":
        terraria_start(ec2_client, ec2_instanceid, app_id, token)
    elif command_name == "terraria-stop":
        terraria_stop(ec2_client, ec2_instanceid, app_id, token)


def get_instance_status(ec2_client, ec2_instanceid):
    response = ec2_client.describe_instances(InstanceIds=[ec2_instanceid])
    inst = response['Reservations'][0]['Instances'][0]
    return inst['State']['Name'], inst.get('PublicIpAddress')


def terraria_status(ec2_client, ec2_instanceid, app_id, token):
    state, public_ip = get_instance_status(ec2_client, ec2_instanceid)

    message = f"🌹 Running at `{public_ip}:7777`" if state == 'running' else f"🥀 Server status: {state}"

    patch_original_response(app_id, token, message)


def terraria_start(ec2_client, ec2_instanceid, app_id, token):
    state, public_ip = get_instance_status(ec2_client, ec2_instanceid)

    if state != "running":
        ec2_client.start_instances(InstanceIds=[ec2_instanceid])
        waiter = ec2_client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[ec2_instanceid], WaiterConfig={'Delay': 5, 'MaxAttempts': 20})
        _, public_ip = get_instance_status(ec2_client, ec2_instanceid)
    message = f"🌹 Terraria server is up 😊\nConnect to: `{public_ip}:7777`"

    patch_original_response(app_id, token, message)


def terraria_stop(ec2_client, ec2_instanceid, app_id, token):
    ec2_client.stop_instances(InstanceIds=[ec2_instanceid])
    message = f"🥀 Terraria server is shutting down. Thanks for playing"

    patch_original_response(app_id, token, message)
