import subprocess
import re
from typing import Tuple

def get_pylint_score() -> Tuple[float, str]:
    """ Run pylint and return its score and output. """
    result = subprocess.run(['pylint', 'PostFinder'], capture_output=True, text=True)

    # Print stderr for information in case of errors
    if result.returncode > 32:  # 32 and below - warning and style errors, not critical
        print("STDERR:", result.stderr)
        raise ValueError("Critical error when starting pylint")

    # Extracting pylint score from output
    match = re.search(r'Your code has been rated at ([\d.]+)/10', result.stdout)
    if match:
        return float(match.group(1)) / 10, result.stdout
    raise ValueError("Failed to get pylint evaluation")
