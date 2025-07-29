from shouldersurfscore.classes import keys

normal_keyboard_list = [
    list('`1234567890-='),
    list('qwertyuiop[]\\'),
    list('asdfghjkl;\''),
    list('zxcvbnm,./')
]

normal_keyboard = keys.Keys(normal_keyboard_list, row_offset=[0, 1, 0.5, 0.5])

keypad_list = [
    list('123'),
    list('456'),
    list('789'),
    list('0')
]

normal_keypad = keys.Keys(keypad_list, row_offset=[0,0,0,1])