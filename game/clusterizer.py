# -*- coding: utf-8 -*-

from __future__ import division, print_function
from itertools import product
from collections import defaultdict
import math


class CluBox(object):
    """
    Паспорт контейнера для CluSterizer.
    Содержит информацию о координатах точки привязки 'x' и 'y',
    размере ограничивающего прямоугольника и его полуразмерах.
    В качестве точки привязки контейнера рассматривается середина
    ограничивающего прямоугольника.
    
    +---------------+
    |               |
    |       @       |
    |               |
    +---------------+
    
    """
    
    __slots__ = (
        "x", "y", "__width", "__height", "__halfwidth", "__halfheight"
    )
    
    __hash__ = None
    
    def __init__(self, x=0, y=0, width=0, height=0):
        
        self.x = float(x)
        self.y = float(y)
        self.__width = float(width)
        self.__height = float(height)
        self.__halfwidth = self.__width / 2.0
        self.__halfheight = self.__height / 2.0
    
    @property
    def width(self):
        
        return self.__width
    
    @width.setter
    def width(self, value):
        
        self.__width = float(value)
        self.__halfwidth = self.__width / 2.0
    
    @property
    def height(self):
        
        return self.__height
    
    @height.setter
    def height(self, value):
        
        self.__height = float(value)
        self.__halfheight = self.__height / 2.0
    
    @property
    def halfwidth(self):
        
        return self.__halfwidth
    
    @property
    def halfheight(self):
        
        return self.__halfheight


class CluSterizer(object):
    """
    Хранилище двумерных объектов, использующее разбиение пространства
    на кластеры (сетку).
    """
    
    DEFAULT_CLUSTER_SIZE = 1000.0
    
    def __init__(self, cluster_size=None):
        
        self._step = abs(
            float(cluster_size or self.DEFAULT_CLUSTER_SIZE)
        )
        self._inv_step = 1.0 / self._step
        self.clusters = defaultdict(set) # dict<(int, int): set>
        self.objects = {} # dict<object: (int, int)>
    
    @property
    def cluster_size(self):
        
        return self._step
    
    def objs(self):
        
        return self.objects.keys()
    
    def _diapason(self, clubox):
        
        x = clubox.x
        y = clubox.y
        hw = clubox.halfwidth
        hh = clubox.halfheight
        min_x = int(math.floor((x - hw) * self._inv_step))
        min_y = int(math.floor((y - hh) * self._inv_step))
        max_x = int(math.floor((x + hw) * self._inv_step))
        max_y = int(math.floor((y + hh) * self._inv_step))
        pairs = product(
            xrange(min_x, max_x + 1),
            xrange(min_y, max_y + 1)
        )
        for pair in pairs:
            yield pair
    
    def register(self, obj, clubox):
        
        if not isinstance(clubox, CluBox):
            raise TypeError(
                "second param must ba an instance of CluBox class"
            )
        
        obj.box = clubox
        occuped_clusters = tuple(self._diapason(obj.box))
        
        if obj in self.objects:
            self.release(obj)
        
        for ixiy in occuped_clusters:
            self.clusters[ixiy].add(obj)
        self.objects[obj] = occuped_clusters
    
    def release(self, obj):
        
        occuped_clusters = self.objects[obj]
        del self.objects[obj]
        for ixiy in occuped_clusters:
            self.clusters[ixiy].discard(obj)
    
    def select(self, clubox):
        
        # Сбор *всех* объектов из затронутых кластеров в одно множество
        objs = set()
        map(
            objs.update,
            (self.clusters[c] for c in self._diapason(clubox))
        )
        
        # Выборка объектов, точно затронутых выделением
        def intersect(Apx, Apy, Ahw, Ahh, Bpx, Bpy, Bhw, Bhh):
            hsum_x = Ahw + Bhw
            hsum_y = Ahh + Bhh
            pdif_x = Bpx - Apx
            pdif_y = Bpy - Apy
            return abs(pdif_x) < hsum_x and abs(pdif_y) < hsum_y
        
        result = (
            o
            for o in objs
            if intersect(
                o.box.x, o.box.y,
                o.box.halfwidth, o.box.halfheight,
                clubox.x, clubox.y,
                clubox.halfwidth, clubox.halfheight
            )
        )
        
        return result
