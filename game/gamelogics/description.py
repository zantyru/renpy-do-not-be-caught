# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import json
import zlib
from collections import namedtuple


"""Описание игрового уровня. По нему строится местность, размещаются
преследователи и игрок, задаётся проходимость ячеек и их внешний вид."""


CreatureDescription = namedtuple(
    "CreatureDescription",
    "role image_filename start_col start_row"
)

CellDescription = namedtuple(
    "CellDescription",
    "col, row, image_filename"
)

CellImpassability = namedtuple(
    "CellImpassability",
    "top topright bottomright bottom bottomleft topleft"
)


class LevelDescription(object):
    
    def __init__(self):
        
        self.finish_col = None
        self.finish_row = None
        self._creatures = {}
        self._cells = {}
        self._impassability = {}
    
    def save(self, filepathname):
        """
        Запись сведений об уровне в файл. Исключения должен обрабатывать
        сам пользователь.
        """
        
        dirpath = os.path.dirname(filepathname)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath)
        
        j = json.dumps((
            self.finish_col,
            self.finish_row,
            self._creatures.values(),
            self._cells.values(),
            self._impassability.items()
        ))
        
        with open(filepathname, "wb") as f:
            f.write(j.encode("utf-8").encode("zlib"))
    
    def load(self, filepathname):
        """
        Загрузка сведений об уровне из файла. Исключения должен
        обрабатывать сам пользователь.
        """
        
        #@FIXIT Данная реализация не позволяет загружать файл
        # из rpa-архива. Решение есть, но зависимость от Ren'Py не надо
        # созавать здесь, внутри.
        
        j = None
        
        with open(filepathname, "rb") as f:
            j = json.loads(f.read().decode("zlib").decode("utf-8"))
        
        self._creatures.clear()
        self._cells.clear()
        self._impassability.clear()
        
        finish_col, finish_row, creatures, cells, impassability = j
        
        def iter_creatures():
            for obj in creatures:
                value = CreatureDescription(*obj)
                key = (value.start_col, value.start_row)
                yield (key, value)
        
        def iter_cells():
            for obj in cells:
                value = CellDescription(*obj)
                key = (value.col, value.row)
                yield (key, value)
        
        def iter_impassability():
            for obj in impassability:
                key_raw, value_raw = obj
                yield (tuple(key_raw), CellImpassability(*value_raw))
        
        self.finish_col = finish_col
        self.finish_row = finish_row
        self._creatures = dict(iter_creatures())
        self._cells = dict(iter_cells())
        self._impassability = dict(iter_impassability())
    
    def add_creature_description(self, role, image_filename, start_col,
    start_row):
        
        self._creatures[start_col, start_row] = CreatureDescription(
            role, image_filename, start_col, start_row
        )
    
    def del_creature_description(self, col, row):
        
        del self._creatures[col, row]
    
    def iter_creature_descriptions(self):
        
        return iter(self._creatures.viewvalues())
    
    def clear_creature_descriptions(self):
        
        self._creatures.clear()
    
    def add_cell_description(self, col, row, image_filename):
        
        self._cells[col, row] = CellDescription(col, row, image_filename)
    
    def del_cell_description(self, col, row):
        
        self.set_impassability_for(col, row,
            (False, False, False, False, False, False)
        )
        del self._cells[col, row]
    
    def get_cell_description(self, col, row):
        
        return self._cells.get((col, row))
    
    def iter_cell_descriptions(self):
        
        return iter(self._cells.viewvalues())
    
    def clear_cell_descriptions(self):
        
        self._cells.clear()
        self._impassability.clear()
    
    def set_impassability_for(self, col, row, impassability):
        
        if any(impassability):
            self._impassability[col, row] = \
                CellImpassability(*impassability)
        else:
            self._impassability.pop((col, row), None)
    
    def get_impassability_for(self, col, row):
        
        data = self._impassability.get((col, row))
        if not data:
            data = (False, False, False, False, False, False)
        return data
