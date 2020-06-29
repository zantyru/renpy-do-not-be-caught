# -*- coding: utf-8 -*-

from operator import attrgetter
from itertools import chain
from collections import defaultdict
from .data import CellData, CreatureData, LevelData, EventData
import grid


"""Обработка игровой ситуации по правилам ("передвижка" фигурок,
обработка столкновений (занятие одной ячейки), проверка наступления
условий проигрыша и выигрыша)."""


class _triplet(object):
    
    __slots__ = ("players", "stupids", "clevers")
    
    def __init__(self):
        
        self.players = []
        self.stupids = []
        self.clevers = []
    
    def __iter__(self):
        
        yield self.players
        yield self.stupids
        yield self.clevers


def calculate_distance(level=None):
    """
    Рассчёт для каждой ячейки игрового поля удалённости от игрока.
    Ячейка, в которой стоит игрок, будет содержать ноль, соседние
    доступные - на единицу больше - и так далее.
    """
    
    neighbors = CellData.not_none_neighbors
    
    players = level.creatures(CreatureData.PLAYER)
    
    curr_cells = set((player.cell for player in players))
    next_cells = set()
    computed_cells = set()
    distance = 0
    
    while curr_cells or next_cells:
        while curr_cells:
            c = curr_cells.pop()
            c.distance = distance
            computed_cells.add(c)
            for n in neighbors(c):
                if n not in computed_cells and n not in curr_cells:
                    next_cells.add(n)
        distance += 1
        curr_cells, next_cells = next_cells, curr_cells


def do_computer_turn(level=None):
    """
    Рассчёт потенциально возможного хода противника. В результате
    возвращается список *ожидаемых* событий для каждого из
    преследователей.
    """
    
    # Сначала рассчитываем для каждой ячейки игрового поля
    # удалённость от игрока. Ячейка, в которой стоит игрок, будет
    # содержать ноль, соседние доступные - на единицу больше и так
    # далее.
    calculate_distance(level=level)
    
    # Теперь каждый преследователь должен выбрать из соседних ячеек
    # ячейку с минимальным значением параметра distance.
    expected_events = []
    neighbors = CellData.not_none_neighbors
    
    def best_next_cell(cell):
        min_distance = cell.distance
        min_direction = None
        for n in neighbors(cell):
            if n.distance < min_distance:
                min_distance = n.distance
                min_direction = n
        return min_direction
    
    pursuers = chain(
        level.creatures(CreatureData.STUPID_PURSUER),
        level.creatures(CreatureData.CLEVER_PURSUER)
    )
    for p in pursuers:
        c = best_next_cell(p.cell)
        expected_events.append(EventData(
            event=EventData.MOVE_EVENT,
            who=p,
            data=(p.cell, c) if c is not None else (p.cell, p.cell)
        ))
    
    #@NOTE Различие в поведении задаётся не здесь, а в 'process'
    
    return expected_events


