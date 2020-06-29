################################################################################
## Инициализация
################################################################################

## Значение инициализации позволяет init коду в этом файле запускаться перед
## init кодом других файлов.
init offset = -2

## Вызываю gui.init, чтобы сбросить стили, чувствительные к стандартным
## значениям и задать высоту и ширину окна игры.
init python:
    gui.init(1066, 600)



################################################################################
## Конфигурируемые Переменные GUI
################################################################################


## Цвета #######################################################################
##
## Цвета текста в интерфейсе.

## Акцентный цвет используется в заголовках и подчёркнутых текстах.
define gui.accent_color = '#0099ff'

## Цвет используемый в текстовой кнопке, когда она не выбрана и не наведена.
define gui.idle_color = '#aaaaaa'

## Small_color используется в маленьком тексте, который должен быть ярче/темнее,
## для достижения вышеуказанного эффекта.
define gui.idle_small_color = '#888888'

## Цвет, используемых в кнопках и панелях, когда они наведены.
define gui.hover_color = '#0099ff'

## Цвет, используемый текстовой кнопкой, когда она выбрана, но не наведена.
## Кнопка может быть выбрана, если это текущий экран или текущее значение
## настройки.
define gui.selected_color = '#555555'

## Цвет, используемый текстовой кнопкой, когда она не может быть выбрана.
define gui.insensitive_color = '#aaaaaa7f'

## Цвета, используемые для частей панелей, которые не заполняются. Они не
## используются напрямую, а только при воссоздании файлов изображений.
define gui.muted_color = '#66c1ff'
define gui.hover_muted_color = '#99d6ff'

## Цвета, используемые в тексте диалогов и выборов.
define gui.text_color = '#404040'
define gui.interface_text_color = '#404040'


## Шрифты и их размеры #########################################################

## Шрифт, используемый внутриигровым текстом.
define gui.text_font = "DejaVuSans.ttf"

## Шрифт, используемый именами персонажей.
define gui.name_text_font = "DejaVuSans.ttf"

## Шрифт, используемый текстом вне игры.
define gui.interface_text_font = "DejaVuSans.ttf"

## Размер нормального текста диалога.
define gui.text_size = 19

## Размер для имён персонажей.
define gui.name_text_size = 25

## Размер текста в пользовательском интерфейсе.
define gui.interface_text_size = 20

## Размер заголовков в пользовательском интерфейсе.
define gui.label_text_size = 24

## Размер текста на экране уведомлений.
define gui.notify_text_size = 14

## Размер заголовка игры.
define gui.title_text_size = 42


## Главное и игровое меню. #####################################################

## Изображения, используемые в главном и игровом меню.
define gui.main_menu_background = "gui/main_menu.png"
define gui.game_menu_background = "gui/game_menu.png"

## Должны ли мы показывать название и версию игры?
define gui.show_name = True


## Диалог ######################################################################
##
## Эти переменные контролируют, как диалог появляется на отдельной строчке.

## Высота текстового окна, содержащего диалог.
define gui.textbox_height = 155

## Местоположение текстового окна по вертикали экрана. 0.0 — верх, 0.5 — центр,
## и 1.0 — низ.
define gui.textbox_yalign = 1.0


## Местоположение имени говорящего персонажа в отношении текстового окна. Это
## могут быть целые значения в пикселях слева и сверху от начала окна или
## процентное отношение, например, 0.5 для центрирования.
define gui.name_xpos = 200
define gui.name_ypos = 0

## Горизонтальное выравнивание имени персонажа. Это может быть 0.0
## для левоориентированного, 0.5 для центрированного, и 1.0 для
## правоориентированного выравнивания.
define gui.name_xalign = 0.0

## Ширина, высота и границы окна, содержащего имя персонажа или None, для
## автоматической размерки.
define gui.namebox_width = None
define gui.namebox_height = None

