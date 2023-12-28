from typing import Optional


def validate_parse_command_args(args_str: Optional[str]):
    # If args_str is None or empty, return with an error message
    if not args_str:
        return (
            None,
            None,
            "No arguments provided.\nPlease specify the channel after the command, e.g., /parse channel_name",
        )

    args = args_str.split()

    # Extract and validate arguments
    channel = args[0]  # Mandatory argument

    # Assign and validate the optional 'limit' argument
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
        limit = 10000  # Default value if the argument is not provided

    return channel, limit, ""
