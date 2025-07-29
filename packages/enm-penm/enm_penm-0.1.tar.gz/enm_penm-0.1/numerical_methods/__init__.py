# numerical_methods/__init__.py

import os
from pathlib import Path
import webbrowser


def get_presentation_path():
    """Возвращает путь к презентации."""
    package_dir = Path(__file__).parent
    presentation_path = package_dir / "data" / "numerical_methods_presentation.pdf"
    if not presentation_path.exists():
        raise FileNotFoundError("Презентация не найдена!")
    return str(presentation_path)


def show_presentation():
    """Открывает презентацию в стандартном PDF-ридере."""
    path = get_presentation_path()
    webbrowser.open(path)


def get_theory():
    """Возвращает теоретическую справку."""
    return {
        "root_finding": "Методы решения нелинейных уравнений: дихотомия, Ньютона, секущих.",
        "linear_algebra": "Методы решения СЛАУ: Гаусса, Якоби, Зейделя.",
        "integration": "Численное интегрирование: метод трапеций, Симпсона.",
    }


# Пример численного метода (метод Ньютона)
def newton_method(f, df, x0, tol=1e-6, max_iter=100):
    """
    Реализация метода Ньютона для нахождения корня f(x) = 0.

    Параметры:
        f: Функция, корень которой ищем.
        df: Производная f.
        x0: Начальное приближение.
        tol: Допустимая погрешность.
        max_iter: Максимальное число итераций.

    Возвращает:
        Найденный корень или None, если не сошлось.
    """
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x
        dfx = df(x)
        if dfx == 0:
            return None
        x = x - fx / dfx
    return None

show_presentation()