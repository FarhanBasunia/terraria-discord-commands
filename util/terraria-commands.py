#!/usr/bin/env python3
"""
Utility to register Discord slash commands
Run this after deploying the CDK stack to register commands with Discord
"""

import requests
import sys
import os


def main():
    """Main function"""

    application_id = os.environ.get("DISCORD_APPLICATION_ID")
    bot_token = os.environ.get("DISCORD_BOT_TOKEN")

    if not application_id or not bot_token:
        msg = "Error: Missing Discord credentials"\
              "\nSet the following environment variables:"\
              "DISCORD_APPLICATION_ID - From Discord Developer Portal > General Information"\
              "DISCORD_BOT_TOKEN - From Discord Developer Portal > Bot > Token"\
              "\nOn Windows:"\
              "set DISCORD_APPLICATION_ID=your_app_id"\
              "set DISCORD_BOT_TOKEN=your_bot_token"\
              "python util\\bot_commands.py"
        print(msg)
        sys.exit(1)

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "list":
            list_commands(application_id, bot_token)
        elif command == "delete":
            confirm = input("Are you sure you want to delete ALL commands? (yes/no): ")
            if confirm.lower() == "yes":
                delete_all_commands(application_id, bot_token)
            else:
                print("Cancelled.")
        elif command == "register":
            register_commands(application_id, bot_token)
        else:
            print(f"Unknown command: {command}")
            print("\nUsage:")
            print("  python util\\bot_commands.py register - Register commands")
            print("  python util\\bot_commands.py list     - List registered commands")
            print("  python util\\bot_commands.py delete   - Delete all commands")
    else:
        # Default: register commands
        register_commands(application_id, bot_token)


def register_commands(application_id: str, bot_token: str):
    """Register slash commands with Discord"""

    url = f"https://discord.com/api/v10/applications/{application_id}/commands"

    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }

    # Define all commands
    commands = [
        {
            "name": "terraria-start",
            "type": 1,
            "description": "Start the Terraria game server and get the IP address"
        },
        {
            "name": "terraria-stop",
            "type": 1,
            "description": "Stop the Terraria game server"
        },
        {
            "name": "terraria-status",
            "type": 1,
            "description": "Check the current status of the game server"
        }
    ]

    print("=" * 60)
    print("Discord Slash Command Registration")
    print("=" * 60)
    print(f"\nApplication ID: {application_id}")
    print(f"API URL: {url}\n")

    success_count = 0

    for command in commands:
        print(f"Registering: /{command['name']}")
        print(f"  Description: {command['description']}")

        response = requests.post(url, headers=headers, json=command)

        if response.status_code in [200, 201]:
            print(f"  ✅ Success!\n")
            success_count += 1
        else:
            print(f"  ❌ Failed!")
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.text}\n")

    print("=" * 60)
    if success_count == len(commands):
        print(f"✅ All {len(commands)} commands registered successfully!")
    else:
        print(f"⚠️  {success_count}/{len(commands)} commands registered")
    print("=" * 60)

    return success_count == len(commands)


def list_commands(application_id: str, bot_token: str):
    """List all registered commands"""
    url = f"https://discord.com/api/v10/applications/{application_id}/commands"

    headers = {
        "Authorization": f"Bot {bot_token}"
    }

    print("\nFetching registered commands...\n")

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commands = response.json()
        if commands:
            print(f"Found {len(commands)} registered command(s):\n")
            for cmd in commands:
                print(f"  • /{cmd['name']} - {cmd['description']}")
                print(f"    ID: {cmd['id']}\n")
        else:
            print("No commands registered yet.")
    else:
        print(f"❌ Failed to fetch commands")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")


def delete_all_commands(application_id: str, bot_token: str):
    """Delete all registered commands"""
    url = f"https://discord.com/api/v10/applications/{application_id}/commands"

    headers = {
        "Authorization": f"Bot {bot_token}"
    }

    # Get all commands
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commands = response.json()

        if not commands:
            print("No commands to delete.")
            return

        print(f"Deleting {len(commands)} command(s)...\n")

        for cmd in commands:
            delete_url = f"{url}/{cmd['id']}"
            delete_response = requests.delete(delete_url, headers=headers)

            if delete_response.status_code == 204:
                print(f"✅ Deleted /{cmd['name']}")
            else:
                print(f"❌ Failed to delete /{cmd['name']}")
    else:
        print("Failed to fetch commands for deletion")


if __name__ == "__main__":
    main()
