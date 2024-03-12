'''
@version: 1.0.0
@author: CrossingVoid
@date: 2023/03/05

The extend_widget.py is mainly for some widget basic on tk widget,
adding some features on them

'''
from Tkinter_template.Assets.soundeffect import play_sound
from Tkinter_template.Assets.image import tk_image
from collections import defaultdict
from tkinter import Button, Label


class BindButton(Button):
    '''
    for keyboard holdon feature
    need focus on 
    like use 'Return' for enter key
    '''

    def __init__(self, char, root=None, **option):
        self.char = char
        self.__state = False
        super().__init__(root, **option)
        self.__bind()

    def __bind(self):
        def keypress(event):
            if (self.char is None) or (event.keysym == self.char):
                self.config(relief='sunken')

        def keyrelease(event):
            if (self.char is None) or (event.keysym == self.char):
                self.config(relief='raised')
                if self.__state:
                    self.invoke()
                else:
                    self.__state = True

        self.bind('<KeyPress>', keypress)
        self.bind('<KeyRelease>', keyrelease)


class EffectButton(Button):
    '''
    achieve hover feature
    '''

    def __init__(self, color: tuple, sound: str = None, root=None, **option):
        '''
        color(first for bg, second for fg)
        '''
        self.color = color
        self.sound = sound
        super().__init__(root, **option)
        self.__bg = self['bg']
        self.__fg = self['fg']
        self.__bind()

    def __bind(self):
        def enter(event):
            if self.sound:
                play_sound(self.sound)
            self.config(bg=self.color[0], fg=self.color[1])

        def leave(event):
            self.config(bg=self.__bg, fg=self.__fg)

        self.bind('<Enter>', enter)
        self.bind('<Leave>', leave)

class SelectLabel(Label):
    label_collection = defaultdict(list)
    label_function = {}

    def __init__(self, category, root, **option) -> None:
        self.__category = category
        self.label_collection[self.__category].append(self)
        super().__init__(root, **option)

    @classmethod
    def clear(cls):
        cls.label_collection.clear()
        cls.label_function.clear()

    @classmethod
    def embed_function(cls, category: str, func):
        cls.label_function[category] = func

    @classmethod
    def show(cls, category: str, canvas: object, coordinate: tuple, interval: int, direction='right'):
        def select(arg):
            nonlocal choice_number
            if arg == 'down':
                if choice_number in range(0, len(cls.label_collection[category])-1):
                    play_sound("select")
                    choice_number += 1
                else:
                    return
            elif arg == 'up':
                if choice_number in range(1, len(cls.label_collection[category])):
                    play_sound("select")
                    choice_number -= 1
                else:
                    return

            for i in range(0, len(cls.label_collection[category])):
                if i == choice_number:
                    canvas.itemconfig(
                        f'arrow-{i}', state='normal')
                    cls.label_collection[category][i].config(
                        fg='indigo', bg='coral', relief='solid')
                else:
                    cls.label_collection[category][i].config(
                        fg='black', bg='lightblue', relief='flat')
                    canvas.itemconfig(
                        f'arrow-{i}', state='hidden')

        def choice(event):
            func = cls.label_function[category]
            func(
                cls.label_collection[category][choice_number]['text']
            )
        if (category not in cls.label_collection) or (category not in cls.label_function):
            raise ValueError(f"Categoey: {category} not in dictionary")

        canvas.unbind("<Down>")
        canvas.unbind("<Return>")
        canvas.unbind("<Up>")
        choice_number = 0

        for number, obj in enumerate(cls.label_collection[category]):
            canvas.create_window(coordinate[0], coordinate[1]+interval*number, anchor='w',
                                 window=obj, tags=f'label-{number}')
            if direction == 'right':
                canvas.create_image(coordinate[0]-25, coordinate[1]+interval*number, anchor='e',
                                    image=tk_image('play.png', 60, dirpath='images\\selectimage'), tags=(f'arrow-{number}', 'H'),
                                    state='hidden')
            # else:
            #     canvas.create_image(coordinate[0]-10, coordinate[1]+interval*number, anchor='e',
            #                         image=tk_image('play.png', 60, dirpath='images\\selectimage'), tags=(tagName, 'H',
            #                                                                                              state='hidden')

        canvas.bind(
            '<Down>', lambda event, args='down': select(args))
        canvas.bind(
            '<Up>', lambda event, args='up': select(args))
        canvas.bind('<Return>', choice)

        select('initial')