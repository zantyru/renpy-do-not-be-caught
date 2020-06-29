init offset = -2
init python:
    
    if persistent.current_level is None:
        persistent.current_level = 1
    
    if persistent.level_achieved_steps is None:
        persistent.level_achieved_steps = set()
    
    if persistent.level_achieved_souls is None:
        persistent.level_achieved_souls = set()
