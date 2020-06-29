########################################################################
## Инициализация
########################################################################

init offset = 2
init python:
    
    import os
    
    
    class LoadLevelAction(Action):
        def __init__(self, editor, levelfile):
            self.editor = editor
            self.levelfile = levelfile
        def __call__(self):
            self.editor.load(self.levelfile)
    
    
    class SaveLevelAction(Action):
        def __init__(self, editor, levelfile):
            self.editor = editor
            self.levelfile = levelfile
            ext = ".{}".format(LEVELFILE_EXTENSION)
            if not self.levelfile.endswith(ext):
                self.levelfile = "{}{}".format(self.levelfile, ext)
        def __call__(self):
            self.editor.save(self.levelfile)
    
    
    editor_instance = LevelEditorDisplayable()


########################################################################
## Стили
########################################################################


########################################################################
## Экраны Редактора уровней
########################################################################


## Экран меню редактора уровней ########################################
##
## Показывает основную и общую структуру редактора. Экран частично
## копирует структуру screen game_menu.
screen scr_editor():
    tag menu
    predict False
    style_prefix "editor"
    add "gui/editor/background.png"
    frame:
        style "editor_outer_frame"
        vbox:
            frame:
                style "editor_menu_frame"
                hbox:
                    xalign 0.5
                    yalign 0.5
                    spacing 20
                    vbox:
                        hbox:
                            xalign 0.5
                            spacing 20
                            textbutton "Заново":
                                action ShowMenu(
                                    "confirm",
                                    _("Стереть всё и начать заново?\n"
                                    "Несохранённый прогресс будет потерян."),
                                    [
                                        Function(editor_instance.clear_and_start_from_scratch),
                                        Hide("confirm")
                                    ],
                                    Hide("confirm")
                                )
                            textbutton _("Загрузить"):
                                action ShowMenu(
                                    "scr_modalmenu_load"
                                )
                            textbutton _("Сохранить"):
                                action ShowMenu(
                                    "scr_modalmenu_save"
                                )
                        hbox:
                            xalign 0.5
                            spacing 20
                            textbutton "Опробовать" action Start("start_debug")
                            textbutton "Выйти в меню" action Return()
                    hbox:
                        yalign 0.5
                        spacing 20
                        textbutton "Кисть ячеек" action ShowMenu(
                            "scr_modalmenu_cellbrush"
                        )
                        textbutton "Кисть объектов" action ShowMenu(
                            "scr_modalmenu_creaturebrush"
                        )
            frame:
                style "editor_work_frame"
                add editor_instance

style editor_outer_frame is empty:
    background "gui/editor/overlay/editor_menu.png"
style editor_menu_frame is empty:
    ysize 102
    xfill True
style editor_work_frame is empty
style editor_button is gui_button


########################################################################
screen scr_modalmenu(message,
confirm_action=None, confirm_text=None,
reject_action=None, reject_text=None):
    zorder 200
    style_prefix "scr_modalmenu"
    add "gui/overlay/confirm.png"
    frame:
        vbox:
            xalign .5
            yalign .5
            spacing 25
            label _(message):
                style "scr_modalmenu_prompt"
                xalign 0.5
            transclude
            hbox:
                xalign 0.5
                spacing 84
                if confirm_text:
                    textbutton _(confirm_text) action confirm_action
                if reject_text:
                    textbutton _(reject_text) action reject_action

style scr_modalmenu_frame is gui_frame:
    background Frame(
        ["gui/confirm_frame.png", "gui/frame.png"],
        gui.confirm_frame_borders,
        tile=gui.frame_tile
    )
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5
    maximum (0.9, 0.8) #(config.screen_width, config.screen_height)
style scr_modalmenu_prompt is gui_prompt
style scr_modalmenu_prompt_text is gui_prompt_text:
    text_align 0.5
    layout "subtitle"
style scr_modalmenu_button is gui_medium_button:
    properties gui.button_properties("confirm_button")
