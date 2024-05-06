import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import colorchooser
from PIL import Image, ImageDraw, ImageTk, ImageFont
import os

win = Tk()

win.config(bg='white')
win.title('WaterSigner')
win.geometry('550x350+515+250')
win.resizable(width=False, height=False)

current_color = 'black'
ws_text = 'Water Sign'
current_position = (0, 0)

font_dir = 'C:/Windows/Fonts'
available_fonts = [os.path.splitext(f)[0].capitalize() for f in os.listdir(font_dir) if f.endswith('.ttf')]

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
my_path = desktop + '\edited_image.jpg'
print(my_path)


def upload_photo():
    """Загружаем фото"""
    global cropped_image, file_path, image_width, image_height
    file_path = filedialog.askopenfilename(filetypes=[('Изображения', '*.png;*.jpg;*.jpeg;*.gif;*.bmp')])
    if file_path:
        image = Image.open(file_path)
        image_width, image_height = image.size
        if image_width > 350 or image_height > 200:
            scale = min(350 / image_width, 200 / image_height)
            new_width = int(image_width * scale)
            new_height = int(image_height * scale)
            image = image.resize((new_width, new_height))
        cropped_image = ImageTk.PhotoImage(image)
        canvas.create_image(185, 100, anchor=CENTER, image=cropped_image)
        canvas.image = cropped_image
        upload_myPhoto.config(text='Изображение\nзагружено')


def get_text():
    """Получить текст из Entry"""
    global ws_text
    ws_text = entry_waterSign.get()
    print(ws_text)


def choose_color():
    """Выбор цвета"""
    global current_color
    color = colorchooser.askcolor()[1]
    current_color = color
    print(current_color)


def selected_combobox(event):
    """Получение значения выпадающего списка (позиции)"""
    global selection
    selection = position.get()
    choose_position()


def choose_position():
    """Определение координат позиции"""
    global current_position
    if selection == position_list[0]:  #ЦЕНТР
        x_cord = image_width / 2
        y_cord = image_height / 2
        current_position = x_cord, y_cord
    if selection == position_list[1]:  #ВПРАВО-ВВЕРХ
        x_cord = image_width - image_width / 3
        y_cord = 0
        current_position = x_cord, y_cord
    if selection == position_list[2]:  #ВЛЕВО-ВВЕРХ
        x_cord = 0
        y_cord = 0
        current_position = x_cord, y_cord
    if selection == position_list[3]:  #ВПРАВО-ВНИЗ
        x_cord = image_width - image_width / 3
        y_cord = image_height - image_height / 5
        current_position = x_cord, y_cord
    if selection == position_list[4]:  #ВЛЕВО-ВНИЗ
        x_cord = 0
        y_cord = image_height - image_height / 5
        current_position = x_cord, y_cord


def get_font_options():
    global final_font
    get_text()
    tkinter_font_family = current_font.get()
    tkinter_font_size = current_size.get()
    font_path = 'C:/Windows/Fonts/' + tkinter_font_family + '.ttf'
    final_font = ImageFont.truetype(font_path, tkinter_font_size)


def add_watermark():
    """Добавление конечного водяного знака на фото"""
    get_font_options()
    image = Image.open(file_path)
    drawing = ImageDraw.Draw(image)
    drawing.text(current_position,
                 ws_text,
                 fill=current_color,
                 font=final_font)
    image.save(my_path)
    upload_myPhoto.config(text='Загрузить\nизображение')
    print('Новое изображение сформировано!')


def show_config():
    get_font_options()
    text_example.config(font=current_font, fg=current_color, text=ws_text)


