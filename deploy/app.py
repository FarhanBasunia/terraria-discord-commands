import aws_cdk as cdk
from app_stack import AppStack

app = cdk.App()

AppStack(
    scope=app,
    stack_name="terraria-discord-commands"
)

app.synth()
