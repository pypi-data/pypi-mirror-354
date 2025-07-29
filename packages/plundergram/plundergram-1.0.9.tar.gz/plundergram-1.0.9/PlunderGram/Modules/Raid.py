#PlunderGram/Modules/Raid.py
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError
import asyncio 
import os
import json
from datetime import datetime
 
def savemess(message):
    """
    Saves the details of a Telegram message and its sender into a structured dictionary format.

    Arguments:
        - message: An instance of a Telegram message object containing various attributes 
          related to the message and its sender.

    Returns:
        - A dictionary containing the sender's information and the message details.

    Behavior:
        - Checks if the message has a sender. If it does, it constructs a dictionary with the sender's 
          relevant attributes, including:
            - id: Unique identifier of the sender.
            - first_name: First name of the sender (if available).
            - last_name: Last name of the sender (if available).
            - username: Username of the sender (if available).
            - phone: Phone number of the sender (if available).
            - is_bot: Boolean indicating if the sender is a bot.
            - access_hash: Access hash of the sender (if available).
            - is_verified: Boolean indicating if the sender is verified.
            - is_restricted: Boolean indicating if the sender is restricted.
            - is_deleted: Boolean indicating if the sender's account is deleted.
            - is_scammer: Boolean indicating if the sender is marked as a scammer.
            - about: About information of the sender (if available).
        - Constructs and returns a dictionary with the following structure:
            - sender: A dictionary containing the sender's information (or None if no sender).
            - message: A dictionary containing the message details, including:
                - id: Unique identifier of the message.
                - text: The text content of the message.
                - date: The date and time when the message was sent, converted to a string.
                - is_media: Boolean indicating if the message contains media.
                - media_type: The type of media (if any) associated with the message.
                - reply_to: The ID of the message this message is replying to (if applicable).
                - is_edited: Boolean indicating if the message has been edited.
                - edit_date: The date and time when the message was edited (if applicable).
                - views: The number of views the message has received (if applicable).
                - forward_info: Information about the forwarding of the message (if applicable).
    """

    sender = message.sender
    sender_dict = None
    if sender:
        sender_dict = {
            "id": sender.id,
            "first_name": getattr(sender, 'first_name', None),
            "last_name": getattr(sender, 'last_name', None),
            "username": getattr(sender, 'username', None),
            "phone": getattr(sender, 'phone', None),
            "is_bot": getattr(sender, 'bot', None),
            "access_hash": getattr(sender, 'access_hash', None),
            "is_verified": getattr(sender, 'verified', None),
            "is_restricted": getattr(sender, 'restricted', None),
            "is_deleted": getattr(sender, 'deleted', None),
            "is_scammer": getattr(sender, 'scam', None),
            "about": getattr(sender, 'about', None)
        }
    return {
        "sender": sender_dict,
        "message": {
            "id": message.id,
            "text": message.text,
            "date": str(message.date),
            "is_media": message.media is not None,
            "media_type": message.media.__class__.__name__ if message.media else None,
            "reply_to": message.reply_to_msg_id,
            "is_edited": message.edit_date is not None,
            "edit_date": str(message.edit_date) if message.edit_date else None,
            "views": getattr(message, 'views', None),
            "forward_info": str(message.fwd_from) if message.fwd_from else None,
        }
    }

