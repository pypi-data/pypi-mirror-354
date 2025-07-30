"""
Библиотека для просмотра кода по ячейкам

from cv_gg import ACV

acv = ACV()
print(acv.get_imports())  # Должен вывести общий импорт
print(acv.get_cell(1, 1, 0))  # Должен вывести первую ячейку первой задачи

help(acv.get_imports)
help(acv.get_cell)

"""

from .core import ACV
