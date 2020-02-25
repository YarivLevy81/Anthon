import sys
import client
import server
import web


def print_available_commands(commands):
    available_commands_str = '|'.join(commands)
    print(f'Currently available command are - [{available_commands_str}]')


if __name__ == '__main__':
    args = sys.argv
    usage = "python -m FinalProject [COMMAND] [ARGS]"
    available_commands = {"run_server": server, "upload_thought": client, "run_webserver": web}

    if len(args) < 2:
        print(usage)
        exit(1)

    command = args[1]

    if command not in available_commands:
        print(f'Command {command} is unsupported')
        print_available_commands(available_commands.keys())
        exit(1)

    available_commands[command].main(args[1:])
