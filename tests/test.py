from .run_pylint import get_pylint_score

def test_pylint_quality():
    threshold = 0.75  # Установите пороговое значение качества кода
    score = get_pylint_score()
    assert score >= threshold, f"Качество кода ({score}) ниже порога ({threshold})"





