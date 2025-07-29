from itertools import product
import datetime
from shouldersurfscore.classes import timeouts

class Attacker:
    '''
    Class represents an attacker.

    This is used to structure how the attacker might try to break the password
    given a password and a device they are trying to break into.
    '''
    def __init__(self, observed_password, device, strategy='default'):
        self.guess_queue = []
        self.observed_password = observed_password
        self.device = device

        if strategy == 'default':
            self.strategy = [
                self.sequential_guesses
            ]
        else:
            self.strategy = [
                getattr(self, strategy)
            ]

    def break_in(self) -> dict:
        '''
        Method to simulate an attacker breaking into a device, from their strategies based on starting guess `guess`. 

        Returns a dictionary with a few metrics calculated in it.
        '''
        analysis = {}

        for strategy in self.strategy:
            strategy(self.observed_password)

        analysis['guess_index'] = self.guess_queue.index(self.device.password)
        analysis['guess_percent'] = analysis['guess_index'] / len(self.guess_queue)

        # Calculate total practical time
        try:
            # Run device timeout for each guess
            for _ in range(analysis['guess_index']):
                self.device.timeout.make_guess()

            analysis['practical_time'] = self.device.timeout.elapsed_time
        
        # Handle situations where device locked out by setting practical_time to None.
        except timeouts.DeviceLockout:
            analysis['practical_time'] = None

        return analysis

    def sequential_guesses(self, observed_pin):
        '''
        Sequential guess strategy. 

        The attacker uses each character in the password in order.

        This will guess any password that has not already been guessed.
        '''
        guesses = []
        for length in self.device.valid_pin_lengths:
            guesses += list(product(self.device.key_space, repeat=length))

        guesses = [''.join(guess) for guess in guesses]
        self._append_guesses(guesses)

    def _append_guesses(self, new_guesses):
        '''
        Helper function to make sure that new guesses are allowed before adding them to the guess queue.
        '''
        guesses = [guess for guess in new_guesses if guess not in self.device.prohibited]
        guesses = [guess for guess in guesses if guess not in self.guess_queue]

        self.guess_queue += guesses