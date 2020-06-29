# -*- coding: utf-8 -*-

from __future__ import division
from collections import defaultdict
import grid


"""Здесь собран код только игровой логики: данные и их обработка
в рамках механики игры. Визуализация в другом модуле."""


class CellData(object):
    """
    Данные ячейки игрового поля. Тут не видно, но предполагается,
    что это шестиугольник ("шестисторонник").
    """
    
    __slots__ = ("col", "row", "top", "topright", "bottomright",
    "bottom", "bottomleft", "topleft", "distance")
    
    def __init__(self, col, row, top=None, topright=None,
    bottomright=None, bottom=None, bottomleft=None, topleft=None):
        
        """
        top, topright, bottomright, bottom, bottomleft, topleft - ссылки
        на соседние ячейки, значение None обозначает невозможность
        перехода из *этой* ячейки.
        
                        top
                     WWWWWWWWW
                    W         W
           topleft W           W topright
                  W             W
                   W           W 
        bottomleft  W         W  bottomright
                     WWWWWWWWW 
        
                      bottom
        """
        
        self.col = int(col)
        self.row = int(row)
        self.top = top
        self.topright = topright
        self.bottomright = bottomright
        self.bottom = bottom
        self.bottomleft = bottomleft
        self.topleft = topleft
        self.distance = None
    
    @staticmethod
    def neighbors(cell):
        """
        Возвращает итератор ссылок на соседей. Ссылки могут иметь
        значение None.
        """
        
        yield cell.top
        yield cell.topright
        yield cell.bottomright
        yield cell.bottom
        yield cell.bottomleft
        yield cell.topleft
    
    @staticmethod
    def not_none_neighbors(cell):
        """
        Возвращает итератор не None ссылок на соседей.
        """
        
        for n in CellData.neighbors(cell):
            if n is None:
                continue
            yield n


class CreatureData(object):
    """
    Данные о "живой сущности". Убегающей и догоняющей.
    """
    
    INACTIVE = 0 # выбыл из игры
    STUPID_PURSUER = 1 # глупый преследователь
    CLEVER_PURSUER = 2 # умелый преследователь
    PLAYER = 3 # игрок
    
    __slots__ = ("cell", "role")
    
    def __init__(self, cell=None, role=None):
        
        self.cell = cell
        self.role = role
    
    @staticmethod
    def roles():
        
        yield CreatureData.INACTIVE
        yield CreatureData.PLAYER
        yield CreatureData.STUPID_PURSUER
        yield CreatureData.CLEVER_PURSUER


