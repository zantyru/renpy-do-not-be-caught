# -*- coding: utf-8 -*-

"""Некоторый инструментарий для работы с регулярной сеткой
из шестиугольников. Функция вычисления координат соседней ячейки,
функция открытия-закрытия границ ячейки."""


TOP = "top"
TOPRIGHT = "topright"
BOTTOMRIGHT = "bottomright"
BOTTOM = "bottom"
BOTTOMLEFT = "bottomleft"
TOPLEFT = "topleft"
SIDES = (TOP, TOPRIGHT, BOTTOMRIGHT, BOTTOM, BOTTOMLEFT, TOPLEFT)

_impassable = set()


class WrongSideException(Exception):
    pass


def neighbor(col, row, side):
    
    even = 1 - col % 2
    odd = 1 - even
    
    guide = {
        TOP:
            (0, -1, BOTTOM),
        TOPRIGHT:
            (1, -even, BOTTOMLEFT),
        BOTTOMRIGHT:
            (1, odd, TOPLEFT),
        BOTTOM:
            (0, 1, TOP),
        BOTTOMLEFT:
            (-1, odd, TOPRIGHT),
        TOPLEFT:
            (-1, -even, BOTTOMRIGHT),
    }
    
    try:
        dcol, drow, backside = guide[side]
    except KeyError:
        raise WrongSideException(
            "'{}' is not a valid side".format(side)
        )
    
    return col + dcol, row + drow, backside


def edge_passable(colA, rowA, colB, rowB, oneway=False):
    
    result1 = (colA, rowA, colB, rowB) not in _impassable
    result2 = (colB, rowB, colA, rowA) not in _impassable
    
    if oneway:
        result2 = True
    
    return result1 and result2


def open_edge(col, row, side, oneway=False):
    
    colN, rowN, _ = neighbor(col, row, side)
    _impassable.discard((col, row, colN, rowN))
    if not oneway:
        _impassable.discard((colN, rowN, col, row))


def close_edge(col, row, side, oneway=False):
    
    colN, rowN, _ = neighbor(col, row, side)
    _impassable.add((col, row, colN, rowN))
    if not oneway:
        _impassable.add((colN, rowN, col, row))


def clear():
    
    _impassable.clear()
