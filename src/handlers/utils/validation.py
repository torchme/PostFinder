from typing import Optional


def validate_parse_command_args(args_str: Optional[str]):
    if not args_str:
        return (
            None,
            None,
            "No arguments provided.\nPlease specify the channel after the command, e.g., /parse channel_name",
        )
    args = args_str.split()
    channel = args[0]
    context = " ".join(args[1:])
    limit = 100

    return channel, context, limit, ""