class LevelData(object):
    """
    Хранилище текущих параметров запущенного игрового уровня: координаты
    финишной ячейки, координаты игрока, координаты преследователей,
    игровое поле.
    """
    
    #     -2 -1  0  1  2  3  -> x (col)
    #     __          __
    #    /  \__ ..   /  \__ 
    #-1  \__/  \__ ..\__/  \
    #    /  \__/  \__ ..\__/
    # 0  \__/..\__/  \__ .. 
    #     ..   /  \__/  \__ 
    # 1   __ ..\__/  \__/  \
    #    /  \__/  \__/  \__/
    # 2  \__/  \__/  \__/  \
    #       \__/  \__/  \__/
    # |
    # v
    #
    # y (row)
    
    def __init__(self):
        
        self._min_col = 0
        self._max_col = 0
        self._min_row = 0
        self._max_row = 0
        self._field = {}
        self._creatures = defaultdict(list)
        self._cell2creatures = defaultdict(set)
        self._edgemem = defaultdict(int)
        self.finish_col = 0
        self.finish_row = 0
    
    def set_impassability_for(self, col, row, impassability):
        
        cell = self.cell(col, row)
        
        if not cell:
            return
        
        for side, closed in zip(grid.SIDES, impassability):
            ncol, nrow, backside = grid.neighbor(col, row, side)
            neighbor = self.cell(ncol, nrow)
            if closed:
                grid.close_edge(col, row, side, oneway=True)
            else:
                grid.open_edge(col, row, side, oneway=True)
            if neighbor:
                if grid.edge_passable(col, row, ncol, nrow):
                    setattr(cell, side, neighbor)
                    setattr(neighbor, backside, cell)
                else:
                    setattr(cell, side, None)
                    setattr(neighbor, backside, None)
    
    def add_cell(self, col, row):
        
        cell = CellData(col, row)
        self._field[col, row] = cell
        
        self._min_col = min(self._min_col, col)
        self._max_col = max(self._max_col, col)
        self._min_row = min(self._min_row, row)
        self._max_row = max(self._max_row, row)
        
        impassability = (False, False, False, False, False, False)
        self.set_impassability_for(col, row, impassability)
        
        return cell
    
    def del_cell(self, col, row):
        
        impassability = (True, True, True, True, True, True)
        self.set_impassability_for(col, row, impassability)
        
        cell = self._field.pop((col, row), None)
        del cell
    
    def cell(self, col, row):
        
        return self._field.get((col, row))
    
    def add_creature(self, col, row, role):
        
        if (col, row) not in self._field:
            return None
        
        creature = CreatureData(cell=self._field[col, row], role=role)
        self._creatures[creature.role].append(creature)
        self._cell2creatures[creature.cell].add(creature)
        
        return creature
    
    def del_creature(self, creature):
        
        self._cell2creatures[creature.cell].discard(creature)
        candidates = self._creatures[creature.role]
        try:
            candidates.remove(creature)
            creature.cell = None
        except ValueError:
            pass
    
    def creatures(self, role):
        
        return self._creatures[role]
    
    def clear(self):
        """Полная очистка данных.
        """
        
        self._min_col = 0
        self._max_col = 0
        self._min_row = 0
        self._max_row = 0
        self._field.clear()
        self._creatures.clear()
        self._cell2creatures.clear()
        self._edgemem.clear()
        self.finish_col = 0
        self.finish_row = 0
        grid.clear()
    
    def is_occupied(self, cell):
        
        return len(self._cell2creatures[cell]) > 0
    
    def update_occupation(self, cell, creature):
        
        self._cell2creatures[creature.cell].discard(creature)
        creature.cell = cell
        self._cell2creatures[creature.cell].add(creature)
    
    @property
    def cols(self):        
        """Количество столбцов у игрового поля. Так как расстановка
        ячеек свободная, то результат вычисляется как разность между
        максимальным номером столбца и минимальным плюс единица.
        """
        
        return self._max_col - self._min_col + 1
    
    @property
    def rows(self):
        """Количество столбцов у игрового поля. Так как расстановка
        ячеек свободная, то результат вычисляется как разность между
        максимальным номером столбца и минимальным плюс единица.
        """
        
        return self._max_row - self._min_row + 1
    
    @property
    def souls(self):
        """Количество существ на игровом поле, в том числе игрок.
        """
        
        s = 0
        for value in self._creatures.viewvalues():
            s += len(value)
        
        return s


class EventData(object):
    """
    Событие ожидаемое или произошедшее. Описывает ситуацию на игровом
    поле в динамике.
    """
    
    MOVE_EVENT = 1
    CRASH_EVENT = 2
    PLAYER_WIN_EVENT = 3
    PLAYER_LOOSE_EVENT = 4
    
    def __init__(self, event=None, who=None, data=None):
        """
        event - тип события
        who   - ссылка на экземпляр CreatureData, для которого событие
                предназначено
        data  - данные, описывающие событие
        
               event       |                   data
        -------------------+--------------------------------------------
        MOVE_EVENT         | [current_cell, new_cell]
        CRASH_EVENT        | None
        PLAYER_WIN_EVENT   | None
        PLAYER_LOOSE_EVENT | None
        """
        
        if not isinstance(event, (int, long)):
            raise TypeError(
                "param 'event' must be an integer"
            )
        
        if not isinstance(who, CreatureData):
            raise TypeError(
                "param 'who' must be an instance of class CreatureData"
            )
        
        self.event = event
        self.who = who
        self.data = data
