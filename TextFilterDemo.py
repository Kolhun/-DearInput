

import os
import sys
import dearpygui.dearpygui as dpg

dataCategory = [
    {"id": "001", "name": "Москва"},
    {"id": "002", "name": "Санкт-Петербург"},
    {"id": "003", "name": "Новосибирск"},
    {"id": "004", "name": "Екатеринбург"},
    {"id": "005", "name": "Казань"},
    {"id": "006", "name": "Moscow"},
    {"id": "007", "name": "Saint Petersburg"},
    {"id": "008", "name": "Novosibirsk"},
    {"id": "009", "name": "Yekaterinburg"},
    {"id": "010", "name": "Kazan"},
]
#gggg
TABLE_TAG = "tagTableWorkPopup"
def _truncate_string_low(s, length):
    return s if len(s) <= length else s[:length] + '...'


def _setValuePop(sender, app_data, user_data):
    index, key, data_id = user_data
    print(f"Выбран ID: {data_id}, ключ: {key}")
    #dpg.delete_item(item=popup_tag)


def _filter_table(filter_text, table_tag, original_data):

    filter_text = filter_text.lower()


    dpg.delete_item(table_tag, children_only=True)

    for index, (key, data) in enumerate(original_data.items()):
        if filter_text in data["name"].lower():
            with dpg.table_row(parent=table_tag, filter_key=data["name"]):
                for j in range(2):
                    if j == 0:
                        str_name = _truncate_string_low(data["id"], 11)
                    if j == 1:
                        str_name = _truncate_string_low(data["name"], 25)
                    dpg.add_selectable(
                        label=str_name,
                        span_columns=True,
                        user_data=(index, key, data["id"], "__selectCategory_popup1"),
                        callback=_setValuePop
                    )


def _on_input_change(sender, app_data, user_data):

    input_text = dpg.get_value("input_text")

    converted_text = cyrillic_support.decode_string(input_text)
    input_char_codes = [ord(char) for char in converted_text]
    moscow_char_codes = [ord(char) for char in "Москва"]

    print(
        f"Введенный текст: {input_text} -> Преобразованный текст: {converted_text} -> Код символов: {input_char_codes}")
    print(f"Слово 'Москва' -> Код символов: {moscow_char_codes}")

    filtered_data = filter_data(converted_text)

    sorted_results = sorted(filtered_data, key=lambda x: x["name"])

    print("Результаты фильтрации и сортировки:")
    for item in sorted_results:
        print(item)

    table_update(sorted_results)


def table_update(_list: list):

    if dpg.does_item_exist(TABLE_TAG):
        dpg.delete_item(item=TABLE_TAG)

    # Создаём тему для таблицы
    with dpg.theme() as table_theme:
        with dpg.theme_component(dpg.mvTable):
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)

    with dpg.table(
        header_row=True,
        no_host_extendX=True,
        delay_search=True,
        borders_innerH=True,
        borders_outerH=True,
        borders_innerV=True,
        borders_outerV=True,
        context_menu_in_body=True,
        row_background=True,
        parent="windows",
        policy=dpg.mvTable_SizingFixedFit,
        clipper=True,
        scrollY=True,
        tag=TABLE_TAG,
        no_host_extendY=True,
        width=400,
        height=200,
        freeze_rows=1
    ) as table_sel_rowss:
        dpg.add_table_column(label="ID")
        dpg.add_table_column(label="Имя")

        for data in _list:
            with dpg.table_row(parent=TABLE_TAG, filter_key=data["name"]):
                for j in range(2):
                    if j == 0:
                        str_name = _truncate_string_low(data["id"], 11)
                    if j == 1:
                        str_name = _truncate_string_low(data["name"], 25)
                    dpg.add_selectable(
                        label=str_name,
                        span_columns=True,
                    )

    dpg.bind_item_theme(table_sel_rowss, table_theme)
    print()

def filter_data(search_string):
    search_string = search_string.lower()
    filtered_data = [
        item for item in dataCategory
        if search_string in item["name"].lower()
    ]
    return filtered_data


def on_button_click(sender, app_data):
    input_text = dpg.get_value("input_text")

    converted_text = cyrillic_support.decode_string(input_text)
    input_char_codes = [ord(char) for char in converted_text]
    moscow_char_codes = [ord(char) for char in "Москва"]
    print(
        f"Введенный текст: {input_text} -> Преобразованный текст: {converted_text} -> Код символов: {input_char_codes}")
    print(f"Слово 'Москва' -> Код символов: {moscow_char_codes}")

    filtered_data = filter_data(converted_text)

    sorted_results = sorted(filtered_data, key=lambda x: x["name"])

    print("Результаты фильтрации и сортировки:")
    for item in sorted_results:
        print(item)


class CyrillicSupport:
    big_let_start = 0x00C0
    big_let_end = 0x00DF
    small_let_end = 0x00FF
    remap_big_let = 0x0410
    alph_len = big_let_end - big_let_start + 1
    alph_shift = remap_big_let - big_let_start

    def __init__(self, app_path):
        self.app_path = app_path
        self.font_path = os.path.join(self.app_path, 'fonts', 'C:/Windows/Fonts/times.ttf')

    def registry_font(self):
        with dpg.font_registry():
            with dpg.font(self.font_path, size=16) as font:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                dpg.add_font_range(0x0391, 0x03C9)
                dpg.add_font_range(0x2070, 0x209F)

                if sys.platform == 'win32':
                    self._remap_chars()
                dpg.bind_font(font)

    def _remap_chars(self):
        biglet = self.remap_big_let
        for i1 in range(self.big_let_start, self.big_let_end + 1):
            dpg.add_char_remap(i1, biglet)
            dpg.add_char_remap(i1 + self.alph_len, biglet + self.alph_len)
            biglet += 1

        dpg.add_char_remap(0x00A8, 0x0401)
        dpg.add_char_remap(0x00B8, 0x0451)

    def decode_string(self, instr: str):
        if sys.platform == 'win32':
            outstr = []
            for i in range(len(instr)):
                char_byte = ord(instr[i])
                if char_byte in range(self.big_let_start, self.small_let_end + 1):
                    char = chr(ord(instr[i]) + self.alph_shift)
                    outstr.append(char)
                elif char_byte == 0x00A8:
                    outstr.append(chr(0x0401))
                elif char_byte == 0x00B8:
                    outstr.append(chr(0x0451))
                else:
                    outstr.append(instr[i])

            return ''.join(outstr)
        else:
            return instr


def main():
    dpg.create_context()
    global cyrillic_support
    cyrillic_support = CyrillicSupport(os.getcwd())
    cyrillic_support.registry_font()

    with dpg.window(label="Пример с полем ввода и кнопкой", min_size=(600, 300),tag="windows"):
        dpg.add_button(label="Поиск", callback=on_button_click)
        dpg.add_input_text(
            label="Пробная версия фильтра",
            hint="Введите для фильтрации",
            callback=_on_input_change,
            user_data=("tagTableWorkPopup", dataCategory),
            width=300,
            tag="input_text",
            parent="windows"
        )
        table_update(dataCategory)
        # dpg.add_input_text(label="Введите текст:", tag="input_text")


    dpg.create_viewport(title='Пример DearPyGui', width=1024, height=768)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()

