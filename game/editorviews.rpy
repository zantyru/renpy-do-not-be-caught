init offset = 1
init python:
    
    from __future__ import division
    import os
    import math
    import json
    from itertools import product
    from collections import defaultdict, namedtuple
    import pygame
    from renpy.exports import Displayable, Render
    import gamelogics as galo
    from clusterizer import CluSterizer, CluBox
    from animation import Animachine
    
    
    if not os.path.exists(LEVELS_DIRECTORY):
        os.makedirs(LEVELS_DIRECTORY)
    
    
    IMAGEOBJ_BACKGROUNDHEX = Image("images/editor/bg.png")
    
    LevelCreatureBrush = namedtuple(
        "LevelCreatureBrush",
        "role image_filename"
    )
    
    LevelCellBrush = namedtuple(
        "LevelCellBrush",
        "image_filename top topright bottomright bottom bottomleft topleft"
    )
    
    
    def _brushes(path, containerclass):
        rv = []
        files = iter_files(path, ".json")
        for f in files:
            j = None
            fullpath = "{}/{}".format(path, f)
            with renpy.file(renpy.fsencode(fullpath)) as data:
                j = json.loads(data.read().decode("utf-8"))
            rv.append(containerclass(*j))
        return rv
    cellbrushes = _brushes(CELLBRUSHES_DIR, LevelCellBrush)
    creaturebrushes = _brushes(CREATUREBRUSHES_DIR, LevelCreatureBrush)
    
    #@HARDCODE for 'finish' marker
    creaturebrushes.insert(
        0, 
        LevelCreatureBrush("finish", "images/editor/finish.png")
    )
    
    
    class LevelEditorDisplayable(Displayable): #@SMELL
        """
        Графическое представление игрового уровня и взаимодействие
        с пользователем.
        """
        
        CAMERA_VELOCITY = 400 # pixels per sec
        
        def __init__(self, **properties):
            
            super(LevelEditorDisplayable, self).__init__(**properties)
            
            self.controls = KeyboardMouseState()
            
            self.camera_expect_up = False
            self.camera_expect_down = False
            self.camera_expect_left = False
            self.camera_expect_right = False
            
            self._shortcut4displayables = {} #dict<XData:XDisplayable>
            self._shortcut4creatures = {} #dict<(col, row):CreatureData>
            
            # For CluSterizer, и виртуальаня камера
            self.box = CluBox(x=0, y=0, width=0, height=0)
            self.clusterizer = CluSterizer()
            
            # Сборка данных. Сцепление с элементами UI
            self.level = galo.LevelData()
            self.level_description = galo.LevelDescription()
            
            # Инструменты редактирования
            self.brushmode = BRUSHMODE_CELL
            self.brush = None
            
            # Анимации
            self.animation = Animachine()
            
            def anim_camera(dt, *args):
                up, down, left, right = args
                dxcam = 0.0
                dycam = 0.0
                if up:
                    dycam -= 1.0
                if down:
                    dycam += 1.0
                if left:
                    dxcam -= 1.0
                if right:
                    dxcam += 1.0
                hypotcam = math.hypot(dxcam, dycam)
                if hypotcam > EPS:
                    self.box.x += dt * self.CAMERA_VELOCITY * dxcam / hypotcam
                    self.box.y += dt * self.CAMERA_VELOCITY * dycam / hypotcam
                return None
            
            self.animation.register("camera", anim_camera)
        
        def setup_brush(self, mode, brush):
            
            self.brushmode = mode
            self.brush = brush
        
        def save(self, filepathname):
            
            filepathname = renpy.fsencode("{}/{}/{}".format(
                config.gamedir, LEVELS_DIRECTORY, filepathname
            ))
            self.level_description.save(filepathname)
        
        def load(self, filepathname):
            
            self.clear_and_start_from_scratch()
            
            filepathname = renpy.fsencode("{}/{}/{}".format(
                config.gamedir, LEVELS_DIRECTORY, filepathname
            ))
            self.level_description.load(filepathname)
            
            self.level.finish_col = self.level_description.finish_col
            self.level.finish_row = self.level_description.finish_row
            
            for c in self.level_description.iter_cell_descriptions():
                col = c.col
                row = c.row
                cell = self.level.add_cell(col, row)
                impassability = self.level_description.get_impassability_for(col, row)
                self.level.set_impassability_for(col, row, impassability)
                cell_image = Image(c.image_filename)
                obj = CellDisplayable(cell, cell_image)
                obj.box.x, obj.box.y = colrow2world(col, row)
                self.clusterizer.register(obj, obj.box)
                # shortcut
                self._shortcut4displayables[cell] = obj
            
            for c in self.level_description.iter_creature_descriptions():
                col = c.start_col
                row = c.start_row
                creature = self.level.add_creature(col, row, c.role)
                creature_image = Image(c.image_filename)
                obj = CreatureDisplayable(creature, creature_image)
                obj.box.x, obj.box.y = colrow2world(col, row)
                self.clusterizer.register(obj, obj.box)
                # shortcut
                self._shortcut4displayables[creature] = obj
                self._shortcut4creatures[col, row] = creature
            
            # "Finish" marker  #@SMELL
            col = self.level.finish_col
            row = self.level.finish_row
            if self.level.cell(col, row) is not None:
                creature = self.level.add_creature(col, row, "finish") #@HARDCODE #@DUPLICATE
                creature_image = Image("images/editor/finish.png") #@HARDCODE #@DUPLICATE
                obj = CreatureDisplayable(creature, creature_image)
                obj.box.x, obj.box.y = colrow2world(col, row)
                self.clusterizer.register(obj, obj.box)
                # shortcut
                self._shortcut4displayables[creature] = obj
                self._shortcut4creatures[col, row] = creature
        
        def clear_and_start_from_scratch(self):
            """
            Очистка уровня и начало заново.
            """
            
            self._shortcut4displayables.clear()
            for obj in self.clusterizer.objs():
                self.clusterizer.release(obj)
            self.level.clear()
            self.level_description.clear_creature_descriptions()
            self.level_description.clear_cell_descriptions()
            self.box.x = 0
            self.box.y = 0
            renpy.redraw(self, 0)
        
        def render_hex_grid(self, renderer):
            
            left_col, top_row = world2colrow(
                self.box.x - self.box.halfwidth,
                self.box.y - self.box.halfheight
            )
            
            right_col, bottom_row = world2colrow(
                self.box.x + self.box.halfwidth,
                self.box.y + self.box.halfheight
            )
            
            colrow = product(
                xrange(left_col - 1, right_col + 2),
                xrange(top_row - 1, bottom_row + 2)
            )
            
            for col, row in colrow:
                wx, wy = colrow2world(col, row)
                sx, sy = world2screen(wx, wy, self.box)
                renderer.place(
                    IMAGEOBJ_BACKGROUNDHEX,
                    sx - IMAGE_CELL_HALFWIDTH,
                    sy - IMAGE_CELL_HALFHEIGHT
                )
        
        def render(self, width, height, st, at):
            
            # Cache
            _ld = self.level
            cols = _ld.cols
            rows = _ld.rows
            
            ## Calculations ##
            
            # Движение камеры
            directions = (
                self.camera_expect_up, self.camera_expect_down,
                self.camera_expect_left, self.camera_expect_right
            )
            if any(directions):
                self.animation.plan_job("camera", directions)
            
            if self.animation.animate(st):
                renpy.redraw(self, 0)
            
            ## Visualization ##
            
            self.box.width = width
            self.box.height = height
            
            w = width
            h = height
            
            renderer = Render(w, h)
            
            renderer.place(Solid("#23d8ec"), 0, 0) #@DEBUG фон
            self.render_hex_grid(renderer)
            
            # Рисуем то, что попадает в кадр
            visible_objects = self.clusterizer.select(self.box)
            layer2 = []
            for vo in visible_objects:
                if isinstance(vo, CreatureDisplayable):
                    layer2.append(vo)
                    continue
                vo_scr_x, vo_scr_y = world2screen(vo.box.x, vo.box.y, self.box) #@SMELL
                renderer.place(vo, vo_scr_x - vo.box.halfwidth, vo_scr_y - vo.box.halfheight)
            for vo in layer2:
                vo_scr_x, vo_scr_y = world2screen(vo.box.x, vo.box.y, self.box) #@SMELL
                renderer.place(vo, vo_scr_x - vo.box.halfwidth, vo_scr_y - vo.box.halfheight)
            
            return renderer.subsurface((0, 0, w, h))
        
        def event(self, ev, x, y, st):
            
            con = self.controls
            con.update(ev, x, y)
            need_redraw = False
            
            if 0 <= x < self.box.width and 0 <= y < self.box.height:
                
                wx, wy = screen2world(x, y, self.box)
                col, row = world2colrow(wx, wy)
                cell = self.level.cell(col, row)
            
                if con.mkey_had_click(M_BUTTON1): # and not(con.mmods & MMOD_DROP):
                    
                    if self.brush is None:
                        
                        renpy.notify(_("Не выбрана кисть."))
                    
                    elif self.brushmode == BRUSHMODE_CELL and cell is None:
                    
                        cell = self.level.add_cell(col, row)
                        
                        obj = CellDisplayable(
                            cell,
                            Image(self.brush.image_filename)
                        )
                        obj.box.x, obj.box.y = colrow2world(col, row)
                        
                        self._shortcut4displayables[cell] = obj
                        self.clusterizer.register(obj, obj.box)
                        
                        self.level_description.add_cell_description(
                            col, row,
                            self.brush.image_filename
                        )
                        self.level_description.set_impassability_for(
                            col, row, (
                                self.brush.top,
                                self.brush.topright,
                                self.brush.bottomright,
                                self.brush.bottom,
                                self.brush.bottomleft,
                                self.brush.topleft
                            )
                        )
                    
                        need_redraw = True
                    
                    elif self.brushmode == BRUSHMODE_OBJECT and cell is not None:
                    
                        cre = self._shortcut4creatures.get((col, row))
                        
                        if cre is None:
                            
                            cre = self.level.add_creature(
                                col, row,
                                self.brush.role
                            )
                            
                            obj = CreatureDisplayable(
                                cre,
                                Image(self.brush.image_filename)
                            )
                            obj.box.x, obj.box.y = colrow2world(col, row)
                            
                            self._shortcut4displayables[cre] = obj
                            self._shortcut4creatures[col, row] = cre
                            self.clusterizer.register(obj, obj.box)
                            
                            if self.brush.role == "finish":
                                
                                _col = self.level_description.finish_col
                                _row = self.level_description.finish_row
                                
                                try: #@DUPLICATE
                                    _cre = self._shortcut4creatures.pop((_col, _row))
                                    _obj = self._shortcut4displayables.pop(_cre)
                                    self.clusterizer.release(_obj)
                                    self.level.del_creature(_cre)
                                    #if cre.role == "finish":
                                    #    self.level.finish_col = 0
                                    #    self.level.finish_row = 0
                                    #    self.level_description.finish_col = 0
                                    #    self.level_description.finish_row = 0
                                    #else:
                                    #    self.level_description.del_creature_description(_col, _row)
                                    del _obj
                                    del _cre
                                except KeyError:
                                    pass
                                
                                self.level.finish_col = col
                                self.level.finish_row = row
                                self.level_description.finish_col = col
                                self.level_description.finish_row = row
                            else:
                                self.level_description.add_creature_description(
                                    self.brush.role,
                                    self.brush.image_filename,
                                    col, row
                                )
                            
                            need_redraw = True
                    
                elif con.mkey_had_click(M_BUTTON3):
                    
                    if self.brushmode == BRUSHMODE_CELL and cell is not None:
                        
                        obj = self._shortcut4displayables.pop(cell)
                        self.clusterizer.release(obj)
                        self.level.del_cell(col, row)
                        del obj
                        del cell
                        self.level_description.del_cell_description(col, row)
                        
                        try:
                            cre = self._shortcut4creatures.pop((col, row))
                            obj = self._shortcut4displayables.pop(cre)
                            self.clusterizer.release(obj)
                            self.level.del_creature(cre)
                            if cre.role == "finish":
                                self.level.finish_col = 0
                                self.level.finish_row = 0
                                self.level_description.finish_col = 0
                                self.level_description.finish_row = 0
                            else:
                                self.level_description.del_creature_description(col, row)
                            del obj
                            del cre
                        except KeyError:
                            pass
                        
                        need_redraw = True
                    
                    if self.brushmode == BRUSHMODE_OBJECT:
                        
                        try:
                            cre = self._shortcut4creatures.pop((col, row))
                            obj = self._shortcut4displayables.pop(cre)
                            self.clusterizer.release(obj)
                            self.level.del_creature(cre)
                            self.level_description.del_creature_description(col, row)
                            del obj
                            del cre
                        except KeyError:
                            pass
                        
                        need_redraw = True
            
            #if con.mmods & MMOD_DRAG:
            #    self.camera_expect_up = con.mouse_dy < 0.0
            #    self.camera_expect_down = con.mouse_dy > 0.0
            #    self.camera_expect_left = con.mouse_dx < 0.0
            #    self.camera_expect_right = con.mouse_dx > 0.0
            #else:
            #    self.camera_expect_up = False
            #    self.camera_expect_down = False
            #    self.camera_expect_left = False
            #    self.camera_expect_right = False
            
            self.camera_expect_up = con.kkey_is_pressed(pygame.K_UP)
            self.camera_expect_down = con.kkey_is_pressed(pygame.K_DOWN)
            self.camera_expect_left = con.kkey_is_pressed(pygame.K_LEFT)
            self.camera_expect_right = con.kkey_is_pressed(pygame.K_RIGHT)
            
            need_redraw = need_redraw or \
                self.camera_expect_up or \
                self.camera_expect_down or \
                self.camera_expect_left or \
                self.camera_expect_right
            
            if need_redraw:
                renpy.redraw(self, 0)
        
        def visit(self):
            
            return []
