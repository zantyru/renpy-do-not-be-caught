init offset = 10
init python:
    
    debug_levelfilename = None




label start_debug():
    
    scene ingame bg
    
    if debug_levelfilename:
        call runlevel("Test&Debug", debug_levelfilename)
    
    return
