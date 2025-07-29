#PlunderGram/Modules/Spyglass.py
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import BotMethodInvalidError
import requests
import json
import asyncio
import os
from datetime import datetime
  
def get_webhook_info(target, proxy):
    """
    Retrieves information about the webhook configuration for a specified Telegram bot.

    Arguments:
        - target: A string representing the bot token used to authenticate the request.
        - proxy: A dictionary containing proxy settings for the request (if needed).

    Returns:
        - A dictionary containing the JSON response from the Telegram API, which includes 
          details about the webhook configuration.

    Behavior:
        - Sends a GET request to the Telegram API endpoint for retrieving webhook information 
          using the provided bot token and proxy settings.
        - Parses the JSON response from the API and returns it as a dictionary.
    """

    response = requests.get(f"https://api.telegram.org/bot{target}/getWebhookInfo", proxies=proxy)
    return response.json()

def hookinfo(target, proxy):
    """
    Retrieves the webhook information for a specified Telegram bot and checks if a webhook is set.

    Arguments:
        - target: A string representing the bot token used to authenticate the request.
        - proxy: A dictionary containing proxy settings for the request (if needed).

    Returns:
        - A dictionary containing the webhook information if a webhook is set.
        - None if no webhook is currently set.

    Behavior:
        - Calls the get_webhook_info function to retrieve the webhook configuration for the bot.
        - Checks if the "url" field in the "result" of the webhook information is present.
            - If a webhook URL is found, it returns the webhook information.
            - If no webhook URL is set, it prints a message indicating that no webhook is currently set.
    """

    webhook_info = get_webhook_info(target, proxy)
    
    if webhook_info["result"]["url"]:
        return webhook_info
    else:
        print("No webhook is currently set.")

async def spyglass(captain,target, proxy, output_dir):
    """
    Asynchronously retrieves and saves information about a Telegram bot, including its details and webhook configuration.

    Arguments:
        - captain: A dictionary containing the bot's credentials and connection details, including:
            - id: The bot's ID.
            - hash: The bot's hash.
            - type: The type of proxy (if any).
            - host: The proxy host (if any).
            - port: The proxy port (if any).
        - target: A string representing the bot token used to authenticate the request.
        - proxy: A tuple containing the proxy settings for the request.

    Returns:
        - None

    Behavior:
        - Extracts the bot's ID, hash, type, host, and port from the captain dictionary.
        - Constructs a proxy tuple and generates a filename for saving bot details based on the current date.
        - Initializes a Telegram client using the provided credentials and proxy settings, and starts it with the bot token.
        - Retrieves the bot's information and webhook configuration.
        - Checks if a JSON file for storing existing data exists:
            - If it exists, attempts to load the existing data. If there is a JSON decoding error or the file is not found, initializes an empty list.
            - If it does not exist, initializes an empty list.
        - Combines the retrieved bot information and webhook information into a single record and appends it to the existing data.
        - Writes the updated list of data back to the JSON file, ensuring proper formatting.
        - Handles exceptions for invalid bot tokens and other errors, printing appropriate messages.
        - Disconnects the Telegram client after the operation is complete.
    """

    ID = captain['id']
    HASH = captain['hash']
    type = captain['type']
    host = captain['host'] 
    port = int(captain['port'])
    prox = (type,host,port)
    date_str = datetime.now().strftime('%Y-%m-%d')
    filez = str(date_str + '_Spyglass_BotDetail.json')
    json_file = os.path.join(output_dir, filez)
    bot_client = TelegramClient(StringSession(), ID, HASH, proxy=prox)
    await bot_client.start(bot_token=target)

    try:
        bot = await bot_client.get_me()
        bot_info = {
        "id": bot.id,
        "first_name": bot.first_name,
        "username": bot.username,
    }
        hook_info = hookinfo(target, proxy)   

        # Load existing data or create empty list
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                existing_data = []
        else:
            existing_data = []

        # Append new record
        combined_data = {
            "bot_info": bot_info,
            "hook_info": hook_info
        }
        existing_data.append(combined_data)

        # Write updated list back to JSON file
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

    except BotMethodInvalidError:
        print("The bot token is invalid or has been revoked.")
    except asyncio.CancelledError:
        print("Spyglass Cancelled")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        print('Spyglass Complete')
        await bot_client.disconnect()

