#!/usr/bin/env python3
import asyncio
import os
import argparse
import tracemalloc
from PlunderGram.Modules import *
           
tracemalloc.start()
"""This beginnning section handles the config file and global variable initialization."""
# Define the config file name
config_file = 'config.ini'  
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the config file
config_path = os.path.join(script_dir, config_file)

# Pull from config
config, colors = load(config_path)
CC = colors['color_code']
target = config['Targets']['target']
sourcechat = config['Targets']['channel']
captain = config['Captain']
proxy = {
    'http': config['Navigation']['http'],
    'https': config['Navigation']['https']
}
output_dir = config['Treasure Chest']['x']

if output_dir == '0':
    output_dir = 'TreasureChest'
    output_path = os.path.join(script_dir, output_dir)

os.makedirs(output_dir, exist_ok=True)

#initialize global variables
startmess = 1
maxmess = 1000
tasks = {}

broadside = f"""{CC}\n\nAhoy! \nPlunder initialized with {config_file} configuration.\n 
          The following commands can be entered as needed during program execution:\n\n
          [SOS] --> Displays this message.\n
          [Sitrep] --> Shows all running tasks.\n
          [Spyglass] --> checks if target is viable and returns target detail if successful.\n
          [Recon] --> polls for updates sent to bot. This can be used for additional user/chat discovery.\n
          [Boarding] --> initiates contact with target and begins collection of new messages from target chat.\n
          [Raid] --> Retrieves all historical messages from target chat.\n
          [Submerge] --> Stops all running commands.\n
          [Sink] --> Stops running specific command based on user response from prompt.\n 
          [Kill] --> Terminates program.\n\n"""


async def userInput(prompt: str) -> str:
    """
Function: userInput

Description:
    Asynchronous function to handle user input.

Arguments:
    - prompt (str): A string that serves as a message or question displayed to the user, prompting them for input.

Returns:
    - (str): The user input as a string.

    """
    try:
        # Print the prompt and flush the output
        print(prompt, end='', flush=True)  # Ensure the prompt is printed immediately
        user_input = await asyncio.to_thread(input)  # Get user input
        #print(f"Input: {user_input}")  # Debugging: Print the actual input received
    except KeyboardInterrupt:
        print("\nInput interrupted by user.")
        return 'kill'

    except Exception as e:
        print(f"userInput error: {e}")
        user_input = ""  # Return an empty string in case of error
    return user_input


async def submerge():
    """
    Function: submerge

Description:
    An asynchronous function that checks the status of tasks in a dictionary and cancels any that are not completed. 
    It also handles exceptions that may occur during the process.

Arguments:
    - None

Returns:
    - None

Behavior:
    - Iterates through the `tasks` dictionary.
    - Checks if each task is completed:
        - If a task is already done, it prints a message indicating that.
        - If a task is not done, it cancels the task, removes it from the `tasks` dictionary, and prints a cancellation message.
    - Catches and prints any exceptions that occur during the execution of the function.

    """
    try:
        tasks_copy = list(tasks.items())  # Makes a copy of the tasks to avoid modifying during iteration
        for task_name, task in tasks_copy:
            if not task.done():
                task.cancel()
                await task  # Waits until the task is actually cancelled
                print(f"Task {task_name} cancelled.")
            else:
                print(f"Task {task_name} was already done.")
    except Exception as e:
        print(f"Submerge failed with exception: {e}")

            

async def sitrep():
    """
    Function: sitrep

    Description:
        An asynchronous function that retrieves and prints the names of currently running tasks. 
        It specifically highlights tasks of interest.

    Arguments:
        - None

    Returns:
        - None

    Behavior:
        - Uses `asyncio.all_tasks()` to get a list of all currently running tasks.
        - Prints a header indicating that it will list currently running tasks.
        - Iterates through the list of tasks and retrieves their names.
        - If a task's name matches one of the specified names ("Recon", "Spyglass", "Raid", "Boarding"), it prints the task's name.
        - Catches and prints any exceptions that occur during the execution of the function.

    """
    try:
        status = asyncio.all_tasks()
        print("Currently running tasks:\n")
        for update in status:
            task_name = update.get_name()
            if task_name in ["Recon", "Spyglass", "Raid", "Boarding"]:
                print(f"{task_name}\n")
 
    except Exception as e:
       print(f" Sitrep failed with exception: {e}")


