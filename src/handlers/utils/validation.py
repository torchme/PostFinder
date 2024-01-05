from typing import Optional


def validate_parse_command_args(args_str: Optional[str]):
    if not args_str:
        return (
            None,
            None,
            "No arguments provided.\nPlease specify the channel after the command, e.g., /parse channel_name",
        )
    args = args_str.split()
    channel = args[0]  # Mandatory argument
    if len(args) > 1:
        try:
            limit = int(args[1])
        except ValueError:
            return (
                None,
                None,
                "Limit should be a number. Default value of 10000 is set.",
            )
    else:
        limit = 10000

    return channel, limit, ""
