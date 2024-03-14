from typing import Optional
import re
import yaml
from src.config import config_path

def validate_parse_command_args(args_str: Optional[str]):
    if not args_str:
        return (
            None,
            None,
            None,
            "No arguments provided.\nPlease specify the channel after the command, e.g., /parse channel_name",
        )
    
    with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            video_regex = re.compile(config['regex']['youtube']['video'])
    tg_channel = None   
    args = args_str.split()
    video_url = video_regex.findall(args[0])[0] if video_regex.match(args[0]) else None 
    
    if not video_url:
        tg_channel = args[0].replace("@", "")
         
    context = " ".join(args[1:])
    limit = 100
    return tg_channel, video_url,  context, limit, ""