## Границы окна, содержащего имя персонажа слева, сверху, справа и снизу по
## порядку.
define gui.namebox_borders = Borders(5, 5, 5, 5)

## Если True, фон текстового окна будет моститься (расширяться по эффекту
## плитки), если False, фон текстового окна будет фиксированным.
define gui.namebox_tile = False


## Размещение диалога по отношению к текстовому окну. Это могут быть целые
## значения в пикселях слева и сверху от текстового окна или процентное
## отношение, например, 0.5 для центрирования.
define gui.dialogue_xpos = 224
define gui.dialogue_ypos = 42

## Максимальная ширина диалогового текста в пикселях.
define gui.dialogue_width = 620

## Горизонтальное выравнивание диалогового текста. Это может быть
## 0.0 для левоориентированного, 0.5 для центрированного, и 1.0 для
## правоориентированного выравнивания.
define gui.dialogue_text_xalign = 0.0


## Кнопки ######################################################################
##
## Эти переменные, вместе с файлами изображений в gui/button, контролируют
## аспекты того, как кнопки отображаются.

## Ширина и высота кнопки в пикселях. Если None, Ren'Py самостоятельно
## рассчитает размер.
define gui.button_width = None
define gui.button_height = 30

## Границы каждой стороны кнопки в порядке слева, сверху, справа, снизу.
define gui.button_borders = Borders(4, 4, 4, 4)

## Если True, фон изображения будет моститься. Если False, фон изображения будет
## линейно масштабирован.
define gui.button_tile = False

## Шрифт, используемый кнопкой.
define gui.button_text_font = gui.interface_text_font

## Размер текста, используемый кнопкой.
define gui.button_text_size = gui.interface_text_size

## Цвет текста в кнопке в различных состояниях.
define gui.button_text_idle_color = gui.idle_color
define gui.button_text_hover_color = gui.hover_color
define gui.button_text_selected_color = gui.selected_color
define gui.button_text_insensitive_color = gui.insensitive_color

## Горизонтальное выравнивание текста в кнопке. (0.0 — лево, 0.5 — по центру,
## 1.0 — право).
define gui.button_text_xalign = 0.0


## Эти переменные переписывают настройки различных видов кнопок. Пожалуйста,
## посмотрите документацию по gui, для просмотра всех вариаций кнопок, и для
## чего каждая из них нужна.
##
## Эти настройки используются стандартным интерфейсом:

define gui.radio_button_borders = Borders(21, 4, 4, 4)

define gui.check_button_borders = Borders(21, 4, 4, 4)

define gui.confirm_button_text_xalign = 0.5

define gui.page_button_borders = Borders(9, 4, 9, 4)

define gui.quick_button_borders = Borders(9, 4, 9, 0)
define gui.quick_button_text_size = 12
define gui.quick_button_text_idle_color = gui.idle_small_color
define gui.quick_button_text_selected_color = gui.accent_color

## Вы также можете добавить собственные настройки, добавляя правильно-
## именованные переменные. Например, вы можете раскомментировать следующую
## строчку, чтобы установить ширину кнопок навигации.

# define gui.navigation_button_width = 250


## Кнопки Выбора ###############################################################
##
## Кнопки выбора используются во внутриигровых меню.

define gui.choice_button_width = 658
define gui.choice_button_height = None
define gui.choice_button_tile = False
define gui.choice_button_borders = Borders(84, 5, 84, 5)
define gui.choice_button_text_font = gui.text_font
define gui.choice_button_text_size = gui.text_size
define gui.choice_button_text_xalign = 0.5
define gui.choice_button_text_idle_color = "#cccccc"
define gui.choice_button_text_hover_color = "#ffffff"


## Кнопки Слотов ###############################################################
##
## Кнопка слотов — особый вид кнопки. Она содержит миниатюру и текст,
## описывающий слот сохранения. Слот сохранения использует файлы из gui/button,
## как и другие виды кнопок.

