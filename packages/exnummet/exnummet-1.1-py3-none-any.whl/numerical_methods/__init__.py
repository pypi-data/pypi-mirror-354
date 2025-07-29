# numerical_methods/__init__.py

import os
from pathlib import Path
import webbrowser
from pkg_resources import resource_filename
from IPython.display import display, IFrame

import subprocess
def get_presentation_path():
    """Возвращает абсолютный путь к презентации."""
    return resource_filename('numerical_methods', 'data/numerical_methods_presentation.pdf')


def show_presentation():
    """Открывает презентацию в стандартном PDF-ридере."""
    path = get_presentation_path()
    if os.name == 'nt':  # Windows
        os.startfile(path)
    elif os.name == 'posix':  # macOS/Linux
        if os.uname().sysname == 'Darwin':  # Только для macOS
            subprocess.run(["open", path])
        else:  # Linux
            subprocess.run(["xdg-open", path])
    else:
        import webbrowser
        webbrowser.open(f"file://{path}")


def get_theory():
    """Возвращает теоретическую справку."""
    pdf_path = get_presentation_path()
    display(IFrame(src=pdf_path, width=800, height=600))


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