def open_settings():
    """Диалоговое окно настроек текста"""
    global current_style, current_font, current_size, final_font, text_example

    setting_dialog = tkinter.Toplevel(win)
    setting_dialog.title('Настройка текста')
    setting_dialog.config(bg='white')
    setting_dialog.geometry('420x250+620+350')
    setting_dialog.resizable(width=False, height=False)
    setting_dialog.columnconfigure(1, weight=1)

    font_label = tkinter.Label(setting_dialog, text='Шрифт:', justify=RIGHT, bg='white', font=('Georgia', 9))
    font_label.grid(row=0, column=0, ipadx=5, ipady=1, padx=5, pady=5, sticky='ew')
    current_font = tkinter.StringVar(setting_dialog)
    current_font.set('Arial')
    font_list = tkinter.OptionMenu(setting_dialog, current_font, *available_fonts)
    font_list.grid(row=0, column=1, ipadx=40, ipady=1, padx=5, pady=5, sticky='ew')

    size_label = tkinter.Label(setting_dialog, text='Размер:', justify=RIGHT, bg='white', font=('Georgia', 9))
    size_label.grid(row=2, column=0, ipadx=5, ipady=1, padx=5, pady=5, sticky='ew')
    current_size = tkinter.IntVar(setting_dialog)
    current_size.set(12)
    slider = tkinter.Scale(setting_dialog, from_=8, to=72, orient=tkinter.HORIZONTAL, variable=current_size, bg='white',
                           relief=GROOVE)
    slider.grid(row=2, column=1, ipadx=40, ipady=1, padx=5, pady=5, sticky='ew')

    text_example = tkinter.Label(setting_dialog, text='Водяной знак', bg='white')
    text_example.grid(row=4, column=0, columnspan=2, ipadx=40, ipady=1, padx=5, pady=5, sticky='ew')

    apply_button = tkinter.Button(setting_dialog, text='Применить', command=show_config, bg='#f0f0f0',
                                  activebackground='light grey', relief=GROOVE, font=('Consolas', 12))
    apply_button.grid(row=3, column=0, columnspan=2, ipadx=40, ipady=1, padx=5, pady=5, sticky='ew')


win.columnconfigure(0, weight=0)
win.columnconfigure(1, weight=1)
win.rowconfigure(0, weight=2)

win.rowconfigure(2, weight=1)

win.rowconfigure(3, weight=10)

upload_myPhoto = tkinter.Button(win, text='Загрузить\nизображение', font=('Consolas', 12),
                                justify=CENTER, bg='#f0f0f0', activebackground='light grey',
                                relief=GROOVE, command=upload_photo)
upload_myPhoto.grid(row=0, column=0, rowspan=6, ipadx=6, ipady=55, padx=5, pady=5, sticky='nsew')

first_label = tkinter.Label(win, text='Текст водяного знака', font=('Georgia', 9), anchor=CENTER,
                            justify=LEFT, borderwidth=0, relief='groove', bg='white')
first_label.grid(row=0, column=1, ipadx=15, ipady=5, padx=5, pady=5)

second_label = tkinter.Label(win, text='Позиция водяного знака', font=('Georgia', 9), anchor=E,
                             justify=LEFT, borderwidth=0, relief='groove', bg='white')
second_label.grid(row=1, column=1, columnspan=1, rowspan=1, ipadx=6, ipady=2, padx=5, pady=5, sticky='NSEW')

save_newImage = tkinter.Button(win, text='Сформировать новое изображение!', font=('Consolas', 12),
                               justify=CENTER, bg='#f0f0f0', activebackground='light grey',
                               relief=GROOVE, command=add_watermark)
save_newImage.grid(row=2, column=1, columnspan=3, rowspan=2, sticky='ew', ipadx=6, ipady=40, padx=5, pady=5)

canvas = tkinter.Canvas(win, width=350, height=200)
canvas.grid(row=4, column=1, columnspan=3, ipadx=6, ipady=2, padx=5, pady=5)

entry_waterSign = tkinter.Entry(win)
entry_waterSign.grid(row=0, column=2, ipadx=6, ipady=5, padx=5, pady=5)

color_button = tkinter.Button(win, text='Цвет', font=('Consolas', 10),
                              justify=CENTER, bg='#f0f0f0', activebackground='light grey',
                              relief=GROOVE, command=choose_color)
color_button.grid(row=0, column=3, ipadx=6, ipady=2, padx=5, pady=5, sticky=NSEW)

setting_button = tkinter.Button(win, text='Настроить', font=('Consolas', 10),
                                justify=CENTER, bg='#f0f0f0', activebackground='light grey',
                                relief=GROOVE, command=open_settings)
setting_button.grid(row=1, column=3, ipadx=6, ipady=2, padx=5, pady=5)

position_list = ['ЦЕНТР', 'ВПРАВО-ВВЕРХ', 'ВЛЕВО-ВВЕРХ', 'ВПРАВО-ВНИЗ', 'ВЛЕВО-ВНИЗ']
position = ttk.Combobox(values=position_list, state='readonly')
position.grid(row=1, column=2, rowspan=1, ipadx=1, ipady=1, padx=5, pady=5, sticky='ew')
position.bind('<<ComboboxSelected>>', selected_combobox)

win.mainloop()
