import subprocess
import re

def test_linter(linter_name, command, threshold=None):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        output = result.stdout

        if linter_name == "pylint":
            # Pylint outputs a final score e.g. 'Your code has been rated at 8.60/10'
            score_search = re.search(r'rated at ([0-9.]+)/10', output)
            if score_search:
                score = float(score_search.group(1))
                return 1 if score >= threshold else 0
            else:
                raise ValueError("Pylint score not found in output")

        # For other linters, you might simply check for an error-free run
        return 1  # Return 1 if no exceptions were raised (indicating success)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {linter_name}: {e.output}")
        return 0  # Return 0 if an exception was raised (indicating failure)

# Example usage of the test function for each linter:
def test_mypy():
    return test_linter("mypy", ["poetry", "run", "mypy", "."])

def test_pylint():
    threshold = 7.5  # Or any other threshold you wish to set
    return test_linter("pylint", ["poetry", "run", "pylint", "--disable=C0114,C0115,C0116,C0301,C0411,W291,W0311", "$(find . -type f -name \"*.py\" ! -path \"./venv/*\")"], threshold)

def test_black():
    return test_linter("black", ["poetry", "run", "black", ".", "--check"])

def test_isort():
    return test_linter("isort", ["poetry", "run", "isort", ".", "--check-only"])

# You could then call these functions in your test suite:
if __name__ == "__main__":
    results = {
        "mypy": test_mypy(),
        "pylint": test_pylint(),
        "black": test_black(),
        "isort": test_isort(),
    }
    print(results)