async def centralcommand(commandqueue):
    """
    Function: centralcommand

Description:
    An asynchronous function that processes commands from a command queue, executes corresponding tasks, 
    and manages task execution and user input. It handles various commands related to task management 
    and provides feedback to the user.

Arguments:
    - commandqueue: An asynchronous queue (typically an instance of asyncio.Queue) from which commands are retrieved for processing.

Returns:
    - None

Behavior:
    - Enters an infinite loop to continuously process commands from the commandqueue.
    - Acquires a lock (command_lock) to ensure that command execution is thread-safe.
    - For each command received:
        - Checks if the command is already running and prints a message if so.
        - Executes specific tasks based on the command:
            - **spyglass**: Creates and starts spyglass task.
            - **recon**: Creates and starts recon task.
            - **boarding**: Prompts for a source chat ID and starts boarding task.
            - **raid**: Prompts for a source chat ID and message ID range, then starts raid task.
            - **submerge**: Starts submerge task.
            - **sitrep**: Starts sitrep task.
            - **sink**: Prompts for a task to stop and cancels it if found.
            - **kill**: Breaks the loop and stops the command processing.
            - **sos**: Prints broadside.
    - Calls task_done() on the command queue to indicate that the command has been processed.
    """
    global sourcechat, startmess, maxmess
    command_lock = asyncio.Lock()
    try:
        while True:
            command = await commandqueue.get()

            async with command_lock:  # 👈 Lock execution of a command
                print(f"Command received: {command}")
            try:
                match command:
                    case _ if command.lower() in tasks and not tasks[command.lower()].done():
                        print(f"{command} is already running. Please cancel to restart task execution.")

                    case 'spyglass':
                        print(f"Executing {command}.")
                        spy = asyncio.create_task(spyglass(captain, target, proxy, output_dir),name="Spyglass") 
                        tasks['spyglass'] = spy

                    case 'recon':
                        print(f"Executing {command}.")
                        rec = asyncio.create_task(recon(target, proxy, output_dir), name="Recon")
                        tasks['recon'] = rec 

                    case 'boarding':
                        print(f"Executing {command}.")
                        
                        try:
                            if sourcechat == 0:
                                while True:
                                    sourcechat = await userInput("Enter source Chat ID. If you do not have the Chat ID enter none and run Recon to poll for updates: ")
                                    if sourcechat.lower()  == 'none':
                                        sourcechat = 0
                                        break
                                    try:
                                        int(sourcechat)
                                        break
                                    except Exception as e:
                                        print('Invalid Input')
                                        continue
                                        
                        except Exception as e:
                            print(f"Boarding error {e}")
                        print(f"Boarding! ChatID = {sourcechat}")
                        boa = asyncio.create_task(boarding(captain, target, int(sourcechat),output_dir),name="Boarding")
                        tasks['boarding'] = boa

                    case 'raid':
                        print(f"Executing {command}.")

                        try:
                            if sourcechat == 0:
                                while True:
                                    sourcechat = await userInput("Enter source Chat ID. If you do not have the Chat ID enter none and run Recon to poll for updates: ")
                                    if sourcechat.lower()  == 'none':
                                        sourcechat = 0
                                        break
                                    try:
                                        int(sourcechat)
                                        break
                                    except Exception as e:
                                        print('Invalid Input')
                                        continue
                        except Exception as e:
                            print(f"Raid error {e}")
                        try:
                            Q = await userInput(f"Continue with default messageID range: {startmess}, {maxmess}? (Y/N)")
                            if Q.lower() == 'n' or Q.lower() == 'no':
                                while True:
                                    startmess = await userInput("Enter messageID to start with: ")
                                    try:
                                        int(startmess)
                                        break
                                    except Exception as e:
                                        print('Invalid Input.')
                                        continue
                                while True:   
                                    maxmess = await userInput("Enter messageID to end on: ")
                                    try:
                                        int(maxmess)
                                        break
                                    except Exception as e:
                                        print('Invalid Input.')
                                        continue
                            else:
                                print('Running Raid with default settings. Raiding!')
                        except Exception as e:
                            print(f"Raid error {e}")
                        print('Raiding!')
                        rai = asyncio.create_task(raid(captain, target, int(sourcechat), int(startmess), int(maxmess), output_dir),name="Raid") 
                        tasks['raid'] = rai 

                    case 'submerge':
                        print(f"Executing {command}.")
                        sub = asyncio.create_task(submerge(), name="Submerge") 
                        tasks['submerge'] = sub 

                    case 'sitrep':
                        print(f"Executing {command}.")
                        sit = asyncio.create_task(sitrep(), name="Sitrep")
                        tasks['sitrep'] = sit

                    case 'sink':
                        print(f"Executing {command}.")

                        asyncio.create_task(sitrep(), name="Sitrep")
                        await asyncio.sleep(1)
                        finisher = await userInput("Enter a task to stop: ")
                        print(f"Task to stop: {finisher}") #debugging
                        if finisher in tasks:
                            tasks[finisher].cancel()  # Cancel the specific task
                            del tasks[finisher]  # Remove it from the tracking dictionary
                            print(f"Cancelled task: {finisher}")
                        else:
                            print(f"No task found with name: {finisher}")

                    case 'kill': 
                        print(f"Executing {command}.")
                        break

                    case 'sos':
                        print(f"Executing {command}.")
                        print(broadside)
                    case _:
                        print(f"unkown")
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt received. Exiting...")
                break
            except asyncio.CancelledError:
                print("Central command loop cancelled.")
                break

            finally:
                commandqueue.task_done()
    except asyncio.CancelledError:
                print("Central command task cancelled.")

