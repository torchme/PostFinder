import subprocess
import re

def get_pylint_score() -> float:
    """ Запустить pylint и вернуть его оценку. """
    result = subprocess.run(['pylint', 'PostFinder'], capture_output=True, text=True)

    # Выводим stderr для информации в случае ошибок
    if result.returncode > 32:  # 32 и ниже - предупреждения и ошибки стиля, не критические
        print("STDERR:", result.stderr)
        raise ValueError("Критическая ошибка при запуске pylint")

    # Извлечение оценки pylint из вывода
    match = re.search(r'Your code has been rated at ([\d.]+)/10', result.stdout)
    if match:
        return float(match.group(1)) / 10
    raise ValueError("Не удалось получить оценку pylint")

if __name__ == "__main__":
    score = get_pylint_score()
    print(f"Pylint score: {score}")  # Убедитесь, что эта строка присутствует
