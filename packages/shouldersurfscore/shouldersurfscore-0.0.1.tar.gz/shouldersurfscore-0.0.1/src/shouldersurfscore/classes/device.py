from itertools import product

class Device:
    def __init__(self, password, keypad, timeout, valid_pin_lengths, duplicate_keys_allowed=True,
                 sequential_keys_allowed=True, key_space=None):
        self.valid_pin_lengths = valid_pin_lengths
        self.password = password
        self.keypad = keypad
        self.timeout = timeout
        self.locked=True

        if key_space:
            self.key_space=key_space
        else:
            self.key_space = self.keypad.positions.keys()

        self.prohibited = []
        
        if not sequential_keys_allowed:
            for key, length in product(self.key_space, self.valid_pin_lengths):
                self.prohibited.append(key * length)
        if not duplicate_keys_allowed:
            raise NotImplementedError

    def enter_password(self, attempted_password):
        if attempted_password == self.password:
            self.locked = False
        else:
            self.timeout.make_guess()