style scr_modalmenu_button_text is gui_medium_button_text:
    properties gui.button_text_properties("confirm_button")


########################################################################
screen scr_modalmenu_load():
    default var_levelfile = ""
    modal True
    use scr_modalmenu(
        "Загрузка карты уровня",
        [
            LoadLevelAction(editor_instance, var_levelfile),
            SetVariable("debug_levelfilename", var_levelfile),
            Hide("scr_modalmenu_load")
        ],
        "Загрузить",
        Hide("scr_modalmenu_load"),
        "Отмена" \
    ): # Yeah, it's not funny:
        vpgrid:
            cols 1
            yinitial 1.0
            scrollbars "vertical"
            mousewheel True
            draggable True
            #side_xfill True
            for levelfile in iter_files(LEVELS_DIRECTORY, LEVELFILE_EXTENSION):
                textbutton "[levelfile]":
                    #xfill True
                    action SetScreenVariable("var_levelfile", levelfile)
    key "game_menu" action Hide("scr_modalmenu_load")


########################################################################
screen scr_modalmenu_save():
    default var_levelfile = ""
    default var_levelfile_value = ScreenVariableInputValue("var_levelfile")
    modal True
    use scr_modalmenu(
        "Сохранение карты уровня",
        [
            SaveLevelAction(editor_instance, var_levelfile),
            Hide("scr_modalmenu_save")
        ],
        "Сохранить",
        Hide("scr_modalmenu_save"),
        "Отмена" \
    ): # It's not funny here too:
        vbox:
            vpgrid:
                cols 1
                yinitial 1.0
                scrollbars "vertical"
                mousewheel True
                draggable True
                side_xfill True
                for levelfile in iter_files(LEVELS_DIRECTORY, LEVELFILE_EXTENSION):
                    textbutton "[levelfile]":
                        xfill True
                        action SetScreenVariable("var_levelfile", levelfile)
            button:
                key_events True
                xalign 0.5
                action var_levelfile_value.Toggle()
                input:
                    style "scr_modalmenu_save_label_text"
                    value var_levelfile_value
    key "game_menu" action Hide("scr_modalmenu_save")

style scr_modalmenu_save_label_text is gui_label_text:
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color


########################################################################
screen scr_modalmenu_cellbrush():
    default GRID_COLS = 4
    modal True
    use scr_modalmenu("Выберите кисть для ячеек",
    reject_action=Hide("scr_modalmenu_cellbrush"), reject_text="Отмена"):
        vbox:
            vpgrid:
                cols GRID_COLS
                spacing 8
                yinitial 1.0
                scrollbars "vertical"
                mousewheel True
                draggable True
                for b in cellbrushes: #@SEE editorviews.rpy
                    button:
                        xysize (IMAGE_CELL_WIDTH, IMAGE_CELL_HEIGHT)
                        add "[b.image_filename]"
                        action [
                            Function(
                                editor_instance.setup_brush,
                                BRUSHMODE_CELL,
                                b
                            ),
                            Hide("scr_modalmenu_cellbrush")
                        ]
    key "game_menu" action Hide("scr_modalmenu_cellbrush")


########################################################################
screen scr_modalmenu_creaturebrush():
    default GRID_COLS = 4
    modal True
    use scr_modalmenu("Выберите кисть для объектов",
    reject_action=Hide("scr_modalmenu_creaturebrush"), reject_text="Отмена"):
        vbox:
            vpgrid:
                cols GRID_COLS
                spacing 8
                yinitial 1.0
                scrollbars "vertical"
                mousewheel True
                draggable True
                for b in creaturebrushes: #@SEE editorviews.rpy
                    button:
                        xysize (CREATURE_WIDTH, CREATURE_HEIGHT)
                        add "[b.image_filename]"
                        action [
                            Function(
                                editor_instance.setup_brush,
                                BRUSHMODE_OBJECT,
                                b
                            ),
                            Hide("scr_modalmenu_creaturebrush")
                        ]
    key "game_menu" action Hide("scr_modalmenu_creaturebrush")
