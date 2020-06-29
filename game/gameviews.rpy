init offset = 1
init python:
    
    from __future__ import division
    import math
    from itertools import product
    from collections import defaultdict
    import pygame
    from renpy.exports import Displayable, Render
    import gamelogics as galo
    from clusterizer import CluSterizer, CluBox
    from animation import Animachine
    
    
    class CellDisplayable(Displayable):
        """
        Графический интерфейс ячейки игрового поля. Отображение
        на экране и обработка взаимодействия с пользователем.
        """
        
        def __init__(self, cell, image, **properties):
            
            super(CellDisplayable, self).__init__(**properties)
            
            if not isinstance(cell, galo.CellData):
                raise TypeError(
                    "param 'cell' must be instance of class CellData"
                )
            
            self.cell = cell
            self.child = renpy.displayable(image)
            
            # For CluSterizer
            self.box = CluBox( 
                x=0, y=0,
                width=IMAGE_CELL_WIDTH, height=IMAGE_CELL_HEIGHT
            )
        
        def render(self, width, height, st, at):
            """
            Простая отрисовка изображения ячейки в заданных размерах.
            """
            
            r = renpy.render(
                self.child,
                self.box.width, self.box.height,
                st, at
            )
            return r 
        
        def event(self, ev, x, y, st):
            """
            Обработка событий взаимодействия.
            """
            
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                
                hw = self.box.halfwidth
                hh = self.box.halfheight
                
                #  Y                      Y       Я знаю, что на самом
                #  | WWWWW              WWWWW     деле ось OY направлена
                #  |W     W            W  |  W    вниз относительно
                #  W       W   ===> --W---+---W-X поверхности экрана.
                #  |W     W            W  |  W
                #--+-WWWWW---X          WWWWW
                #  |                      |
                #x -= hw   В CluBox всё центрируется автоматически.
                #y -= hh
                
                # Полуплоскости ограничивающих прямых
                #
                #                  s3              s4
                #                 .               .
                #                .               .
                #               . Y             .
                #              .  |  .         .
                #. . . . . . .WWWWWWWWW. . . ... . . s2
                #            W    |    W     .
                #       .   W     |     W   .
                #        . W      |      W .
                #      ---W-------+-------W--X
                #        . W     0|      W .
                #       .   W     |     W   .
                #            W    |    W     .
                #. . . . . . .WWWWWWWWW. . . ... . . s1
                #              .  |  .         .
                #               . |             .
                #                .               .
                #                 .               .
                #                  s5              s6
                #
                return y > -hh and \
                       y < hh and \
                       y < OVERKOEF * (x + hw) and \
                       y > OVERKOEF * (x - hw) and \
                       y > -OVERKOEF * (x + hw) and \
                       y < -OVERKOEF * (x - hw)
    
    
    class CreatureDisplayable(Displayable):
        """
        Графический интерфейс существ.
        """
        
        def __init__(self, creature, image, **properties):
            
            super(CreatureDisplayable, self).__init__(**properties)
            
            if not isinstance(creature, galo.CreatureData):
                raise TypeError(
                    "param 'creature' must be instance of "
                    "class CreatureData"
                )
            
            self.creature = creature
            self.child = renpy.displayable(image)
            
            # For CluSterizer
            self.box = CluBox( 
                x=0, y=0,
                width=CREATURE_WIDTH, height=CREATURE_HEIGHT
            )
        
        def render(self, width, height, st, at):
            """
            Простая отрисовка изображения существа в заданных размерах.
            """
            
            r = renpy.render(
                self.child,
                self.box.width, self.box.height,
                st, at
            )
            return r
        
        def event(self, ev, x, y, st):
            """
            Обработка событий взаимодействия.
            """
            
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                
                hw = self.box.halfwidth
                hh = self.box.halfheight
                
                #x -= hw   В CluBox всё центрируется автоматически.
                #y -= hh
                
                u = hw * hw
                v = hh * hh
                
                return v * x*x + u * y*y < u*v # Внутренность эллипса
    
    
    class LevelDisplayable(Displayable): #@SMELL inside
        """
        Графическое представление игрового уровня и взаимодействие
        с пользователем.
        """
        
        STATE_USER_LISTENING = 0
        STATE_MOTION_ANIMATION = 1
        STATE_MOTION_ANIMATION_TICK = 2
        STATE_PENDING_REMOVAL = 3
        STATE_WINNING = 4
        STATE_LOOSING = 5
        STATE_MAP_JUST_STARTED = 6
        
        def __init__(self, description=None, **properties):
            
            super(LevelDisplayable, self).__init__(**properties)
            
            if not isinstance(description, galo.LevelDescription):
                raise TypeError(
                    "param 'description' must be an instance "
                    "of class LevelDescription"
                )
            
            self.controls = KeyboardMouseState()
            
            self.state = self.STATE_MAP_JUST_STARTED #STATE_USER_LISTENING
            
            self.expected_events = []
            self.happened_events = []
            
            self.list_of_deleted = []
            
            self.camera_expect_up = False
            self.camera_expect_down = False
            self.camera_expect_left = False
            self.camera_expect_right = False
            self.camera_track_distance = None
            self.camera_view_distance = None
            self.camera_velocity_x = 0.0
            self.camera_velocity_y = 0.0
            self.camera_end_x = None
            self.camera_end_y = None
            
            #@MAYBE weakrefs?
            self._shortcut4displayables = {} #dict<XData:XDisplayable>
            self._shortcut4player = None
            self._shortcut4finish = None
            
            # For CluSterizer, и виртуальаня камера
            self.box = CluBox(x=0, y=0, width=0, height=0) # camera
            self.clusterizer = CluSterizer()
            
            # Состояния победы и поражения
            self._winning = False
            self._loosing = False
            self._steps = 0
            self._clear = False
            
            self._update_ingame_menu()
            
            # Сборка данных. Сцепление с элементами UI
            self.level = description2level(description)
            
            for celldesc in description.iter_cell_descriptions():
                col = celldesc.col
                row = celldesc.row
                cell = self.level.cell(col, row)
                cell_image = Image(celldesc.image_filename)
                obj = CellDisplayable(cell, cell_image)
                obj.box.x, obj.box.y = colrow2world(col, row)
                if col == self.level.finish_col and row == self.level.finish_row:
                    self._shortcut4finish = obj
                self.clusterizer.register(obj, obj.box)
                # shortcut
                self._shortcut4displayables[cell] = obj
            
            for c in description.iter_creature_descriptions():
                col = c.start_col
                row = c.start_row
                cell = self.level.cell(col, row) 
                creature = None
                for creature_ in self.level.creatures(c.role): #@SMELL architecture
                    if creature_.cell is cell:
                        creature = creature_
                        break
                creature_image = Image(c.image_filename)
                obj = CreatureDisplayable(creature, creature_image)
                obj.box.x, obj.box.y = colrow2world(col, row)
                if self._shortcut4player is None and c.role == galo.CreatureData.PLAYER:
                    self._shortcut4player = obj
                self.clusterizer.register(obj, obj.box)
                # shortcut
                self._shortcut4displayables[creature] = obj
            
            # Анимации
            self.animation = Animachine()
            
            def anim_camera(dt, *args):
                dirx, diry, vel = args
                hyp = math.hypot(dirx, diry)
                if hyp > EPS:
                    self.box.x += dt * vel * dirx / hyp
                    self.box.y += dt * vel * diry / hyp
                return None
            
            def anim_objects(dt, *args):
                obj, x, y, sx, sy, t = args
                duration = ANIMOTION_TIME
                t += dt
                if t > duration:
                    t = duration
                koef1 = (duration - t) / duration
                koef2 = math.cos(koef1 * math.pi * 0.5)
                obj.box.x = x + koef2 * sx
                obj.box.y = y + koef2 * sy
                self.clusterizer.register(obj, obj.box)
                if t < duration:
                    return obj, x, y, sx, sy, t
                return None
            
            self.animation.register("camera", anim_camera)
            self.animation.register("objects", anim_objects)
        
        def _update_ingame_menu(self):
            
            sd = renpy.get_screen("ingame_menu")
            
            if sd is None:
                return
            
            sd.scope["steps"] = self._steps
            renpy.restart_interaction()
        
        def render(self, width, height, st, at):
            
            # Cache
            _ld = self.level
            cols = _ld.cols
            rows = _ld.rows
            
            ## Setup ##
            
            self.box.width = width
            self.box.height = height
            
            w = width
            h = height
            
            if self.camera_track_distance is None:
                self.camera_track_distance = min(w, h) * 0.5 * 0.5
            if self.camera_view_distance is None:
                self.camera_view_distance = max(w, h) * 2.0
            
            ## Calculations ##
            
            # Движение камеры
            camdirx = 0.0
            camdiry = 0.0
            if self.camera_expect_up:
                camdiry -= 1.0
            if self.camera_expect_down:
                camdiry += 1.0
            if self.camera_expect_left:
                camdirx -= 1.0
            if self.camera_expect_right:
                camdirx += 1.0
            
            dx = self._shortcut4player.box.x - self.box.x
            dy = self._shortcut4player.box.y - self.box.y
            hp = math.hypot(dx, dy)
            #koef = 1.0
            if hp > self.camera_track_distance: #@FIXME
                camdirx += dx
                camdiry += dy
                #koef += math.cos(hp / self.camera_track_distance)
            
            if camdirx*camdirx + camdiry*camdiry > EPS*EPS:
                self.animation.plan_job(
                    "camera",
                    (
                        camdirx,
                        camdiry,
                        #max(koef * CAMERA_VELOCITY, CAMERA_VELOCITY_MAX)
                        CAMERA_VELOCITY
                    )
                )
            
            # Обработка состояний (и анимации)
            if self.state == self.STATE_MAP_JUST_STARTED:
                
                expr = self._shortcut4finish is not None and \
                       self._shortcut4player is not None
                
                if expr:
                    dx = self._shortcut4finish.box.x - self._shortcut4player.box.x
                    dy = self._shortcut4finish.box.y - self._shortcut4player.box.y
                    if abs(dx) < width and abs(dy) < height:
                        self.box.x = dx * 0.5 + self._shortcut4player.box.x
                        self.box.y = dy * 0.5 + self._shortcut4player.box.y
                    else:
                        self.box.x = self._shortcut4finish.box.x
                        self.box.y = self._shortcut4finish.box.y
                
                self.state = self.STATE_USER_LISTENING
                renpy.redraw(self, 0)
                
            elif self.state == self.STATE_USER_LISTENING:
                
                pass
            
            elif self.state == self.STATE_MOTION_ANIMATION:
                
                self.expected_events.extend(
                    galo.do_computer_turn(
                        level=_ld
                    )
                )
                self.happened_events.extend(
                    galo.process(
                        level=_ld,
                        expected_events=self.expected_events
                    )
                )
                self.expected_events[:] = []
                
                if not self.happened_events:
                    renpy.redraw(self, 0)
                
                while self.happened_events:
                    event = self.happened_events.pop()
                    if event.event == galo.EventData.PLAYER_LOOSE_EVENT:
                        if not self._winning:
                            self._loosing = True
                    elif event.event == galo.EventData.PLAYER_WIN_EVENT:
                        if not self._loosing:
                            self._winning = True
                    elif event.event == galo.EventData.MOVE_EVENT:
                        displ = self._shortcut4displayables[event.who]
                        curr_col = event.data[0].col #@MAGICNUMBER
                        curr_row = event.data[0].row #@MAGICNUMBER
                        next_col = event.data[1].col #@MAGICNUMBER
                        next_row = event.data[1].row #@MAGICNUMBER
                        next_x, next_y = colrow2world(next_col, next_row)
                        curr_x, curr_y = colrow2world(curr_col, curr_row)
                        vec_x, vec_y = next_x - curr_x, next_y - curr_y
                        anim_args = (
                            displ, # animated object
                            displ.box.x, displ.box.y, # start position
                            vec_x, vec_y, # translation
                            0.0 # animation timeline
                        )
                        self.animation.plan_job("objects", anim_args)
                    elif event.event == galo.EventData.CRASH_EVENT:
                        self.list_of_deleted.append(event.who)
                
                self.state = self.STATE_MOTION_ANIMATION_TICK
                
            elif self.state == self.STATE_MOTION_ANIMATION_TICK:
                
                if self.animation.is_over("objects"):
                    self.state = self.STATE_PENDING_REMOVAL
                    renpy.redraw(self, 0)
            
            elif self.state == self.STATE_PENDING_REMOVAL:
                
                while self.list_of_deleted:
                    creature = self.list_of_deleted.pop()
                    obj = self._shortcut4displayables[creature]
                    self.clusterizer.release(obj)
                    self.level.del_creature(creature)
                    del self._shortcut4displayables[creature]
                    del creature
                
                if self._winning:
                    self.state = self.STATE_WINNING
                elif self._loosing:
                    self.state = self.STATE_LOOSING
                else:
                    self.state = self.STATE_USER_LISTENING
                
                renpy.redraw(self, 0)
            
            
            if self.state in (self.STATE_WINNING, self.STATE_LOOSING):
                renpy.restart_interaction()
            elif self.animation.animate(st):
                renpy.redraw(self, 0)
            
            
            ## Visualization ##
            
            renderer = Render(w, h)
            
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
            
            if self.state == self.STATE_WINNING:
                return ("win", self._steps, self.level.souls)
            
            elif self.state == self.STATE_LOOSING:
                return ("loose", self._steps, self.level.souls)
            
            elif self.state == self.STATE_USER_LISTENING:
                
                if con.mkey_had_click(M_BUTTON1):
                    
                    wx, wy = screen2world(x, y, self.box)
                    
                    selected_cells = self.clusterizer.select(
                        CluBox(x=wx, y=wy, width=1, height=1)
                    )
                    
                    for c in selected_cells:
                        sx, sy = world2screen(c.box.x, c.box.y, self.box)
                        gotcha = isinstance(c, CellDisplayable) and \
                                 c.event(ev, x - sx, y - sy, st)
                        if gotcha:
                            players = self.level.creatures(
                                galo.CreatureData.PLAYER
                            )
                            if not players:
                                break
                            p = players[0]
                            if hex_distance(p.cell, c.cell) == 1:
                                self._steps += 1
                                self._update_ingame_menu()
                                self.expected_events.append(
                                    galo.EventData(
                                        event=galo.EventData.MOVE_EVENT,
                                        who=p,
                                        data=(p.cell, c.cell)  # from, to
                                    )
                                )
                                self.state = self.STATE_MOTION_ANIMATION
                                need_redraw = True
                            break
            
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
