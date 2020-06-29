init python:
    
    import pygame
    from collections import defaultdict
    
    
    M_BUTTON1 = 1
    M_BUTTON2 = 2
    M_BUTTON3 = 3
    M_WHEELUP = 4
    M_WHEELDOWN = 5
    
    MMOD_MOVE = 0b0001
    MMOD_STOP = 0b0010
    MMOD_DRAG = 0b0100
    MMOD_DROP = 0b1000
    
    
    class _StateData(object):
        
        __slots__ = ("pre", "cur")
        
        def __init__(self):
            
            self.pre = False
            self.cur = False
        
        def setup(self, value):
            
            self.pre, self.cur = self.cur, value
        
        @property
        def click(self):
            
            return self.cur == False and self.pre == True
    
    
    class KeyboardMouseState(object):
        """
        Запоминалка состояний клавиш клавиатуры и мыши. Обычно
        используется внутри метода event класса Displayable.
        """
        
        def __init__(self):
            
            self._k_keys = defaultdict(_StateData)
            self._k_mods = 0
            self._m_keys = defaultdict(_StateData)
            self._m_mods = 0
            self._m_pre_x = None
            self._m_cur_x = None
            self._m_pre_y = None
            self._m_cur_y = None
        
        def _filter(self, key, mod):
            
            #key
            if key & (pygame.K_LCTRL | pygame.K_RCTRL):
                mod = pygame.KMOD_CTRL
            
            elif key & (pygame.K_LALT | pygame.K_RALT):
                mod = pygame.KMOD_ALT
            
            elif key & (pygame.K_LSHIFT | pygame.K_RSHIFT):
                mod = pygame.KMOD_SHIFT
            
            elif key & (pygame.K_LMETA | pygame.K_RMETA):
                mod = pygame.KMOD_META
            
            #mod
            if mod & (pygame.KMOD_LCTRL | pygame.KMOD_RCTRL):
                mod = pygame.KMOD_CTRL
            
            elif mod & (pygame.KMOD_LALT | pygame.KMOD_RALT):
                mod = pygame.KMOD_ALT
            
            elif mod & (pygame.KMOD_LSHIFT | pygame.KMOD_RSHIFT):
                mod = pygame.KMOD_SHIFT
            
            elif mod & (pygame.KMOD_LMETA | pygame.KMOD_RMETA):
                mod = pygame.KMOD_META
            
            elif mod & (pygame.KMOD_LSUPER | pygame.KMOD_RSUPER):
                mod = pygame.KMOD_SUPER
            
            return key, mod
        
        def update(self, ev, x, y):
            
            self._m_pre_x, self._m_cur_x = self._m_cur_x, x
            self._m_pre_y, self._m_cur_y = self._m_cur_y, y
            
            self._m_mods &= ~MMOD_STOP #reset mod in mods
            self._m_mods &= ~MMOD_DROP #reset mod in mods
            
            # This is prevent freeze a 'click' state
            for state in self._k_keys.itervalues():
                state.pre = False
            for state in self._m_keys.itervalues():
                state.pre = False
            
            if ev.type == pygame.KEYDOWN:
                key, mod = self._filter(ev.key, ev.mod)
                self._k_keys[key].setup(True)
                self._k_mods |= mod #setup mod in mods
            
            elif ev.type == pygame.KEYUP:
                key, mod = self._filter(ev.key, ev.mod)
                self._k_keys[key].setup(False)
                self._k_mods &= ~mod #reset mod in mods
            
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                self._m_keys[ev.button].setup(True)
                
            elif ev.type == pygame.MOUSEBUTTONUP:
                self._m_keys[ev.button].setup(False)
                reason = not(
                    self._m_keys[M_BUTTON1].cur or \
                    self._m_keys[M_BUTTON2].cur or \
                    self._m_keys[M_BUTTON3].cur
                )
                if reason and (self._m_mods & MMOD_DRAG):
                    self._m_mods &= ~MMOD_DRAG #reset mod in mods
                    self._m_mods |= MMOD_DROP #setup mod in mods
            
            elif ev.type == pygame.MOUSEMOTION:
                self._m_mods |= MMOD_MOVE #setup mod in mods
                reason = \
                    self._m_keys[M_BUTTON1].cur or \
                    self._m_keys[M_BUTTON2].cur or \
                    self._m_keys[M_BUTTON3].cur
                if reason:
                    self._m_mods |= MMOD_DRAG #setup mod in mods
            
            if ev.type != pygame.MOUSEMOTION:
                if self._m_mods & MMOD_MOVE:
                    self._m_mods &= ~MMOD_MOVE #reset mod in mods
                    self._m_mods |= MMOD_STOP #setup mod in mods
        
        def kkey_is_pressed(self, kkey):
            
            return self._k_keys[kkey].cur
        
        def kkey_had_click(self, kkey):
            
            return self._k_keys[kkey].click
        
        @property
        def kmods(self):
            
            return self._k_mods
        
        def mkey_is_pressed(self, mkey):
            
            return self._m_keys[mkey].cur
        
        def mkey_had_click(self, mkey):
            
            return self._m_keys[mkey].click
        
        @property
        def mmods(self):
            
            return self._m_mods
        
        def wheel_scrolls_up(self):
            
            return self._m_keys[M_WHEELUP].cur
        
        def wheel_scrolls_down(self):
            
            return self._m_keys[M_WHEELDOWN].cur
        
        @property
        def mouse_dx(self):
            
            dx = 0.0
            if self._m_pre_x is not None:
                dx = self._m_cur_x - self._m_pre_x
            return dx
        
        @property
        def mouse_dy(self):
            
            dy = 0.0
            if self._m_pre_y is not None:
                dy = self._m_cur_y - self._m_pre_y
            return dy
