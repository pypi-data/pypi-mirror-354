# Plundergram: A Telegram OSINT and recon tool (for research use only).

## Disclaimer:
This project is intended for educational and research purposes only.
Users are solely responsible for ensuring their use of this tool complies with Telegram’s Terms of Service and all applicable laws.
The author does not condone or accept liability for any misuse, unethical behavior, or illegal activity involving this software.

## Description:
Plundergram is a reconnaissance tool built for analyzing activity on Telegram using both the Telegram API and Bot API. It enables researchers and analysts to extract detailed insights from Telegram channels, groups, and bots.

Key capabilities include:

- Identifying and profiling Telegram bots

- Retrieving bot commands and messages sent via bots

- Collecting messages from public and private chats (where access is available)

- Accessing historical chat data for analysis

Plundergram is intended for investigative and research purposes, such as analyzing credential phishing operations, tracking threat actor activity, or conducting OSINT (Open Source Intelligence) on Telegram-based networks.

## Features

- Telegram Bot Profiling: Identify and gather metadata about Telegram bots, including usernames, IDs, and associated channels or groups.

- Command Extraction: Capture and analyze commands sent to bots to understand their interaction patterns.

- Message Collection: Retrieve messages sent by bots and users within public and private chats.

- Historical Chat Retrieval: Access and analyze historical chat logs for comprehensive intelligence gathering.

- Multi-Channel Support: Work across various Telegram channels, groups, and private chats.

- Telegram API & Bot API Integration: Utilizes official Telegram APIs to ensure reliable and efficient data collection.

- CLI Tool: Easy-to-use command-line interface for quick reconnaissance and automation.

- Extensible and Scriptable: Designed for integration with other tools and workflows in cybersecurity and OSINT investigations.

## Installation

### Prerequisites

Prerequisites
Python 3.7 or higher
Telethon 1.28.5 or higher
Requests 2.25.0 or higher
Telegram - https://telegram.org/apps
Telegram API credentials (API ID and API Hash) — Get yours here:https://core.telegram.org/api#getting-started
Currently uses Tor proxy, untested with other proxies but this is configurable. (Better proxy handling to come in future releases)


### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/username/repository-name.git
    ```

2. Install the package and dependencies:

    ```bash
    pip install PlunderGram
    ```

3. Configuration

    Edit the config.ini file and replace values with your information

4. Run the project:
    For CLI:
        - For Python:
            ```bash
            python Plunder.py
            ```
    CLI Bypass:
        - For Python:
            ```bash
            python Plunder.py -h for commands
            ```

## Usage

**See docs folder for full details on each module.**

PlunderGram can be used to accomplish the following objectives:

1. Collect information on a Telegram Bot
2. Collect commands sent to a Telegram Bot.
3. Collect new messages sent to a Telegram Chat from a Telegram Bot in real time.
4. Collect all messages in a Telegram chat (does not include deleted messages). 

**Important note:**
> - Message IDs are not necessarily incrememental, so we are essentially guessing valid message IDs during historical message retrieval. -
> - Retrieval occurs in chunks of 100 with a 3 second delay between chunks for rate limiting purposes. 
> - Max rate is 2000 message ID retrievals per minute.

Guide:

1. Enter information into the config file (config.ini)

2. Run Plunder
    CLI Bypass:
    Example Usage: python3 Plunder Recon
    
    Command List:
    (Required)
    [Recon]
    Description:
    An asynchronous function that continuously checks for updates from a specified Telegram bot 
    and saves new updates to a JSON file. It validates updates to ensure that only new messages are recorded.

    [Boarding]
    Description:
        An asynchronous function that sets up a Telegram bot client, establishes contact with a specified bot, 
        and forwards messages from a source chat to a destination chat. 
        It handles the connection and disconnection of the bot client.

    [Raid] 
    Description:
        An asynchronous function that sets up a Telegram bot client to perform a raid operation 
        by checking a range of message IDs in a specified source chat and saving the results to a JSON file.

    Arguments(required):
    [--startmess]
    Message ID to start on (int)
    [--maxmess]
    Message ID to end on (int)


    (Optional - Overrides Config data)
    [--token] 
        Telegram Bot Token - Optional for Recon, Boarding, Raid
    [--sourcechat]
        Source Chat ID (int) - Optional for Boarding, Raid
    [--treasurechest]
        Directory Path for storing output file - Optional for Recon, Boarding, Raid

    Full CLI:
    Example Usage: python3 Plunder

    CLI Command Detail:
    [SOS] --> Displays command details.
    [Sitrep] --> Shows all running tasks.
    [Spyglass] --> checks if target is viable and returns target detail if successful.
    [Recon] --> polls for commands sent to target. This can be used for additional user/chat discovery.
    [Boarding] --> initiates contact with target and begins collection of new messages from target chat.
    [Raid] --> Retrieves all historical messages from target chat.
    [Submerge] --> Stops all running commands.
    [Sink] --> Stops running command specified by user response to prompt.
    [Kill] --> Terminates program.

3. Output files are stored in an adjacent directory that can be specified wihtin the config file. The default directory is [TreasureChest]


## Contributing

Contributions are welcome! To contribute:

- Fork the repository

- Create a new branch (git checkout -b feature-name)

- Make your changes and commit them (git commit -m 'Add some feature')

- Push to your fork (git push origin feature-name)

- Open a Pull Request on the main repository

Please follow the coding style and add tests where possible.

## Support

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-yellow?logo=buymeacoffee&style=for-the-badge)](https://www.buymeacoffee.com/kpwnthr)


## License

This project is licensed under the Apache License 2.0 — see the LICENSE file for details.

## Acknowledgments

Inspired by OSINT and cybersecurity research communities.

Thanks to the creators of Telethon for the Telegram API library.

Thanks to the creators of ASCII Art Archive and associated tools.

Special thanks to anyone who contributed or helped test this project.
