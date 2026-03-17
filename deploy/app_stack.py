import os

from aws_cdk import (
    Stack,
    Tags,
    aws_logs,
    RemovalPolicy,
    aws_iam,
    aws_lambda,
    Duration,
    aws_apigateway,
    CfnOutput
)
from constructs import Construct


class AppStack(Stack):
    def __init__(self, scope: Construct, stack_name: str, **kwargs) -> None:
        super().__init__(scope, stack_name, **kwargs)

        env_vars = {
            "DISCORD_PUBLIC_KEY": os.getenv("DISCORD_PUBLIC_KEY", "<err>"),
            "EC2_INSTANCE_ID": os.getenv("EC2_INSTANCE_ID", "<err>"),
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO")
        }

        for item in env_vars:
            if "err" in env_vars[item]:
                message = f"Missing environment variable: {item}\n"\
                    f"Inject the env variable in the current terminal"
                raise Exception(message)

        lambda_name = "terraria-discord-commands"

        log_group = aws_logs.LogGroup(
            self, f"{lambda_name.title().replace("-", "")}LogGroup",
            log_group_name=f"/aws/lambda/{lambda_name}",
            retention=aws_logs.RetentionDays.ONE_DAY,
            removal_policy=RemovalPolicy.DESTROY
        )

        lambda_role = aws_iam.Role(
            self,
            f"{lambda_name.title().replace("-", "")}Role",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Role for Terraria Discord Commands bot to manage EC2 instances",
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ]
        )

        lambda_role.add_to_policy(
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                actions=[
                    "ec2:StartInstances",
                    "ec2:StopInstances",
                    "ec2:DescribeInstances",
                    "ec2:DescribeInstanceStatus",
                ],
                resources=["*"]
            )
        )

        lambda_function = aws_lambda.Function(
            self,
            f"{lambda_name.title().replace("-", "")}Lambda",
            function_name=lambda_name,
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="app.lambda_handler",
            code=aws_lambda.Code.from_asset("../lambda"),
            role=lambda_role,
            timeout=Duration.minutes(5),
            memory_size=128,
            log_group=log_group,
            environment=env_vars
        )

        api_gateway = aws_apigateway.RestApi(
            self,
            f"{lambda_name.title().replace("-", "")}ApiGateway",
            rest_api_name=f"{lambda_name}-api-gateway",
            deploy_options=aws_apigateway.StageOptions(
                stage_name="prod",
                throttling_rate_limit=10,
                throttling_burst_limit=20,
            )
        )
        interactions = api_gateway.root.add_resource("interactions")
        
        lambda_integration = aws_apigateway.LambdaIntegration(
            lambda_function,
            proxy=True,
            allow_test_invoke=True,
        )

        interactions.add_method("POST", aws_apigateway.LambdaIntegration(lambda_integration))

        CfnOutput(self, "DiscordWebhookURL", value=f"{api_gateway.url}interactions")

        self.tags.set_tag("Project", "TerrariaDiscordBot")