## Кнопка слота сохранения.
define gui.slot_button_width = 230
define gui.slot_button_height = 172
define gui.slot_button_borders = Borders(9, 9, 9, 9)
define gui.slot_button_text_size = 12
define gui.slot_button_text_xalign = 0.5
define gui.slot_button_text_idle_color = gui.idle_small_color

## Ширина и высота миниатюры, используемой слотом сохранения.
define config.thumbnail_width = 214
define config.thumbnail_height = 120

## Количество колонок и рядов в таблице слотов.
define gui.file_slot_cols = 3
define gui.file_slot_rows = 2


## Позиционирование и Интервалы ################################################
##
## Эти переменные контролируют позиционирование и интервалы различных элементов
## пользовательского интерфейса.

## Местоположение левого края навигационных кнопок по отношению к левому краю
## экрана.
define gui.navigation_xpos = 34

## Вертикальная позиция индикатора пропуска.
define gui.skip_ypos = 9

## Вертикальная позиция экрана уведомлений.
define gui.notify_ypos = 38

## Интервал между выборами в меню.
define gui.choice_spacing = 19

## Кнопки в секции навигации главного и игрового меню.
define gui.navigation_spacing = 4

## Контролирует интервал между настройками.
define gui.pref_spacing = 9

## Контролирует интервал между кнопками настройки.
define gui.pref_button_spacing = 0

## Интервал между кнопками страниц.
define gui.page_spacing = 0

## Интервал между слотами.
define gui.slot_spacing = 9

## Позиция текста главного меню.
define gui.main_menu_text_xalign = 1.0


## Рамки #######################################################################
##
## Эти переменные контролируют вид рамок, содержащих компоненты
## пользовательского интерфейса, когда наложения или окна не представлены.

## Генерирует рамки, представленные кодом игрока.
define gui.frame_borders = Borders(4, 4, 4, 4)

## Рамки, используемые в частях экрана подтверждения.
define gui.confirm_frame_borders = Borders(34, 34, 34, 34)

## Рамки, используемые в частях экрана пропуска.
define gui.skip_frame_borders = Borders(14, 5, 42, 5)

## Рамки, используемые в частях экрана уведомлений.
define gui.notify_frame_borders = Borders(14, 5, 34, 5)

## Должны ли фоны рамок моститься?
define gui.frame_tile = False


## Панели, Полосы прокрутки и Ползунки #########################################
##
## Эти настройки контролируют вид и размер панелей, полос прокрутки и ползунков.
##
## Стандартный GUI использует только ползунки и вертикальные полосы прокрутки.
## Все остальные панели используются только через программируемый код.

## Высота горизонтальных панелей, полос прокрутки и ползунков. Ширина
## вертикальных панелей, полос прокрутки и ползунков.
define gui.bar_size = 30
define gui.scrollbar_size = 10
define gui.slider_size = 25

## True, если изображения панелей должны моститься. False, если они должны быть
## линейно масштабированы.
define gui.bar_tile = False
define gui.scrollbar_tile = False
define gui.slider_tile = False

## Горизонтальные границы.
define gui.bar_borders = Borders(4, 4, 4, 4)
define gui.scrollbar_borders = Borders(4, 4, 4, 4)
define gui.slider_borders = Borders(4, 4, 4, 4)

## Вертикальные границы.
define gui.vbar_borders = Borders(4, 4, 4, 4)
define gui.vscrollbar_borders = Borders(4, 4, 4, 4)
define gui.vslider_borders = Borders(4, 4, 4, 4)

## Что делать с непрокручиваемыми полосами прокрутки в интерфейсе. "hide" прячет
## их, а None их показывает.
define gui.unscrollable = "hide"


## История #####################################################################
##
## Экран истории показывает диалог, который игрок уже прошёл.

## Количество диалоговых блоков истории, которых Ren'Py будет хранить.
define config.history_length = 250

## Высота доступных записей на экране истории, или None, чтобы задать высоту в
## зависимость от производительности.
define gui.history_height = 117