def process(level=None, expected_events=None):
    """
    Применение всех событий из списка expected_events. На выходе
    получается список событий из тех, что успешно произошли, и из
    вновь добавленных в ходе обработки. 
    """
    
    if not isinstance(level, LevelData):
        raise TypeError(
            "param 'level' must be an instance of class LevelData"
        )
    
    if not hasattr(expected_events, "__iter__"):
        raise TypeError(
            "param 'expected_events' must be iterable"
        )
    
    expected_cells = defaultdict(set)
    happened_events = []
    happened_cells = set()
    
    # Регистрация ожидаемых перемещений и проверка возможности хода игрока
    all_right = True
    for e in expected_events:
        if e.event == EventData.MOVE_EVENT:
            if e.who.role == CreatureData.PLAYER:
                colA = e.data[0].col
                rowA = e.data[0].row
                colB = e.data[1].col
                rowB = e.data[1].row
                if not grid.edge_passable(colA, rowA, colB, rowB):
                    all_right = False
                    break
            expected_cells[e.data[1]].add(e.who) #@MAGICNUMBER 1 --> новая ячейка
    
    # Если игрок не может двигаться, то все стоят
    if not all_right:
        return []
    
    # Полезные операции
    def make_move(creature, destination_cell):
        happened_events.append(EventData(
            event=EventData.MOVE_EVENT,
            who=creature,
            data=(creature.cell, destination_cell)
        ))
        if creature.role != CreatureData.PLAYER:
            happened_cells.add(destination_cell)
        creature.cell = destination_cell
    
    def get_another_cell_for(creature):
        source_cell = creature.cell
        destination_cell = None
        best_distance = None
        for cell in CellData.not_none_neighbors(source_cell):
            if cell in happened_cells or cell in expected_cells:
                continue
            if best_distance is None or cell.distance < best_distance:
                best_distance = cell.distance
                destination_cell = cell
        return destination_cell or creature.cell
    
    # Вся обработка здесь
    sorted_cellkeys = sorted(
        expected_cells.iterkeys(),
        key=attrgetter("distance")
    )
    
    for cellkey in sorted_cellkeys:
        
        creatures = expected_cells[cellkey]
        creatures_count = len(creatures)
        
        if creatures_count == 1:
            
            creature, = creatures # запятая нужна
            make_move(creature, cellkey)
            expr = creature.role == CreatureData.PLAYER and \
                   cellkey.col == level.finish_col and \
                   cellkey.row == level.finish_row
            if expr:
                happened_events.append(EventData(  
                    event=EventData.PLAYER_WIN_EVENT,
                    who=creature
                ))
        
        elif creatures_count == 2:
            
            creature1, creature2 = creatures
            if creature1.role != CreatureData.PLAYER:
                creature1, creature2 = creature2, creature1
            
            if creature1.role == CreatureData.PLAYER:
                make_move(creature1, cellkey)
                make_move(creature2, cellkey)
                happened_events.append(EventData(  
                    event=EventData.PLAYER_LOOSE_EVENT,
                    who=creature1
                ))
            
            elif creature1.role == CreatureData.STUPID_PURSUER:
                make_move(creature1, cellkey)
                if creature2.role == creature1.role:
                    make_move(creature2, cellkey)
                    happened_events.append(EventData(  
                        event=EventData.CRASH_EVENT,
                        who=creature1
                    ))
                    happened_events.append(EventData(  
                        event=EventData.CRASH_EVENT,
                        who=creature2
                    ))
                else:
                    cellnew = get_another_cell_for(creature2)
                    make_move(creature2, cellnew)
            
            elif creature1.role == CreatureData.CLEVER_PURSUER:
                make_move(creature1, cellkey)
                if creature2.role == creature1.role:
                    cellnew = get_another_cell_for(creature2)
                    make_move(creature2, cellnew)
                else:
                    make_move(creature2, cellkey)
                    happened_events.append(EventData(  
                        event=EventData.CRASH_EVENT,
                        who=creature1
                    ))
                    happened_events.append(EventData(  
                        event=EventData.CRASH_EVENT,
                        who=creature2
                    ))
        
        else: #creatures_count > 2
            
            players = []
            stupids = []
            clevers = []
            
            for creature in creatures:
                if creature.role == CreatureData.CLEVER_PURSUER:
                    clevers.append(creature)
                    continue
                make_move(creature, cellkey)
                if creature.role == CreatureData.STUPID_PURSUER:
                    stupids.append(creature)
                elif creature.role == CreatureData.PLAYER:
                    players.append(creature)
            
            if not stupids: #len(stupids) == 0:
                creature = clevers.pop()
                make_move(creature, cellkey)
                for player in players:
                    happened_events.append(EventData(  
                        event=EventData.PLAYER_LOOSE_EVENT,
                        who=player
                    ))
            
            for creature in clevers:
                cellnew = get_another_cell_for(creature)
                make_move(creature, cellnew)
            
            if len(stupids) == 1:
                for player in players:
                    happened_events.append(EventData(  
                        event=EventData.PLAYER_LOOSE_EVENT,
                        who=player
                    ))
            else:
                for stupid in stupids:
                    happened_events.append(EventData(  
                        event=EventData.CRASH_EVENT,
                        who=stupid
                    ))
    
    return happened_events
