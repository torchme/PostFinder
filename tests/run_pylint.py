import subprocess
import re
from typing import Tuple

def get_pylint_score() -> Tuple[float, str]:
    """ Run pylint and return its score and output. """
    result = subprocess.run(['pylint', 'PostFinder'], capture_output=True, text=True)

    # Assert non-critical errors
    assert result.returncode <= 32, f"Critical error when starting pylint: {result.stderr}"

    # Extracting pylint score from output
    match = re.search(r'Your code has been rated at ([\d.]+)/10', result.stdout)
    assert match, "Failed to get pylint evaluation"

    return float(match.group(1)) / 10, result.stdout

if __name__ == "__main__":
    score, output = get_pylint_score()
    print(f"Pylint score: {score}")