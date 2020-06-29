################################################################################
## Инициализация
################################################################################

init offset = -1
init python:
    
    import random
    
    #store.dirtyhack_steps = 0 #@SMELL #@DIRTYHACK
    
    store.override_start_level = -1
    
    class OverrideStartLevelAction(Action):
        def __init__(self, n):
            self.n = n
        def __call__(self):
            store.override_start_level = self.n


################################################################################
## Стили
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## Внутриигровые экраны
################################################################################


## Экран разговора #############################################################
##
## Экран разговора используется, чтобы показывать пользователю диалог. Он
## использует два параметра, who и what, что, соответственно, имя говорящего
## персонажа и показываемый текст. (Параметр who может быть None, если имя не
## задано.)
##
## Этот экран должен создать текст с id "what", чтобы Ren'Py могла показать
## текст. Здесь также можно создать наложения с id "who" и id "window", чтобы
## применить к ним настройки стиля.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        if who is not None:

            window:
                style "namebox"
                text who id "who"

        text what id "what"


    ## Если есть боковое изображение ("голова"), показывает его над текстом. Не
    ## показывается на варианте для мобильных устройств — места нет.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos


## Экран ввода #################################################################
##
## Этот экран используется, чтобы показывать renpy.input. Параметр запроса,
## используемый, чтобы вводить в него текст.
##
## Этот экран должен создать наложение ввода с id "input", чтобы принять
## различные вводимые параметры.
##
## http://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xalign gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Экран выбора ################################################################
##
## Этот экран используется, чтобы показывать внутриигровые выборы,
## представленные оператором menu. Один параметр, вложения, список объектов,
## каждый с заголовком и полями действия.
##
## http://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


## Когда это true, заголовки меню будут проговариваться рассказчиком. Когда
## false, заголовки меню будут показаны как пустые кнопки.
define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 225
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")


## Экран быстрого меню #########################################################
##
## Быстрое меню показывается внутри игры, чтобы обеспечить лёгкий доступ ко
## внеигровым меню.

screen ingame_menu():
    
    ## Гарантирует, что это появляется поверх других экранов.
    zorder 100
    
    default steps = 0
    default souls = False
    
    fixed:
        minimum (config.screen_width, 130)
        maximum (config.screen_width, 130)
        
        add "gui/ingamemenu_background.png"
        
        add "gui/label_steps.png" xpos 70 ypos 28
        
        hbox xpos 130 ypos 75:
            for digit in str(steps % 10000).zfill(4):
                add "gui/digits/{}.png".format(digit) yanchor 1.0
        
        if souls:
            add "gui/label_souls.png" xpos 486 ypos 28
        
        imagebutton xpos 800 ypos 4:
            auto "gui/button/ingamemenu_%s_button_restart.png"
            action Confirm("onceagain", Return(("loose", 0, 0)))
        
        imagebutton xpos 900 ypos 4:
            auto "gui/button/ingamemenu_%s_button_quit.png"
            action Confirm("confirm", Return(("break", 0, 0)))


# Данный код гарантирует, что экран быстрого меню будет показан в игре в любое
# время, если только игрок не скроет интерфейс.
init python:
    config.overlay_screens.append("ingame_menu")


################################################################################
## Экраны Главного и Игрового меню
################################################################################

## Экран главного меню #########################################################
##
## Используется, чтобы показывать главное меню, когда Ren'Py запустилась.
##
## http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():
    
    tag menu
    
    add gui.main_menu_background
    
    add "gui/label_author.png" xalign 1.0 yalign 0.98
    
    if config.developer == True:
        textbutton _("Редактор") yalign 1.0 action ShowMenu("scr_editor")
    
    vbox xalign 0.5 ypos 40:
        
        add "gui/label_title.png" xalign 0.5
        
        null height 120
        
        hbox xalign 0.5:
            
            spacing 10
            
            imagebutton auto "gui/button/mainmenu_%s_play.png":
                action Start()
            
            if persistent.current_level > 1:
                imagebutton auto "gui/button/mainmenu_%s_continue.png":
                    action ShowMenu("continue_menu")
            
            if renpy.variant("pc"):
                imagebutton auto "gui/button/mainmenu_%s_quit.png":
                    action Quit(confirm=not main_menu)


