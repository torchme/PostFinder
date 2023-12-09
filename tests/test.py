from .run_pylint import get_pylint_score

def test_pylint_quality():
    threshold = 0.75  # Set the code quality threshold
    score, output = get_pylint_score()
    assert score >= threshold, f"Code quality ({score}) is below the threshold ({threshold}).\nDetails:\n{output}"
