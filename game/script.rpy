init offset = 10
init python:
    
    import os
    import gamelogics as galo
    
    lvldesc = galo.LevelDescription()




image ingame bg = "gui/background.jpg"




transform whipwhap:
    
    yalign 0.3
    xalign 1.0
    alpha 0.0
    
    parallel:
        easein 1.0 xalign 0.5
        pause 1.2
        easeout 1.0 xalign 0.0
    
    parallel:
        linear 1.0 alpha 1.0
        pause 1.2
        linear 1.0 alpha 0.0




screen LevelTitle(t):
    
    zorder 50
    
    text "[t]" size 48 at whipwhap


screen LevelShowScreen(levelinstance):
    
    key "game_menu" action NullAction()
    
    fixed:
        yalign 1.0
        minimum (config.screen_width, config.screen_height - 120)
        maximum (config.screen_width, config.screen_height - 120)
        add levelinstance




label start():
    
    scene ingame bg
    
    python:
        n = max(0, store.override_start_level)
        store.override_start_level = -1
        
    while n < LEVELS_COUNT:
        
        python:
            d1 = (n + 1) % 10
            d2 = (n + 1) // 10
            levelfilename = "map{}{}.lvl".format(d2, d1)
            leveltitle = LEVELS_DATA[n][0]
            levelsteps = LEVELS_DATA[n][1]
            levelclearable = LEVELS_DATA[n][2]
            state, steps, souls = "", 0, 0
            
            sd = renpy.get_screen("ingame_menu")
            if sd is not None:
                sd.scope["souls"] = levelclearable
                #renpy.restart_interaction()
        
        while state == "loose" or state == "":
            call runlevel(leveltitle, levelfilename)
            $ state, steps, souls = _return
        
        if state == "win":
            python:
                if steps <= levelsteps:
                    persistent.level_achieved_steps.add(n)
                if levelclearable and souls == 1:
                    persistent.level_achieved_souls.add(n)
                n += 1
                if n + 1 > persistent.current_level:
                    persistent.current_level = n + 1 # Нумеруются с 1
        
        elif state == "break":
            jump end

label end():
    
    return


label runlevel(levelname, levelfilename):
    
    show screen LevelTitle(levelname)
    
    python:
        try:
            lvlpath = renpy.fsencode("{}/{}/{}".format(
                config.gamedir, LEVELS_DIRECTORY, levelfilename
            ))
            lvldesc.load(lvlpath)
        except IOError:
            pass
        lvl = LevelDisplayable(lvldesc)
    
    call screen LevelShowScreen(lvl)
    
    python:
        del lvl
    
    hide screen LevelTitle
    
    return _return