async def raidmess(client, sourcechat, message_ids,json_file,chunk_size):
    """
    Function: raidmess

Description:
    An asynchronous function that retrieves messages from a specified source chat based on a list of message IDs 
    and saves the retrieved messages to a JSON file. It handles retrieval in chunks and manages potential flood wait errors.

Arguments:
    - client: An instance of the Telegram client used to retrieve messages.
    - sourcechat: An integer representing the chat ID from which messages will be retrieved.
    - message_ids: A list of integers representing the message IDs to be retrieved.
    - json_file: A string representing the path to the JSON file where the retrieved messages will be saved.
    - chunk_size: An integer representing the number of message IDs to process in each chunk.

Returns:
    - None

Behavior:
    - Checks if the specified JSON file exists:
        - If it exists, attempts to load existing messages from the file. If there is a JSON decoding error or the file is not found, initializes an empty list for messages.
        - If it does not exist, initializes an empty list for messages.
    - Prints a message indicating the range of message IDs being retrieved.
    - Iterates through the message_ids in chunks of size chunk_size:
        - For each chunk, attempts to retrieve messages by their IDs using the get_messages method of the client.
        - If a FloodWaitError occurs, waits for the specified number of seconds before retrying the retrieval.
        - Processes the retrieved messages:
            - For each message, checks if it exists and saves its data using the savemess function, appending the data to the list of all messages.
    - After processing each chunk, saves the updated list of messages back to the specified JSON file.
    - Waits for 3 seconds before processing the next chunk.
    """
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                all_messages = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            all_messages = []

    else:
        all_messages = []

    # Iterate through message IDs in chunks
    print(f"Attempting retrieval of message ids: {min(message_ids)} to {max(message_ids)}")
    for i in range(0, len(message_ids), chunk_size):
        chunk = message_ids[i:i + chunk_size]
        try:
            # Retrieve messages by their IDs
            messages = await client.get_messages(sourcechat, ids=chunk)
        except FloodWaitError as e:
            print(f'Flood wait error: {e.seconds} seconds. Waiting...')
            await asyncio.sleep(e.seconds)
            messages = await client.get_messages(sourcechat, ids=chunk)
            # Process the retrieved messages
        for message in messages:
            if message:  # Check if the message exists
                data = savemess(message)
                all_messages.append(data)
            else:
                continue

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(all_messages, f, ensure_ascii=False, indent=2)
        
        await asyncio.sleep(3)

async def raid(captain, target, sourcechat, startmess, maxmess, output_dir):
    """
Function: raid

Description:
    An asynchronous function that sets up a Telegram bot client to perform a raid operation 
    by checking a range of message IDs in a specified source chat and saving the results to a JSON file.

Arguments:
    - captain: A dictionary containing the credentials and configuration for the Telegram bot, including:
        - id: A string representing the API ID for the Telegram client.
        - hash: A string representing the API hash for the Telegram client.
        - type: A string representing the type of proxy (if any).
        - host: A string representing the proxy host (if any).
        - port: An integer representing the proxy port (if any).
    - target: A string representing the bot token for the Telegram bot.
    - sourcechat: An integer representing the chat ID from which messages will be checked.
    - startmess: An integer representing the starting message ID for the raid operation.
    - maxmess: An integer representing the maximum message ID to check.
    - output_dir: A string representing the directory where the output JSON file will be saved.

Returns:
    - None

Behavior:
    - Extracts values from the captain dictionary to configure the bot client and proxy settings.
    - Constructs a filename for the JSON file based on the current date.
    - Creates a TelegramClient instance for the bot using the provided credentials and proxy settings.
    - Starts the bot client and authenticates using the provided bot token.
    - Prints a message indicating that the bot client is connected and authenticated.
    - Creates a list of message IDs to check, ranging from startmess to maxmess.
    - Calls the raidmess function to perform the raid operation using the bot client, source chat, message IDs, and output file.
    - In the finally block, disconnects the bot client and prints a message indicating that the raid is complete.
    """
    ID = captain['id']
    HASH = captain['hash']
    type = captain['type']
    host = captain['host']
    port = int(captain['port'])
    prox = (type, host, port) 

    date_str = datetime.now().strftime('%Y-%m-%d')
    filez = str(date_str + '_Raid_Messages.json')
    json_file = os.path.join(output_dir, filez)

    bot_client = TelegramClient(StringSession(), ID, HASH, proxy=prox)
    await bot_client.start(bot_token=target)
    print("Bot client is connected and authenticated.")

    # List of message IDs to check
    message_ids = list(range(startmess, maxmess))  # Replace with actual message IDs
    try:
        await raidmess(bot_client, sourcechat, message_ids, json_file, chunk_size = int(100))
    finally:
        await bot_client.disconnect()
        print('Raid complete. Bot client disconnected.')
