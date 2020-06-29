init offset = -2
init python:
    
    # Общие "константы" ################################################
    
    # Filesystem
    LEVELS_DIRECTORY = "data/levels"
    LEVELFILE_EXTENSION = "lvl"
    
    # Mathematica
    EPS = 1e-10
    CAMERA_VELOCITY = 100 # pixels per sec
    CAMERA_VELOCITY_MAX = 500 #  pixels per sec
    CAMERA_ACCELERATION = 10 # (pixels per sec) per sec   (px per sec^2)
    CAMERA_STOPLENGTH = min(config.screen_width, config.screen_height) * .25
    ANIMOTION_TIME = 0.5 # sec # mOtion!
    
    # Cells size preferences
    IMAGE_CELL_WIDTH = 135 #@HARDCODE
    IMAGE_CELL_HEIGHT = 120 #@HARDCODE
    IMAGE_CELL_HALFWIDTH = IMAGE_CELL_WIDTH // 2
    IMAGE_CELL_HALFHEIGHT = IMAGE_CELL_HEIGHT // 2
    
    OVERLAPW = int(IMAGE_CELL_HALFWIDTH / 2.25) + 1 #@MAGICNUMBER
    OVERLAPH = IMAGE_CELL_HALFHEIGHT
    OVERKOEF = OVERLAPH / OVERLAPW
    
    # Creatures size preferences
    CREATURE_WIDTH = 100 #@HARDCODE
    CREATURE_HEIGHT = 100 #@HARDCODE
    CREATURE_HALFWIDTH = CREATURE_WIDTH // 2
    CREATURE_HALFHEIGHT = CREATURE_HEIGHT // 2
    
    # Game
    LEVELS_DATA = (
        # Название; наилучшее мин. кол-во шагов; можно всех столкнуть
        ("Первый", 1, False),
        ("Два", 5, False),
        ("Три", 6, False),
        ("Туда-сюда и кругаля", 8, False),
        ("То же ещё раз", 5, True),
        ("Да, перекаты!", 10, True),
        ("Главное - правильно начать", 4, True),
    )
    LEVELS_COUNT = len(LEVELS_DATA)