## Местоположение, ширина и выравнивание заголовка, показывающего имя говорящего
## персонажа.
define gui.history_name_xpos = 150
define gui.history_name_ypos = 0
define gui.history_name_width = 125
define gui.history_name_xalign = 1.0

## Местоположение, ширина и выравнивание диалогового текста.
define gui.history_text_xpos = 142
define gui.history_text_ypos = 5
define gui.history_text_width = 617
define gui.history_text_xalign = 0.0


## Режим NVL ###################################################################
##
## Экран режима NVL показывает диалог NVL персонажей.

## Границы фона окна NVL.
define gui.nvl_borders = Borders(0, 9, 0, 17)

## Высота доступных строчек в режиме NVL. Установите это на None, чтобы строчки
## динамически регулировали высоту.
define gui.nvl_height = 96

## Интервал между строчками в режиме NVL, если gui.nvl_height имеет значение
## None, и между строчками режима NVL и его меню.
define gui.nvl_spacing = 9

## Местоположение, ширина и выравнивание заголовка, показывающего имя говорящего
## персонажа.
define gui.nvl_name_xpos = 359
define gui.nvl_name_ypos = 0
define gui.nvl_name_width = 125
define gui.nvl_name_xalign = 1.0

## Местоположение, ширина и выравнивание диалогового текста.
define gui.nvl_text_xpos = 375
define gui.nvl_text_ypos = 7
define gui.nvl_text_width = 492
define gui.nvl_text_xalign = 0.0

## Местоположение, ширина и выравнивание текста nvl_thought (текст от лица
## персонажа nvl_narrator).
define gui.nvl_thought_xpos = 200
define gui.nvl_thought_ypos = 0
define gui.nvl_thought_width = 650
define gui.nvl_thought_xalign = 0.0

## Местоположение кнопок меню NVL.
define gui.nvl_button_xpos = 375
define gui.nvl_button_xalign = 0.0

## Локализация #################################################################

## Эта настройка контролирует доступ к разрыву линий. Стандартная настройка
## подходит для большинства языков. Список доступных значений можно найти на
## https://www.renpy.org/doc/html/style_properties.html#style-property-language

define gui.language = "unicode"


################################################################################
## Мобильные устройства
################################################################################

init python:

    ## Это увеличивает размер быстрых кнопок, чтобы сделать их доступнее для
    ## касания на планшетах и телефонах.
    if renpy.variant("touch"):

        gui.quick_button_borders = Borders(34, 12, 34, 0)

    ## Это изменяет размеры и интервалы различных элементов GUI, чтобы
    ## убедиться, что они будут лучше видны на телефонах.
    if renpy.variant("small"):

        ## Размеры шрифтов.
        gui.text_size = 25
        gui.name_text_size = 30
        gui.notify_text_size = 21
        gui.interface_text_size = 30
        gui.button_text_size = 29
        gui.label_text_size = 30

        ## Регулирует местоположение текстового окна.
        gui.textbox_height = 200
        gui.name_xpos = 67
        gui.text_xpos = 75
        gui.text_width = 917

        ## Изменяет размеры и интервалы объектов в игровом меню.
        gui.choice_button_width = 1033

        gui.navigation_spacing = 17
        gui.pref_button_spacing = 9

        gui.history_height = 159
        gui.history_text_width = 575

        ## Местоположение кнопок слотов.
        gui.file_slot_cols = 2
        gui.file_slot_rows = 2

        ## Режим NVL.
        gui.nvl_height = 142

        gui.nvl_name_width = 255
        gui.nvl_name_xpos = 271

        gui.nvl_text_width = 763
        gui.nvl_text_xpos = 288
        gui.nvl_text_ypos = 5

        gui.nvl_thought_width = 1033
        gui.nvl_thought_xpos = 17

        gui.nvl_button_width = 1033
        gui.nvl_button_xpos = 17

        ## Быстрые кнопки.
        gui.quick_button_text_size = 17