async def main():
    """
    Function: main

    Description:
        An asynchronous entry point that optionally bypasses the interactive CLI by parsing
        command-line arguments to run Recon, Boarding, or Raid commands directly.
        If no command-line subcommand is provided, it runs the full interactive command loop.

    Arguments:
        - None

    Returns:
        - None

    Behavior:
        - Parses CLI arguments using argparse with optional subcommands:
            - Recon (no additional args)
            - Boarding (no additional args)
            - Raid (requires --startmess and --maxmess)
        Also accepts global optional overrides (--target, --sourcechat, --treasurechest).
        - If a recognized subcommand is provided:
            - Calls the corresponding function immediately, passing appropriate arguments.
            - Awaits async functions where necessary.
        - If no subcommand is given:
            - Prints an initialization message and a broadside (banner or status).
            - Defines a list of valid interactive commands.
            - Creates an asyncio.Queue to manage commands.
            - Starts an async task (`fleetcommander`) to process commands from the queue via `centralcommand`.
            - Enters an infinite loop, asynchronously accepting user input:
                - Validates the input command against the allowed commands.
                - For valid commands:
                    - Puts the command into the queue.
                    - Waits until the command is fully processed (`commandqueue.join()`).
                    - Special handling for 'kill' command to print exit message.
                - For invalid commands:
                    - Prints an error message.
                - Allows graceful exit on KeyboardInterrupt.
            - In the finally block, ensures proper cleanup by queuing 'submerge' and 'kill' commands,
            cancels the `fleetcommander` task, and waits for the queue to be fully processed.
    """

    parser = argparse.ArgumentParser(description="Plundergram: A Telegram OSINT and recon tool (for research use only).")
    
    subparsers = parser.add_subparsers(dest="function", required=False)

    reconparser = subparsers.add_parser("Recon", help="Run Recon")

    boardingparser = subparsers.add_parser("Boarding", help="Run Boarding")

    raidparser = subparsers.add_parser("Raid", help="Run Raid")
    raidparser.add_argument('--startmess', type=int, help="Starting Message ID", required=True)
    raidparser.add_argument('--maxmess', type = int,help="Ending Message ID", required=True)

    parser.add_argument('--target', help="Telegram Bot Token (can override config)")
    parser.add_argument('--sourcechat', type=int, help="Source Chat ID (can override config)")
    parser.add_argument('--treasurechest', help="Directory Path for storing output file (can override config)")

    args = parser.parse_args()

    if args.function == "Recon":
        try:
            await recon(target, proxy, output_dir)
        except Exception as e:
            print(f"Recon error:{e}")
    elif args.function == "Boarding":
        try:
            await boarding(captain, target, int(sourcechat),output_dir)
        except Exception as e:
            print(f"Boarding error:{e}")
    elif args.function == "Raid":
        try:
            await raid(captain, target, int(sourcechat), int(args.startmess), int(args.maxmess), output_dir)
        except Exception as e:
            print(f"Raid error:{e}")
    else:
        print(f"{CC}Initializing Plunder\n")
        Flag()
        print(broadside)
        #print(output_path) # debugging
        validcommands = ['spyglass', 'recon', 'boarding', 'raid', 'submerge', 'sink', 'kill', 'sos', 'sitrep']
        commandqueue = asyncio.Queue()  
        fleetcommander = asyncio.create_task(centralcommand(commandqueue))
        try:
            while True:
                command = await userInput("Enter command: ")
                if command.lower() in validcommands:
                    if command.lower() == 'kill':
                        print(f"{command} received, closing program...")
                        break
                    await commandqueue.put(command.lower())
                    await commandqueue.join()  # Wait for command to fully finish

                else:
                    print(f"Unknown command: {command}")

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt received. Exiting...")
        except asyncio.CancelledError:
            print('Main loop cancelled')
        finally:
            print("In finally block - starting cleanup")
            try:
                fleetcommander.cancel()

                print("Fleetcommander cancelled.")
            except asyncio.CancelledError:
                print('Fleetcommander already cancelled.')

            # Cancel all other tasks
            for task in tasks.values():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    print(f"Task {task} cancelled.")

            await asyncio.gather(*tasks.values(), return_exceptions=True)

            print("Cleanup done, now exiting...")

def cli():
    asyncio.run(main())
    
if __name__ == "__main__":
    cli() #sync wrapper