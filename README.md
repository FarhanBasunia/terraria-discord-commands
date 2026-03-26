# Terraria Discord Commands

Discord slash commands to control a Terraria server running on AWS EC2.

This project deploys:
- An AWS Lambda function (Python 3.12)
- API Gateway endpoint for Discord interactions (`/interactions`)
- IAM role permissions to start/stop/check an EC2 instance

## Features

The bot registers and handles these slash commands:
- `/terraria-start` — starts the EC2 instance and returns the server IP
- `/terraria-stop` — stops the EC2 instance
- `/terraria-status` — checks instance status and shows connection info when running

## Project Structure

- `deploy/` — AWS CDK app and stack definition
- `lambda/` — Lambda runtime code (Discord signature verification + command handling)
- `util/` — utility script to register/list/delete Discord slash commands

## Prerequisites

- Python 3.12+
- Node.js + AWS CDK CLI (`npm install -g aws-cdk`)
- AWS credentials configured (`aws configure`)
- A Discord application/bot
- Existing EC2 instance for the Terraria server

## Required Environment Variables

### For CDK deployment

Set these in the terminal before deploying:

- `DISCORD_PUBLIC_KEY` — from Discord Developer Portal (General Information)
- `EC2_INSTANCE_ID` — the target Terraria EC2 instance ID
- `LOG_LEVEL` — optional (`DEBUG`, `INFO`, `ERROR`), defaults to `ERROR`

PowerShell example:

```powershell
$env:DISCORD_PUBLIC_KEY="your_discord_public_key"
$env:EC2_INSTANCE_ID="i-0123456789abcdef0"
$env:LOG_LEVEL="INFO"
```

### For command registration utility

- `DISCORD_APPLICATION_ID` — Discord application ID
- `DISCORD_BOT_TOKEN` — bot token

PowerShell example:

```powershell
$env:DISCORD_APPLICATION_ID="your_application_id"
$env:DISCORD_BOT_TOKEN="your_bot_token"
```

## Install Dependencies

From repo root:

```powershell
pip install -r .\lambda\requirements.txt
pip install -r .\deploy\requirements.txt
pip install -r .\util\requirements.txt
```

## Deploy to AWS

```powershell
cd .\deploy
pip install -r requirements.txt
cdk bootstrap
cdk deploy
```

After deployment, CDK outputs:
- `DiscordWebhookURL`

Use this URL in Discord interactions endpoint:

- Discord Developer Portal → Your App → Interactions Endpoint URL
- Set it to: `<DiscordWebhookURL>interactions`

> Note: the stack output already includes `/interactions` in `DiscordWebhookURL`.

## Register Slash Commands

From repo root:

```powershell
python .\util\terraria-commands.py register
```

Other utility commands:

```powershell
python .\util\terraria-commands.py list
python .\util\terraria-commands.py delete
```

This validates response shape generation for a deferred Discord interaction response.

## Notes

- Incoming Discord requests are verified using Ed25519 signatures.
- Responses are sent as ephemeral messages.
- The Lambda role currently allows EC2 actions on all resources (`*`). For production hardening, scope this to your instance ARN(s).