screen continue_menu():
    
    tag menu
    
    add gui.main_menu_background
    
    vpgrid:
        cols 6   
        draggable False
        mousewheel False
        xalign 0.67
        yalign 0.02
        
        for n in xrange(LEVELS_COUNT):
            
            python:
                _img = "gui/button/continuemenu_button_frame{}.png".format(
                    random.randint(1, 3)
                )
                levelsteps = LEVELS_DATA[n][1]
                levelsouls = LEVELS_DATA[n][2]
            
            fixed:
                
                minimum (129 + 31, 100) # 79 + 50, 2*50
                maximum (129 + 31, 100)
                
                add _img:
                    xpos 0 ypos (100 - 79) // 2
                
                if n + 1 <= persistent.current_level:
                    
                    hbox:
                        xalign 0.18 ypos (100 - 40) // 2
                        
                        if n + 1 > 9:
                            add "gui/digits/{}.png".format((n + 1) // 10)
                        add "gui/digits/{}.png".format((n + 1) % 10)
                    
                    vbox:
                        xpos 80 ypos 0
                        
                        if levelsouls:
                            if n in persistent.level_achieved_souls:
                                add "gui/label_souls.png"
                            else:
                                add "gui/label_closed.png"
                        else:
                            add "gui/label_none.png"
                        
                        if n in persistent.level_achieved_steps:
                            add "gui/label_steps.png"
                        else:
                            add "gui/label_closed.png"
                        
                    imagebutton:
                        xpos 0 ypos (100 - 79) // 2
                        auto "gui/button/continuemenu_%s_button.png"
                        action [OverrideStartLevelAction(n), Start()]
                
                else:
                    add "gui/label_denied.png":
                        xpos (79 - 50) // 2 ypos (100 - 50) // 2
    
    imagebutton:
        auto "gui/button/confirmmenu_%s_button_no.png"
        xalign 0.5
        yalign 0.98
        action Return()


## Экран Об игре ###############################################################
##
## Этот экран показывает авторскую информацию об игре и Ren'Py.
##
## В этом экране нет ничего особенного, и он служит только для примера того,
## каким можно сделать свой экран.

screen about():

    tag menu
    
    style_prefix "about"

    vbox:

        label "[config.name!t]"
        text _("Версия [config.version!t]\n")

        ## gui.about обычно установлено в options.rpy.
        if gui.about:
            text "[gui.about!t]\n"

        text _("Сделано с помощью {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


## Это переустанавливается в options.rpy, чтобы добавить текст на экран Об игре.
define gui.about = ""


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


################################################################################
## Дополнительные экраны
################################################################################


## Экран подтверждения #########################################################
##
## Экран подтверждения вызывается, когда Ren'Py хочет спросить у пользователя
## вопрос да или нет.
##
## http://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Гарантирует, чтобы другие экраны не были доступны, пока этот экран
    ## показан.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 25

            if message == "onceagain":
                add "gui/imagetext_onceagain.png" xalign 0.5
            else: # message == "quit" or other
                add "gui/imagetext_quit.png" xalign 0.5
            
            add "gui/imagetext_areyousure.png" xalign 0.5

            hbox:
                xalign 0.5
                spacing 84
                
                imagebutton:
                    auto "gui/button/confirmmenu_%s_button_yes.png"
                    action yes_action
                imagebutton:
                    auto "gui/button/confirmmenu_%s_button_no.png"
                    action no_action

    ## Правый клик и esc как ответ "нет".
    key "game_menu" action no_action


style confirm_frame is gui_frame

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5


## Экран индикатора пропуска ###################################################
##
## Экран индикатора пропуска показывается, чтобы показать, что идёт пропуск.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 5

            text _("Пропускаю")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## Эта трансформация используется, чтобы мигать стрелками одной за другой.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## Нам надо использовать шрифт, имеющий в себе символ U+25B8 (стрелку выше).
    font "DejaVuSans.ttf"


## Экран уведомлений ###########################################################
##
## Экран уведомлений используется, чтобы показать пользователю извещение.
## (Например, когда игра автосохранилась, или был сделан скриншот.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text message

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## Экран NVL ###################################################################
##
## Этот экран используется в диалогах и меню режима NVL.
##
## http://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Показывает диалог или в vpgrid, или в vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Показывает меню, если есть. Меню может показываться некорректно, если
        ## config.narrator_menu установлено на True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## Это контролирует максимальное число строк NVL, могущих показываться за раз.
define config.nvl_list_length = 6

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    text_align gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    text_align gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    text_align gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.button_text_properties("nvl_button")



################################################################################
## Мобильные варианты
################################################################################

style pref_vbox:
    variant "medium"
    xsize 375

## Раз мышь может не использоваться, мы заменили быстрое меню версией,
## использующей меньше кнопок и больше по размеру, чтобы легче их коснуться.
screen quick_menu():
    
    null
    
    #variant "touch"
    #
    #zorder 100
    #
    #hbox:
    #    style_prefix "quick"
    #
    #    xalign 0.5
    #    yalign 1.0
    #
    #    textbutton _("Назад") action Rollback()
    #    textbutton _("Пропуск") action Skip() alternate Skip(fast=True, confirm=True)
    #    textbutton _("Авто") action Preference("auto-forward", "toggle")
    #    textbutton _("Меню") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 284

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 334

style slider_pref_vbox:
    variant "small"
    xsize None

style slider_pref_slider:
    variant "small"
    xsize 500




