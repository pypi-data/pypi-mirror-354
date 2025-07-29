#PlunderGram/Modules/Recon.py

import asyncio
import requests
from datetime import datetime
import json
import os
  
def getup(target,proxy):
    """
    Function: getup

Description:
    A function that retrieves updates from a specified Telegram bot using the Telegram Bot API. 
    It returns the most recent update if available.

Arguments:
    - target: A string representing the bot token for the Telegram bot.
    - proxy: A dictionary or string representing the proxy settings to be used for the HTTP request.

Returns:
    - A dictionary representing the most recent update if available; otherwise, returns False.

Behavior:
    - Sends a GET request to the Telegram Bot API to fetch updates using the provided bot token and proxy settings.
    - Parses the JSON response from the API:
        - If the response indicates success ("ok": true):
            - If there are updates available, sorts the updates by update_id and returns the most recent update.
            - If no updates are found, prints a message and returns False.
        - If the response indicates an error, prints the error description and returns False.
    """
    # Get updates from the bot
    response = requests.get(f"https://api.telegram.org/bot{target}/getUpdates", proxies=proxy)
    updates = response.json()

    if updates["ok"]:
        if updates["result"]:
            # Sort updates by 'update_id' to get the most recent
            most_recent_update = max(updates["result"], key=lambda update: update["update_id"])
                
            return most_recent_update 
        else:
            print(f"Recon: No updates found.")
            return False
    else:
        print(f"Error fetching updates: {updates["description"]}")
        return False

async def recon(target, proxy, output_dir):
    """Function: recon

Description:
    An asynchronous function that continuously checks for updates from a specified Telegram bot 
    and saves new updates to a JSON file. It validates updates to ensure that only new messages are recorded.

Arguments:
    - target: A string representing the bot token for the Telegram bot.
    - proxy: A dictionary or string representing the proxy settings to be used for the HTTP request.
    - output_dir: A string representing the directory where the output JSON file will be saved.

Returns:
    - None

Behavior:
    - Initializes a variable ledger to track the most recent message ID for validation.
    - Constructs a filename for the JSON file based on the current date.
    - Enters an infinite loop to continuously check for updates:
        - Prints a message indicating that it is waiting for updates.
        - Waits for 5 seconds before checking for updates again.
        - Calls the getup function to retrieve updates from the bot.
        - If an update is received:
            - Extracts the message ID from the update.
            - Checks if the message ID is greater than the last recorded ledger value:
                - If it is, updates the ledger with the new message ID.
                - Loads existing data from the JSON file if it exists; otherwise, initializes an empty list.
                - Appends the new update to the list and saves it back to the JSON file.
    """
    ledger = 0 # this variable is used for new update validation
    date_str = datetime.now().strftime('%Y-%m-%d')
    filez = str(date_str + '_Recon_Updates.json')
    json_file = os.path.join(output_dir, filez)
    try:  
        while True:
            await asyncio.sleep(5)  # Wait for a few seconds before checking for updates again
                
            update = getup(target, proxy)

            if update:
                id = update["message"]["message_id"]
                if id > ledger:
                    print("Recon: Got update")
                    ledger = id
                    # Load existing data
                    if os.path.exists(json_file):
                        try:
                            with open(json_file, 'r', encoding='utf-8') as f:
                                updates = json.load(f)
                        except (json.JSONDecodeError, FileNotFoundError):
                            updates = []
                    else:
                        updates = []

                    # Append and save back
                    updates.append(update)
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(updates, f, ensure_ascii=False, indent=2)
         
            if asyncio.current_task().cancelled():
                print("Recon task was cancelled.")
                break  

    except asyncio.CancelledError:
        print("Recon task cancelled.")


              
if __name__ == "__main__":
    recon()