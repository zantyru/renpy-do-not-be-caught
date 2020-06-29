init offset = 0
init python:
    
    import os
    import gamelogics as galo
    
    
    # Общие функции ####################################################
    
    # Перевод координат
    def world2colrow(x, y):
        """
        Перевод мировых координат точки в строково-колоночный адрес
        шестиугольной ячейки, которой принадлежит эта точка.
        """
        
        #      W        :W      |   :  W        :W          :  W 
        #  . . .WWWWWWWWW. . . .|. .:. .WWWWWWWWW. . . . . .:. .WWW. .
        #      W        :W      |   :  W        :W          :  W 
        #               : W     |   : W         : W         : W  
        #               :  W    |   :W          :  W        :W   
        #  . . . . . . .o. .WWWWWWWWW. . . . . .:. .WWWWWWWWW. . . . .
        #               :`,W    |   :W          :  W        :W   
        #               : W`,   |   : W         : W         : W  
        #      W        :W   `, |   :  W        :W          :  W 
        #  -----W-W-W-W-W------`+-------W-W-W-W-W---------------W-W--X
        #      W        :W     0|   :  W        :W          :  W 
        #               : W     |   : W         : W         : W  
        #               :  W    |   :W          :  W        :W   
        #  . . . . . . .:. .WWWWWWWWW. . . . . .:. .WWWWWWWWW. . . . .
        #               :  W    |   :W          :  W        :W   
        #               : W     |   : W         : W         : W  
        #      W        :W      |   :  W        :W          :  W 
        #  . . .WWWWWWWWW       |   :   WWWWWWWWW. . . . . .:. .WWW. .
        #      W        :W      |   :  W        :W          :  W 
        #                       Y
        
        x += IMAGE_CELL_HALFWIDTH
        y += IMAGE_CELL_HALFHEIGHT
        
        colsize = IMAGE_CELL_WIDTH - OVERLAPW
        rowsize = IMAGE_CELL_HEIGHT
        
        col, offsetu = divmod(x, colsize)
        row, offsetv = divmod(y - (col % 2) * OVERLAPH, rowsize)
        
        col, row = int(col), int(row)
        
        # Решаем "наклонности"
        if offsetu < OVERLAPW:
            
            #    |  '      '          o   |  'o     '
            # ---+--WWWWWWWw--U        o  +--WWWWWWWw
            #    | W'      '            o | W'      '
            #    |W '      '             o|W '      '
            #    W  '      '     ==>   ---W--+------+--U
            #    |W '      '             o|W '      '
            #    | W'      '            o | W'      '
            #    +--WWWWWWWw           o  +--WWWWWWWw
            #    |  '      '          o   |  'o     '
            #    V                        V
            
            offsetv -= OVERLAPH
            v = OVERKOEF * offsetu
            
            if offsetv > v:
                
                row += col % 2
                col -= 1
            
            elif offsetv < -v:
                
                row += col % 2 - 1
                col -= 1
        
        return col, row
    
    def colrow2world(col, row):
        """
        Перевод адреса шестиугольной ячейки в мировые координаты
        её центра.
        """
        
        x = col * (IMAGE_CELL_WIDTH - OVERLAPW)
        y = row * IMAGE_CELL_HEIGHT + OVERLAPH * (col % 2)
        return x, y
    
    def screen2world(x, y, clubox):
            
        wx = x + clubox.x - clubox.halfwidth
        wy = y + clubox.y - clubox.halfheight
        return wx, wy
    
    def world2screen(x, y, clubox):
        
        sx = x - clubox.x + clubox.halfwidth
        sy = y - clubox.y + clubox.halfheight
        return sx, sy
    
    # Математика на шестиугольной сетке
    def hex_distance(cell1, cell2):
        """
        Вычисляет расстояние между ячейками на сетке из шестиугольников.
        """
        c1, r1 = cell1.col, cell1.row
        c2, r2 = cell2.col, cell2.row
        dx = abs(c2 - c1)
        dy = abs(r2 - r1)
        dd = abs(dy - dx)
        k = 0
        if dx != 0:
            if c1 % 2 == 0 and r2 > r1:
                k = 1
            elif c2 % 2 == 0 and r1 > r2:
                k = 1
        return max(dx, dy + k, dd)
    
    # Файлы и директории
    def iter_files(path, ext):
        if ext[0] != ".":
            ext = ".{}".format(ext)
        if path[-1] != "/":
            path = "{}/".format(path)
        files = renpy.list_files() # Cписок, не итератор :(        
        for f in sorted(files):
            if not (f.startswith(path) and f.endswith(ext)):
                continue
            yield f.partition(path)[2] #@MAGICNUMBER
    
    # Обработка данных
    def description2level(dscdata):
        
        lvldata = galo.LevelData()
        
        lvldata.finish_col = dscdata.finish_col
        lvldata.finish_row = dscdata.finish_row
        
        for c in dscdata.iter_cell_descriptions():
            col = c.col
            row = c.row
            cell = lvldata.add_cell(col, row)
            impassability = dscdata.get_impassability_for(col, row)
            lvldata.set_impassability_for(col, row, impassability)
        
        for c in dscdata.iter_creature_descriptions():
            col = c.start_col
            row = c.start_row
            creature = lvldata.add_creature(col, row, c.role)
        
        return lvldata
